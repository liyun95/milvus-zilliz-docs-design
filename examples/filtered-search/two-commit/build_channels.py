"""Bounded offline illustration of two-commit release channels.

Builds the Cloud page once per locked snapshot with the existing builder, compares the
two results block by block, and writes one MDX in which only differing blocks are wrapped
in <NextChannel>. No upstream fetch, promotion PR or zdoc rendering. The block splitter
covers this fixture's headings, paragraphs, lists, fences, Tabs and Admonitions only.
"""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import re
import sys
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_example as base  # noqa: E402

CHANNELS = ('current', 'next')
CONTAINERS = (('```', re.compile(r'^```[ \t]*$')), ('<Tabs', re.compile(r'^</Tabs>$')),
              ('<Admonition', re.compile(r'^</Admonition>$')), ('<NextChannel', re.compile(r'^</NextChannel>$')))
LIST_ITEM = re.compile(r'^[ \t]*(?:[-*+]|\d+\.)[ \t]')
WRAPPED = re.compile(r'<NextChannel action="(include|exclude)">\n\n(.*?)\n\n</NextChannel>', re.S)


def sha(text):
    return 'sha256:' + hashlib.sha256(text.encode()).hexdigest()


def load_lock(lock):
    if lock.get('schema_version') != 1 or set(lock) != {'schema_version', 'page', 'channels'}:
        raise ValueError('INVALID_LOCK')
    channels = lock['channels']
    if not isinstance(channels, dict) or set(channels) != set(CHANNELS):
        raise ValueError('LOCK_NEEDS_CURRENT_AND_NEXT')
    for name in CHANNELS:
        entry = channels[name]
        if not isinstance(entry, dict) or set(entry) != {'commit', 'snapshot'} or \
                not all(isinstance(entry[key], str) and entry[key] for key in entry):
            raise ValueError('INVALID_LOCK_CHANNEL:' + name)
        path = (base.ROOT / entry['snapshot']).resolve()
        if not path.is_relative_to(base.ROOT.resolve()) or not path.is_dir():
            raise ValueError('SNAPSHOT_OUTSIDE_FIXTURE:' + name)
    if channels['current']['commit'] == channels['next']['commit'] and \
            channels['current']['snapshot'] != channels['next']['snapshot']:
        raise ValueError('SAME_COMMIT_DIFFERENT_SNAPSHOT')
    return channels


def promote(lock):
    """Cloud release: Prod adopts what UAT has been showing. Returns a new lock."""
    return {**lock, 'channels': {**lock['channels'], 'current': dict(lock['channels']['next'])}}


def build_channel(name, snapshot):
    """Every Cloud rule must hold on each locked commit; errors name the failing channel."""
    try:
        return base.products(milvus_root=snapshot)['filtered-search.mdx']
    except ValueError as error:
        raise ValueError(f'{name}:{error}') from error


def split_page(mdx):
    match = re.match(r'(---\n.*?\n---\n\n(?:import [^\n]*\n)*\n)', mdx, re.S)
    if not match:
        raise ValueError('UNEXPECTED_PAGE_HEADER')
    return match[1], mdx[match.end():]


def split_blocks(body):
    """Top-level blocks: a container or a list is one block; anything else ends at a blank line."""
    lines, blocks, i = body.split('\n'), [], 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        start = i
        closer = next((end for opener, end in CONTAINERS if lines[i].startswith(opener)), None)
        if closer:
            i += 1
            while i < len(lines) and not closer.match(lines[i]):
                i += 1
            if i == len(lines):
                raise ValueError('UNCLOSED_CONTAINER:' + lines[start][:40])
            i += 1
        elif LIST_ITEM.match(lines[i]):
            while i < len(lines) and (lines[i].strip() or (
                    i + 1 < len(lines) and (LIST_ITEM.match(lines[i + 1]) or lines[i + 1].startswith((' ', '\t'))))):
                i += 1
        else:
            while i < len(lines) and lines[i].strip():
                i += 1
        blocks.append('\n'.join(lines[start:i]))
    return blocks


