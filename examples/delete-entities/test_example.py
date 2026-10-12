"""Content preservation and failure-mode checks for the local illustration."""
import ast
import copy
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

import build_example as build


class ExampleChecks(unittest.TestCase):
    def setUp(self):
        self.page = build.read_yaml(build.ROOT / 'zdoc/delete-entities.page.yaml')
        self.source = (build.ROOT / 'milvus-docs/site/en/userGuide/insert-and-delete/delete-entities.md').read_text()
        self.profile = build.read_yaml(build.ROOT / 'zdoc/presentation/cloud-sdk-tabs.yaml')
        self.read = lambda p: (build.ROOT / 'zdoc' / p).read_text()

    def test_preserves_all_cloud_code_with_only_declared_go_auth_fix(self):
        original = (build.ROOT / 'evidence/cloud.original.md').read_text()
        generated = build.products()['delete-entities.mdx']
        baseline = re.findall(r'<Tabs\b[^\n]*>\n(.*?)</Tabs>', original, re.S)
        result = re.findall(r'<Tabs\b[^\n]*>\n(.*?)</Tabs>', generated, re.S)
        self.assertEqual((len(baseline), len(result)), (3, 3))
        for group_id, (a, b) in enumerate(zip(baseline, result)):
            expected, actual = dict(build.FENCE.findall(a)), dict(build.FENCE.findall(b))
            self.assertEqual(len(actual), 7)
            if group_id == 0:
                expected['go'] = expected['go'].replace('    Address: milvusAddr,\n',
                    '    Address: milvusAddr,\n    APIKey: "YOUR_CLUSTER_TOKEN",\n')
            normalize = lambda code: '\n'.join(line.rstrip() for line in code.splitlines() if line.strip())
            self.assertEqual({k: normalize(v) for k, v in expected.items()},
                             {k: normalize(v) for k, v in actual.items()})

    def test_preserves_cloud_prose_and_heading_order(self):
        def prose(text):
            text = text.split('# Delete Entities', 1)[1]
            text = re.sub(r'<Tabs\b.*?</Tabs>', '', text, flags=re.S)
            text = re.sub(r'\\?\{#[^}]+\}', '', text)
            return ' '.join(text.split())
        self.assertEqual(prose((build.ROOT / 'evidence/cloud.original.md').read_text()),
                         prose(build.products()['delete-entities.mdx']))

    def test_generated_code_has_no_source_markers_or_local_credentials(self):
        result = build.products()['delete-entities.mdx']
        for token in ['doc:block:', 'multipleCode', 'localhost', 'root:Milvus']:
            self.assertNotIn(token, result)
        self.assertEqual(result.count('<TabItem value='), 21)
        for lang, code in build.FENCE.findall(result):
            if lang == 'python':
                ast.parse(code)

    def test_variable_binding_preserves_rust_indentation(self):
        result = build.products()['delete-entities.mdx']
        code = next(code for lang, code in build.FENCE.findall(result) if lang == 'rust')
        self.assertIn('\n    let config = ', code)
        self.assertIn('\n    let client = ', code)
        self.assertIn('\n    let request = ', code)
        self.assertTrue(code.rstrip().endswith('}'))

    def test_preserves_approved_cloud_output(self):
        self.assertEqual((build.ROOT / 'evidence/cloud.expected.mdx').read_text(),
                         build.products()['delete-entities.mdx'])

    def test_whole_page_needs_no_blocks_or_fragments(self):
        self.assertNotIn('doc:block:', self.source)
        self.assertNotIn('transforms', self.page)
        self.assertEqual(list((build.ROOT / 'zdoc/fragments').glob('**/*.md')), [])
        self.assertEqual(json.loads(build.products()['registry.json'])['modules']['delete-entities']['blocks'], {})

    def test_missing_or_unexported_variable_fails(self):
        for values, exports, error in [({}, ['x'], 'MISSING_VARIABLE'), ({'x': 'value'}, [], 'UNEXPORTED_VARIABLE')]:
            with self.assertRaisesRegex(ValueError, error):
                build.bind_variables('{{var.x}}', values, exports)

    def test_empty_scalar_is_preserved_and_code_injection_rejected(self):
        self.assertEqual(build.bind_variables('APIKey: "{{var.x}}"', {'x': ''}, ['x']), 'APIKey: ""')
        for value in ['"; unexpected()', 'a\nb', '${COMMAND}', '{{var.x}}', None]:
            with self.assertRaisesRegex(ValueError, 'UNSAFE_EXAMPLE_VALUE'):
                build.bind_variables('{{var.x}}', {'x': value}, ['x'])

    def test_group_language_missing_fails_instead_of_creating_placeholder(self):
        source = re.sub(r'```rust\n.*?^```\s*', '', self.source, count=1, flags=re.M | re.S)
        with self.assertRaisesRegex(ValueError, 'NAV_CODE_MISMATCH'):
            build.render_groups(source, self.profile)
        profile = copy.deepcopy(self.profile)
        profile['languages'].append({'label': 'Ruby', 'value': 'ruby', 'required': True})
        with self.assertRaisesRegex(ValueError, 'LANGUAGE_COVERAGE_MISMATCH'):
            build.render_groups(self.source, profile)

    def test_both_products_bind_every_variable(self):
        result = build.products()
        cloud, milvus = result['delete-entities.mdx'], result['milvus-delete-entities.md']
        self.assertNotIn('{{var.', cloud)
        self.assertNotIn('{{var.', milvus)
        self.assertNotIn('YOUR_CLUSTER_', milvus)
        go = next(code for lang, code in build.FENCE.findall(milvus) if lang == 'go')
        self.assertIn('APIKey: "root:Milvus"', go)
        self.assertNotIn('example_go_token', self.source)
        self.assertIn('milvusAddr := "http://localhost:19530"', go)
        self.assertEqual(cloud.count('export TOKEN="YOUR_CLUSTER_TOKEN"'), 3)
        self.assertEqual(milvus.count('export TOKEN="root:Milvus"'), 3)
        for lang, code in build.FENCE.findall(milvus):
            if lang == 'python':
                ast.parse(code)

    def test_schema_contract_rejects_unsupported_inputs(self):
        build.validate_page(self.page)
        for version in [None, 0, 2, 3, '1']:
            page = copy.deepcopy(self.page)
            page['schema_version'] = version
            with self.subTest(version=version), self.assertRaisesRegex(ValueError, 'UNSUPPORTED_SCHEMA_VERSION'):
                build.validate_page(page)
        for field in ['unexpected_field']:
            page = copy.deepcopy(self.page)
            page[field] = []
            with self.assertRaisesRegex(ValueError, 'UNKNOWN_PAGE_FIELD'):
                build.validate_page(page)
        page = copy.deepcopy(self.page)
        page['transforms'] = [{'operation': 'add'}]
        with self.assertRaisesRegex(ValueError, 'TRANSFORMS_NOT_SUPPORTED_BY_THIS_DEMO'):
            build.validate_page(page)

    def test_optional_cli_omitted_or_rendered_from_same_profile(self):
        rendered, groups = build.render_groups(self.source, self.profile)
        self.assertNotIn('value="shell"', rendered)
        self.assertTrue(all(len(group) == 7 for group in groups))
        source = '<div class="multipleCode">\n<a href="#shell">Zilliz CLI</a>\n</div>\n```shell\necho test\n```\n'
        profile = copy.deepcopy(self.profile)
        for item in profile['languages']:
            item['required'] = False
        profile['default'] = 'shell'
        rendered, groups = build.render_groups(source, profile)
        self.assertEqual(groups, [['shell']])
        self.assertIn('<TabItem value="shell">', rendered)
        self.assertNotIn('required', rendered)
        profile['default'] = 'python'
        with self.assertRaisesRegex(ValueError, 'LANGUAGE_COVERAGE_MISMATCH'):
            build.render_groups(source, profile)

    def test_registry_requires_supported_schema(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = (Path(temp) / 'fixture').resolve()
            shutil.copytree(build.ROOT, fixture)
            reg = fixture / 'zdoc/shared/modules.yaml'
            reg.write_text(reg.read_text().replace('schema_version: 1', 'schema_version: 2'))
            with patch.object(build, 'ROOT', fixture), self.assertRaisesRegex(ValueError, 'UNSUPPORTED_SCHEMA_VERSION'):
                build.products()

    def test_generated_manual_edit_fails_check(self):
        # Use an isolated copy, never alter the displayed generated document.
        with tempfile.TemporaryDirectory() as temp:
            fixture = (Path(temp) / 'fixture').resolve()
            shutil.copytree(build.ROOT, fixture)
            with patch.object(build, 'ROOT', fixture):
                build.run()
                output = fixture / 'generated/delete-entities.mdx'
                output.write_text(output.read_text() + '\nManual modification\n')
                with self.assertRaisesRegex(ValueError, 'GENERATED_OUTPUT_DIFFERS'):
                    build.run(check=True)


if __name__ == '__main__':
    unittest.main()
