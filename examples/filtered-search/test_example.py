"""Content preservation, product isolation and failure checks; no SDK execution."""
from pathlib import Path
import ast
import copy
import json
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch
import yaml

import build_example as build


class ExampleChecks(unittest.TestCase):
    def setUp(self):
        self.source = (build.ROOT / 'milvus-docs/site/en/userGuide/search-query-get/filtered-search.md').read_text()
        self.page = yaml.safe_load((build.ROOT / 'zdoc/filtered-search.page.yaml').read_text())
        self.profile = yaml.safe_load((build.ROOT / 'zdoc/presentation/cloud-sdk-tabs.yaml').read_text())
        self.values = json.loads((build.ROOT / 'zdoc/Variables.json').read_text())
        self.read = lambda file: (build.ROOT / 'zdoc' / file).read_text()

    def compose(self, source=None, page=None):
        return build.compose(self.source if source is None else source, self.page if page is None else page,
                             self.profile, self.values, self.values, self.read)

    def test_all_sixteen_cloud_examples_preserved_in_order(self):
        original = (build.ROOT / 'evidence/cloud.original.md').read_text()
        generated = build.products()['filtered-search.mdx']
        baseline = re.findall(r'<Tabs\b[^\n]*>\n(.*?)</Tabs>', original, re.S)
        result = re.findall(r'<Tabs\b[^\n]*>\n(.*?)</Tabs>', generated, re.S)
        self.assertEqual((len(baseline), len(result)), (2, 2))
        for a, b in zip(baseline, result):
            x, y = build.FENCE.findall(a), build.FENCE.findall(b)
            self.assertEqual(len(y), 8)
            normalize = lambda s: '\n'.join(line.rstrip() for line in s.splitlines() if line.strip())
            self.assertEqual([(lang, normalize(code)) for lang, code in x],
                             [(lang, normalize(code)) for lang, code in y])

    def test_complete_cloud_prose_and_image_urls_preserved(self):
        def prose(text):
            text = text.split('# Filtered Search', 1)[1]
            text = re.sub(r'<Tabs\b.*?</Tabs>', '', text, flags=re.S)
            text = build.FENCE.sub('', text)
            text = re.sub(r'\\?\{#[^}]+\}', '', text)
            text = re.sub(r'!\[[^\]]*\]', '![image]', text)
            return ' '.join(text.split())
        self.assertEqual(prose((build.ROOT / 'evidence/cloud.original.md').read_text()),
                         prose(build.products()['filtered-search.mdx']))

    def test_json_data_preserved_with_declared_punctuation_correction(self):
        original = (build.ROOT / 'evidence/cloud.original.md').read_text()
        expected = []
        for lang, code in build.FENCE.findall(original):
            if lang == 'json':
                expected.append(json.loads(re.sub(r',\s*\]', '\n]', code.replace('，', ','))))
        actual = [json.loads(code) for lang, code in build.FENCE.findall(build.products()['filtered-search.mdx']) if lang == 'json']
        self.assertEqual(expected, actual)

    def test_three_variables_shared_across_all_sdk_languages(self):
        self.assertEqual(set(build.VAR.findall(self.source)), {'product_name', 'example_endpoint', 'example_token'})
        output = build.products()
        for lang, code in build.FENCE.findall(output['milvus-filtered-search.md']):
            if lang != 'json':
                self.assertIn('http://localhost:19530', code)
                self.assertIn('root:Milvus', code)
        self.assertNotIn('YOUR_CLUSTER_', output['milvus-filtered-search.md'])
        self.assertNotIn('Zilliz CLI', output['milvus-filtered-search.md'])
        self.assertNotIn('zilliz vector', output['milvus-filtered-search.md'])
        self.assertNotIn('localhost', output['filtered-search.mdx'])
        self.assertIn('In Zilliz Cloud, filtered searches', output['filtered-search.mdx'])
        self.assertIn('In Milvus, filtered searches', output['milvus-filtered-search.md'])
        for text in output.values():
            self.assertNotIn('{{var.', text)
        self.assertIn('MilvusClient', output['filtered-search.mdx'])
        self.assertNotIn('Zilliz CloudClient', output['filtered-search.mdx'])

    def test_cli_prerequisites_and_filter_modes_preserved(self):
        mdx = build.products()['filtered-search.mdx']
        cli = [code for lang, code in build.FENCE.findall(mdx) if lang == 'shell']
        for code in cli:
            self.assertIn('zilliz login', code)
            self.assertIn('zilliz context set', code)
            body = re.search(r"--body '(.*?)'", code, re.S)[1]
            json.loads(body)
        self.assertNotIn('iterative_filter', cli[0])
        self.assertIn('iterative_filter', cli[1])

    def test_python_parse_and_rust_indentation_preserved(self):
        for text in [build.products()['filtered-search.mdx'], build.products()['milvus-filtered-search.md']]:
            for lang, code in build.FENCE.findall(text):
                if lang == 'python':
                    ast.parse(code)
                if lang == 'rust':
                    self.assertIn('\n    let client = ', code)
                    self.assertTrue(code.rstrip().endswith('}'))

    def test_missing_renamed_or_duplicate_group_fails(self):
        with self.assertRaisesRegex(ValueError, 'MISSING_BLOCK'):
            self.compose(self.source.replace('id="standard-filtering-code"', 'id="renamed"'))
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_OR_NESTED_BLOCK'):
            self.compose(self.source.replace('iterative-filtering-code', 'standard-filtering-code'))
        with self.assertRaisesRegex(ValueError, 'UNCLOSED_BLOCK'):
            self.compose(self.source.replace('<!-- doc:block:end id="iterative-filtering-code" -->', ''))

    def test_cli_targets_ids_not_order(self):
        blocks = build.scan(self.source)
        a, b = list(blocks.values())
        swapped = self.source[:a['start']] + self.source[b['start']:b['end']] + self.source[a['end']:b['start']] + self.source[a['start']:a['end']] + self.source[b['end']:]
        rendered, _, _ = self.compose(swapped)
        cli = [code for lang, code in build.FENCE.findall(rendered) if lang == 'shell']
        self.assertIn('iterative_filter', cli[0])
        self.assertNotIn('iterative_filter', cli[1])

    def test_add_cannot_overwrite_an_existing_language_or_repeat(self):
        page = copy.deepcopy(self.page)
        page['transforms'][0]['target']['language'] = 'python'
        with self.assertRaisesRegex(ValueError, 'LANGUAGE_ALREADY_EXISTS'):
            self.compose(page=page)
        page = copy.deepcopy(self.page)
        page['transforms'].append(page['transforms'][0])
        with self.assertRaisesRegex(ValueError, 'CONFLICTING_TRANSFORMS'):
            self.compose(page=page)

    def test_missing_languages_and_unknown_variables_fail(self):
        source = re.sub(r'```rust\n.*?^```\s*', '', self.source, count=1, flags=re.M | re.S)
        with self.assertRaisesRegex(ValueError, 'NAV_CODE_MISMATCH'):
            self.compose(source)
        with self.assertRaisesRegex(ValueError, 'MISSING_VARIABLE'):
            build.bind('{{var.example_token}}', {}, self.values)
        with self.assertRaisesRegex(ValueError, 'UNEXPORTED_VARIABLE'):
            self.compose(self.source + '\n{{var.unknown}}\n')

    def test_cli_is_optional_but_referenced_file_is_required(self):
        page = copy.deepcopy(self.page)
        page['transforms'] = []
        rendered, _, _ = self.compose(page=page)
        self.assertNotIn('value="shell"', rendered)
        self.assertEqual(rendered.count('<TabItem '), 14)
        page = copy.deepcopy(self.page)
        page['transforms'][0]['content']['file'] = 'missing.md'
        with self.assertRaises(FileNotFoundError):
            self.compose(page=page)

    def test_changed_shared_group_changes_dependency_digest(self):
        before = build.scan(self.source)['standard-filtering-code']['digest']
        after = build.scan(self.source.replace('limit=5,', 'limit=6,', 1))['standard-filtering-code']['digest']
        self.assertNotEqual(before, after)

    def with_rules(self, rules, fragments=None, profile=None):
        source = self.source + '\n<!-- doc:block:start id="product-notes" -->\nShared note.\n<!-- doc:block:end id="product-notes" -->\n'
        page = copy.deepcopy(self.page)
        page['transforms'] = rules
        fragments = fragments or {}
        return build.compose(source, page, profile or self.profile, self.values, self.values,
            lambda file: fragments[file] if file in fragments else self.read(file))[0]

    def test_add_markdown_before_and_after_uses_same_operation(self):
        target = {'module': 'filtered-search', 'block': 'product-notes'}
        rules = [{'operation': 'add', 'target': target, 'position': pos, 'content': {'file': name}}
                 for pos, name in [('before', 'a.md'), ('after', 'b.md'), ('after', 'c.md')]]
        result = self.with_rules(rules, {'a.md': 'First.', 'b.md': 'Second.', 'c.md': 'Third.'})
        positions = [result.index(value) for value in ['First.', 'Shared note.', 'Second.', 'Third.']]
        self.assertEqual(positions, sorted(positions))

    def test_replace_and_remove_markdown(self):
        target = {'module': 'filtered-search', 'block': 'product-notes'}
        result = self.with_rules([{'operation': 'replace', 'target': target, 'content': {'file': 'note.md'}}],
                                 {'note.md': 'A {{var.product_name}} note.'})
        self.assertIn('A Zilliz Cloud note.', result)
        self.assertNotIn('Shared note.', result)
        removed = self.with_rules([{'operation': 'remove', 'target': target}])
        self.assertNotIn('Shared note.', removed)

    def test_replace_language_requires_existing_target_and_matching_fence(self):
        target = {'module': 'filtered-search', 'block': 'standard-filtering-code', 'language': 'python'}
        rule = {'operation': 'replace', 'target': target, 'content': {'file': 'example.md'}}
        result = self.with_rules([rule], {'example.md': '```python\nprint("changed")\n```\n'})
        self.assertIn('print("changed")', result)
        with self.assertRaisesRegex(ValueError, 'INVALID_LANGUAGE_FRAGMENT'):
            self.with_rules([rule], {'example.md': '```java\nchanged();\n```\n'})
        rule['target']['language'] = 'shell'
        with self.assertRaisesRegex(ValueError, 'MISSING_LANGUAGE'):
            self.with_rules([rule], {'example.md': '```shell\necho changed\n```\n'})

    def test_remove_language_respects_site_required_languages(self):
        rule = {'operation': 'remove', 'target': {'module': 'filtered-search', 'block': 'standard-filtering-code', 'language': 'c++'}}
        with self.assertRaisesRegex(ValueError, 'LANGUAGE_COVERAGE_MISMATCH'):
            self.with_rules([rule])
        profile = copy.deepcopy(self.profile)
        next(item for item in profile['languages'] if item['value'] == 'c++')['required'] = False
        result = self.with_rules([rule], profile=profile)
        self.assertEqual(result.count('<TabItem value="c++">'), 1)

    def test_remove_whole_group_and_conflicting_child_transform(self):
        rule = {'operation': 'remove', 'target': {'module': 'filtered-search', 'block': 'standard-filtering-code'}}
        result = self.with_rules([rule])
        self.assertEqual(result.count('<Tabs '), 1)
        with self.assertRaisesRegex(ValueError, 'PARENT_CHILD_CONFLICT'):
            self.with_rules([rule, self.page['transforms'][0]])

    def test_invalid_actions_fields_and_arguments_fail(self):
        target = {'module': 'filtered-search', 'block': 'product-notes'}
        cases = [
            ({'operation': 'add_note', 'target': target, 'content': {'file': 'x'}}, 'UNKNOWN_OPERATION'),
            ({'operation': 'add', 'target': target, 'content': {'file': 'x'}}, 'ADD_POSITION_REQUIRED'),
            ({'operation': 'remove', 'target': target, 'content': {'file': 'x'}}, 'REMOVE_HAS_CONTENT'),
            ({'operation': 'replace', 'target': target}, 'CONTENT_FILE_REQUIRED'),
            ({'operation': 'replace', 'target': target, 'content': {'file': 'x'}, 'selector': 'heading'}, 'UNKNOWN_TRANSFORM_FIELD'),
            ({'operation': 'remove', 'target': {**target, 'module': 'other'}}, 'TARGET_OUTSIDE_SOURCE'),
        ]
        for rule, error in cases:
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                self.with_rules([rule], {'x': 'Text.'})

    def test_new_fragments_are_not_targets_for_later_rules(self):
        rules = copy.deepcopy(self.page['transforms'])
        rules.append({'operation': 'remove', 'target': dict(rules[0]['target'])})
        with self.assertRaisesRegex(ValueError, 'MISSING_LANGUAGE'):
            self.with_rules(rules)

    def test_schema_version_and_unknown_fields_fail_explicitly(self):
        for version in [None, 0, 2, 3, '1']:
            page = copy.deepcopy(self.page)
            page['schema_version'] = version
            with self.subTest(version=version), self.assertRaisesRegex(ValueError, 'UNSUPPORTED_SCHEMA_VERSION'):
                self.compose(page=page)
        page = copy.deepcopy(self.page)
        page['unexpected_field'] = []
        with self.assertRaisesRegex(ValueError, 'UNKNOWN_PAGE_FIELD'):
            self.compose(page=page)

    def test_registry_requires_supported_schema(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = (Path(temp) / 'fixture').resolve()
            shutil.copytree(build.ROOT, fixture)
            reg = fixture / 'zdoc/shared/modules.yaml'
            reg.write_text(reg.read_text().replace('schema_version: 1', 'schema_version: 2'))
            with patch.object(build, 'ROOT', fixture), self.assertRaisesRegex(ValueError, 'UNSUPPORTED_SCHEMA_VERSION'):
                build.products()

    def test_manual_generated_change_fails_check(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = (Path(temp) / 'fixture').resolve()
            shutil.copytree(build.ROOT, fixture)
            with patch.object(build, 'ROOT', fixture):
                build.run()
                output = fixture / 'generated/filtered-search.mdx'
                output.write_text(output.read_text() + '\nManual change\n')
                with self.assertRaisesRegex(ValueError, 'GENERATED_OUTPUT_DIFFERS'):
                    build.run(check=True)


if __name__ == '__main__':
    unittest.main()