def join_blocks(blocks, tail='\n'):
    return '\n\n'.join(blocks) + tail


def wrap(action, blocks):
    return f'<NextChannel action="{action}">\n\n' + '\n\n'.join(blocks) + '\n\n</NextChannel>'


def describe(block):
    kind = ('heading' if block.startswith('#') else 'code-group' if block.startswith('<Tabs') else
            'code' if block.startswith('```') else 'admonition' if block.startswith('<Admonition') else
            'list' if LIST_ITEM.match(block) else 'paragraph')
    return {'kind': kind, 'text': block} if kind in ('heading', 'list', 'paragraph') else \
        {'kind': kind, 'first_line': block.split('\n', 1)[0][:60], 'digest': sha(block)}


def merge(current_blocks, next_blocks):
    """Equal runs appear once; each differing run becomes an exclude/include pair."""
    matcher = difflib.SequenceMatcher(None, current_blocks, next_blocks, autojunk=False)
    parts, pairs, warnings = [], [], []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            parts.extend(current_blocks[i1:i2])
            continue
        old, new = current_blocks[i1:i2], next_blocks[j1:j2]
        if any(block.startswith('<NextChannel') for block in old + new):
            raise ValueError('NESTED_CHANNEL')
        parts.extend(([wrap('exclude', old)] if old else []) + ([wrap('include', new)] if new else []))
        pairs.append({'change': {'replace': 'changed', 'delete': 'removed', 'insert': 'added'}[tag],
                      'current': [describe(b) for b in old], 'next': [describe(b) for b in new]})
        headings = [b.split('\n', 1)[0] for b in old + new if b.startswith('#')]
        if headings:
            warnings.append({'code': 'HEADING_DIFFERS_BY_CHANNEL', 'headings': headings})
    return parts, pairs, warnings


def view(mdx, channel):
    """What the NextChannel component shows on one channel (used to verify the merge)."""
    keep = 'include' if channel == 'next' else 'exclude'
    return WRAPPED.sub(lambda m: m[2] if m[1] == keep else '', mdx)


def compose_channels(current_mdx, next_mdx):
    header, current_body = split_page(current_mdx)
    next_header, next_body = split_page(next_mdx)
    parts, pairs, warnings = merge(split_blocks(current_body), split_blocks(next_body))
    if next_header != header:
        # Front matter cannot be split by channel; Prod's metadata stays until promotion.
        warnings.append({'code': 'METADATA_FOLLOWS_CURRENT', 'next_header_digest': sha(next_header)})
    tail = current_body[len(current_body.rstrip('\n')):]
    return header + join_blocks(parts, tail), pairs, warnings


def products(lock_path=HERE / 'lock.yaml'):
    lock = yaml.safe_load(Path(lock_path).read_text())
    channels = load_lock(lock)
    built = {name: build_channel(name, channels[name]['snapshot']) for name in CHANNELS}
    mdx, pairs, warnings = compose_channels(built['current'], built['next'])
    receipt = {'status': 'local-demo-not-a-release-authorization',
               'channels': {name: {'commit': channels[name]['commit'], 'cloud_output_digest': sha(built[name])}
                            for name in CHANNELS},
               'builder_digest': sha(Path(__file__).read_text() + Path(base.__file__).read_text()),
               'pairs': pairs, 'warnings': warnings, 'output_digest': sha(mdx)}
    return {'filtered-search.mdx': mdx, 'channel-receipt.json': json.dumps(receipt, indent=2, ensure_ascii=False) + '\n'}


def run(check=False):
    output = HERE / 'generated'
    results = products()
    if check:
        for name, text in results.items():
            if not (output / name).exists() or (output / name).read_text() != text:
                raise ValueError('GENERATED_OUTPUT_DIFFERS:' + name)
        print('Fresh two-commit composition matches all generated files.')
    else:
        output.mkdir(exist_ok=True)
        for name, text in results.items():
            (output / name).write_text(text)
        receipt = json.loads(results['channel-receipt.json'])
        print(f"{len(receipt['pairs'])} channel pairs, {len(receipt['warnings'])} warnings.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    run(parser.parse_args().check)
