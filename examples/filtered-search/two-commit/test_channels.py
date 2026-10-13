"""Two-commit channel checks: each channel sees exactly its own build; no zdoc rendering."""
from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import yaml

import build_channels as channels

base = channels.base
NEXT = 'two-commit/milvus-docs-next'
SOURCE = 'site/en/userGuide/search-query-get/filtered-search.md'


def page(body, title='T'):
    return f'---\ntitle: {title}\n---\n\nimport Tabs from "@theme/Tabs";\n\n{body}'


class TwoCommitChecks(unittest.TestCase):
    def setUp(self):
        self.lock = yaml.safe_load((channels.HERE / 'lock.yaml').read_text())
        self.current = base.products()['filtered-search.mdx']
        self.next = base.products(milvus_root=NEXT)['filtered-search.mdx']
        self.mdx, self.pairs, self.warnings = channels.compose_channels(self.current, self.next)

    @contextmanager
    def fixture(self):
        """A writable copy of the example; yields (root, lock path)."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve() / 'filtered-search'
            shutil.copytree(base.ROOT, root, ignore=shutil.ignore_patterns('__pycache__'))
            with patch.object(base, 'ROOT', root):
                yield root, root / 'two-commit/lock.yaml'

    def edit(self, path, old, new, count=1):
        """Replace the first `count` occurrences; the standard-filtering group precedes the iterative one."""
        text = path.read_text()
        self.assertGreaterEqual(text.count(old), count, old)
        path.write_text(text.replace(old, new, count))

    def test_generated_files_are_fresh(self):
        for name, text in channels.products().items():
            self.assertEqual((channels.HERE / 'generated' / name).read_text(), text, name)

    def test_each_channel_sees_exactly_its_own_build(self):
        for name, built in (('current', self.current), ('next', self.next)):
            header, body = channels.split_page(built)
            self.assertTrue(self.mdx.startswith(header))
            self.assertEqual(channels.split_blocks(channels.view(self.mdx, name)[len(header):]),
                             channels.split_blocks(body), name)

    def test_four_small_edits_become_four_pairs(self):
        shape = [(p['change'], [b['kind'] for b in p['current']], [b['kind'] for b in p['next']]) for p in self.pairs]
        self.assertEqual(shape, [('changed', ['paragraph'], ['paragraph']), ('changed', ['list'], ['list']),
                                 ('changed', ['paragraph'], ['paragraph']),
                                 ('changed', ['paragraph'], ['paragraph', 'paragraph'])])
        self.assertIn('assume  you', self.pairs[2]['current'][0]['text'])
        self.assertEqual(self.warnings, [])

    def test_unchanged_code_groups_and_cloud_cli_appear_once(self):
        self.assertEqual(self.mdx.count('<Tabs '), 2)
        self.assertEqual(self.mdx.count('<TabItem value="shell">'), 2)
        for wrapped in channels.WRAPPED.finditer(self.mdx):
            self.assertNotIn('<Tabs', wrapped[2])

    def test_same_commit_has_no_channel_markup(self):
        lock = {**self.lock, 'channels': {**self.lock['channels'], 'next': dict(self.lock['channels']['current'])}}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'lock.yaml'
            path.write_text(yaml.safe_dump(lock))
            result = channels.products(path)
        self.assertEqual(result['filtered-search.mdx'], self.current)
        self.assertNotIn('NextChannel', result['filtered-search.mdx'])

    def test_promotion_moves_prod_to_next_and_clears_every_pair(self):
        promoted = channels.promote(self.lock)
        self.assertEqual(self.lock['channels']['current']['commit'], 'fixture-current')
        self.assertEqual(promoted['channels']['current'], promoted['channels']['next'])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'lock.yaml'
            path.write_text(yaml.safe_dump(promoted))
            result = channels.products(path)
        self.assertEqual(result['filtered-search.mdx'], self.next)

    def test_added_and_removed_blocks_wrap_one_side_only(self):
        mdx, pairs, _ = channels.compose_channels(page('# A\n\nKeep.\n\nOld note.\n'), page('# A\n\nKeep.\n\nNew X.\n\nNew Y.\n'))
        self.assertEqual(pairs[0]['change'], 'changed')
        mdx, pairs, _ = channels.compose_channels(page('# A\n\nKeep.\n\nGone.\n'), page('# A\n\nKeep.\n'))
        self.assertEqual([p['change'] for p in pairs], ['removed'])
        self.assertIn('<NextChannel action="exclude">\n\nGone.\n\n</NextChannel>', mdx)
        self.assertNotIn('action="include"', mdx)
        mdx, pairs, _ = channels.compose_channels(page('# A\n\nKeep.\n'), page('# A\n\nNew.\n\nKeep.\n'))
        self.assertEqual([p['change'] for p in pairs], ['added'])
        self.assertIn('<NextChannel action="include">\n\nNew.\n\n</NextChannel>\n\nKeep.', mdx)

    def test_changed_code_group_is_one_pair_with_cloud_cli_on_both_sides(self):
        with self.fixture() as (root, lock):
            self.edit(root / NEXT / SOURCE, '    .topK(5)\n', '    .topK(10)\n')
            result = channels.products(lock)
            receipt = yaml.safe_load(result['channel-receipt.json'])
        groups = [p for p in receipt['pairs'] if p['current'][0]['kind'] == 'code-group']
        self.assertEqual(len(groups), 1)
        self.assertEqual([b['kind'] for b in groups[0]['next']], ['code-group'])
        mdx = result['filtered-search.mdx']
        for name, limit in (('current', '.topK(5)'), ('next', '.topK(10)')):
            shown = channels.view(mdx, name)
            self.assertEqual(shown.count('<TabItem value="shell">'), 2)
            self.assertIn(limit, shown)

    def test_upstream_change_hidden_by_a_cloud_replace_creates_no_pair(self):
        pairs = lambda lock: yaml.safe_load(channels.products(lock)['channel-receipt.json'])['pairs']
        with self.fixture() as (root, lock):
            self.edit(root / NEXT / SOURCE, '    limit=5,\n    # highlight-start\n', '    limit=10,\n    # highlight-start\n')
            self.assertEqual(len(pairs(lock)), 5)
            page_dir = root / base.PAGE
            config = yaml.safe_load((page_dir / 'page.yaml').read_text())
            config['transforms'].append({'operation': 'replace', 'content': {'file': 'cloud-python.md'},
                                         'target': {'module': 'filtered-search', 'block': 'standard-filtering-code',
                                                    'language': 'python'}})
            (page_dir / 'page.yaml').write_text(yaml.safe_dump(config, sort_keys=False))
            (page_dir / 'cloud-python.md').write_text('```python\nprint("cloud")\n```\n')
            self.assertEqual(len(pairs(lock)), 4)

    def test_cloud_rule_failing_on_one_channel_names_it(self):
        with self.fixture() as (root, lock):
            self.edit(root / NEXT / SOURCE, 'id="standard-filtering-code" -->\n<div', 'id="standard-search-code" -->\n<div')
            self.edit(root / NEXT / SOURCE, 'end id="standard-filtering-code"', 'end id="standard-search-code"')
            with self.assertRaisesRegex(ValueError, '^next:MISSING_BLOCK:standard-filtering-code$'):
                channels.products(lock)

    def test_changed_heading_is_reported(self):
        _, pairs, warnings = channels.compose_channels(page('## Setup\n\nText.\n'), page('## Set up\n\nText.\n'))
        self.assertEqual(warnings, [{'code': 'HEADING_DIFFERS_BY_CHANNEL', 'headings': ['## Setup', '## Set up']}])

    def test_metadata_follows_current(self):
        mdx, _, warnings = channels.compose_channels(page('Text.\n', 'Old'), page('Text.\n', 'New'))
        self.assertTrue(mdx.startswith('---\ntitle: Old\n'))
        self.assertEqual(warnings[0]['code'], 'METADATA_FOLLOWS_CURRENT')

    def test_hand_written_channel_markup_is_kept_but_never_nested(self):
        own = '<NextChannel action="include">\n\nCloud only.\n\n</NextChannel>'
        mdx, pairs, _ = channels.compose_channels(page(f'{own}\n\nA.\n'), page(f'{own}\n\nB.\n'))
        self.assertEqual(mdx.count(own), 1)
        with self.assertRaisesRegex(ValueError, 'NESTED_CHANNEL'):
            channels.compose_channels(page(f'{own}\n\nA.\n'), page('A.\n'))

    def test_unclosed_container_fails(self):
        with self.assertRaisesRegex(ValueError, 'UNCLOSED_CONTAINER'):
            channels.split_blocks('<Admonition type="info">\n\nText.\n')

    def test_invalid_locks_fail(self):
        cases = {
            'LOCK_NEEDS_CURRENT_AND_NEXT': {'current': self.lock['channels']['current']},
            'INVALID_LOCK_CHANNEL:next': {**self.lock['channels'], 'next': {'commit': 'x'}},
            'SNAPSHOT_OUTSIDE_FIXTURE:next': {**self.lock['channels'], 'next': {'commit': 'x', 'snapshot': '../..'}},
            'SAME_COMMIT_DIFFERENT_SNAPSHOT': {**self.lock['channels'],
                                               'next': {'commit': 'fixture-current', 'snapshot': NEXT}},
        }
        for code, value in cases.items():
            with self.subTest(code), self.assertRaisesRegex(ValueError, code):
                channels.load_lock({**self.lock, 'channels': value})
        with self.assertRaisesRegex(ValueError, 'INVALID_LOCK'):
            channels.load_lock({**self.lock, 'extra': 1})


if __name__ == '__main__':
    unittest.main()
