"""Bounded offline illustration of whole-page consumption and schema v1 transforms.

No upstream fetch, approval, publish or actual md2md execution. Supports this
fixture's flat named Markdown/code groups and Markdown fences, not arbitrary Markdown.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import yaml

ROOT = Path(__file__).resolve().parent
FENCE = re.compile(r'^```([^\n]+)\n(.*?)^```[ \t]*(?:\n|$)', re.M | re.S)
VAR = re.compile(r'{{var\.([a-z][a-z0-9_]*)}}')
START = re.compile(r'^<!-- doc:block:start id="([a-z][a-z0-9-]*)" -->\n', re.M)
END = re.compile(r'^<!-- doc:block:end id="([a-z][a-z0-9-]*)" -->[ \t]*(?:\n|$)', re.M)
NAV = re.compile(r'<div class="multipleCode">\n(.*?)</div>\s*', re.S)


def sha(text):
    return 'sha256:' + hashlib.sha256(text.encode()).hexdigest()


def bind(text, values, exports):
    used = set(VAR.findall(text))
    if used - set(exports):
        raise ValueError('UNEXPORTED_VARIABLE')
    if used - values.keys():
        raise ValueError('MISSING_VARIABLE')
    for key in used:
        pattern = r'[A-Za-z0-9 ._-]+' if key == 'product_name' else r'[A-Za-z0-9_:/.-]+'
        if not isinstance(values[key], str) or not re.fullmatch(pattern, values[key]):
            raise ValueError('UNSAFE_EXAMPLE_VALUE:' + key)
    result = VAR.sub(lambda m: values[m[1]], text)
    if '{{var.' in result:
        raise ValueError('UNRESOLVED_VARIABLE')
    return result


def code_group(content):
    nav = NAV.match(content)
    if not nav:
        raise ValueError('EXPECTED_CODE_GROUP')
    pos, codes = nav.end(), {}
    while pos < len(content):
        fence = FENCE.match(content, pos)
        if not fence:
            raise ValueError('UNEXPECTED_GROUP_CONTENT')
        lang, code = fence.groups()
        if lang in codes:
            raise ValueError('DUPLICATE_LANGUAGE:' + lang)
        codes[lang] = code.rstrip('\n')
        pos = fence.end()
        while pos < len(content) and content[pos].isspace():
            pos += 1
    declared = re.findall(r'<a href="#([^"]+)">[^<]+</a>', nav[1])
    if declared != list(codes):
        raise ValueError('NAV_CODE_MISMATCH')
    return codes


def scan(source):
    blocks, active = {}, None
    events = sorted([(m.start(), 'start', m) for m in START.finditer(source)] +
                    [(m.start(), 'end', m) for m in END.finditer(source)])
    fenced = [(m.start(), m.end()) for m in FENCE.finditer(source)]
    if source.count('doc:block:') != len(events):
        raise ValueError('MALFORMED_MARKER')
    for pos, kind, match in events:
        if any(a <= pos < b for a, b in fenced):
            raise ValueError('MARKER_INSIDE_CODE')
        bid = match[1]
        if kind == 'start':
            if active or bid in blocks:
                raise ValueError('DUPLICATE_OR_NESTED_BLOCK')
            active = match
        else:
            if active is None or active[1] != bid:
                raise ValueError('UNBALANCED_BLOCK')
            content = source[active.end():pos]
            if not content.strip():
                raise ValueError('EMPTY_BLOCK')
            kind = 'code-group' if NAV.match(content) else 'markdown'
            codes = code_group(content) if kind == 'code-group' else {}
            blocks[bid] = {'start': active.start(), 'end': match.end(), 'content': content,
                           'kind': kind, 'codes': codes, 'digest': sha(content)}
            active = None
    if active:
        raise ValueError('UNCLOSED_BLOCK')
    return blocks


def render_tabs(codes, profile):
    policy = profile['languages']
    known = [item['value'] for item in policy]
    required = {item['value'] for item in policy if item.get('required')}
    if len(known) != len(set(known)) or profile['default'] not in codes:
        raise ValueError('INVALID_PROFILE')
    if set(codes) - set(known) or required - set(codes):
        raise ValueError('LANGUAGE_COVERAGE_MISMATCH')
    values = [{'label': item['label'], 'value': item['value']} for item in policy if item['value'] in codes]
    output = f'<Tabs groupId="{profile["group_id"]}" defaultValue="{profile["default"]}" values={{{json.dumps(values, separators=(",", ":"))}}}>\n'
    for item in values:
        lang = item['value']
        output += f'<TabItem value="{lang}">\n\n```{lang}\n{codes[lang]}\n```\n\n</TabItem>\n'
    return output + '</Tabs>\n'


def transform_rules(page, blocks):
    if page.get('schema_version') != 1:
        raise ValueError('UNSUPPORTED_SCHEMA_VERSION')
    if set(page) - {'schema_version', 'page', 'source', 'variables', 'presentation', 'metadata', 'links', 'assets', 'transforms'}:
        raise ValueError('UNKNOWN_PAGE_FIELD')
    seen, by_block = set(), {}
    rules = page.get('transforms', [])
    if not isinstance(rules, list):
        raise ValueError('TRANSFORMS_MUST_BE_LIST')
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) - {'operation', 'target', 'position', 'content'}:
            raise ValueError('UNKNOWN_TRANSFORM_FIELD')
        op = rule.get('operation')
        if op not in ('add', 'replace', 'remove'):
            raise ValueError('UNKNOWN_OPERATION')
        target = rule.get('target')
        if not isinstance(target, dict) or set(target) - {'module', 'block', 'language'} or not {'module', 'block'} <= set(target):
            raise ValueError('INVALID_TARGET')
        if target['module'] != page['source']['module']:
            raise ValueError('TARGET_OUTSIDE_SOURCE')
        bid, language = target['block'], target.get('language')
        if bid not in blocks:
            raise ValueError('MISSING_BLOCK:' + bid)
        if 'language' in target and (not isinstance(language, str) or not language):
            raise ValueError('INVALID_LANGUAGE')
        block = blocks[bid]
        if op == 'remove':
            if 'content' in rule or 'position' in rule:
                raise ValueError('REMOVE_HAS_CONTENT_OR_POSITION')
        elif not isinstance(rule.get('content'), dict) or set(rule['content']) != {'file'} or not isinstance(rule['content']['file'], str):
            raise ValueError('CONTENT_FILE_REQUIRED')
        if op == 'add' and language is None:
            if rule.get('position') not in ('before', 'after'):
                raise ValueError('ADD_POSITION_REQUIRED')
        elif 'position' in rule:
            raise ValueError('UNEXPECTED_POSITION')
        if language is not None:
            if block['kind'] != 'code-group':
                raise ValueError('LANGUAGE_TARGET_NOT_CODE_GROUP')
            exists = language in block['codes']
            if op == 'add' and exists:
                raise ValueError('LANGUAGE_ALREADY_EXISTS')
            if op != 'add' and not exists:
                raise ValueError('MISSING_LANGUAGE')
        identity = (bid, language)
        # Multiple before/after insertions are allowed in configuration order.
        if not (op == 'add' and language is None):
            if identity in seen:
                raise ValueError('CONFLICTING_TRANSFORMS')
            seen.add(identity)
        by_block.setdefault(bid, []).append(rule)
    for bid, entries in by_block.items():
        destructive = [r for r in entries if 'language' not in r['target'] and r['operation'] in ('replace', 'remove')]
        if destructive and len(entries) > 1:
            raise ValueError('PARENT_CHILD_CONFLICT')
    return rules


def compose(source, page, profile, values, exports, read_fragment):
    blocks = scan(source)
    rules = transform_rules(page, blocks)
    states = {bid: {'kind': block['kind'], 'codes': dict(block['codes']), 'body': block['content'],
                    'before': [], 'after': [], 'removed': False} for bid, block in blocks.items()}
    consumed = []
    for rule in rules:
        target = rule['target']
        bid, lang, op = target['block'], target.get('language'), rule['operation']
        state = states[bid]
        fragment = None
        if op != 'remove':
            fragment = read_fragment(rule['content']['file'])
            if not fragment.strip() or 'doc:block:' in fragment or '<Tabs' in fragment or '<TabItem' in fragment:
                raise ValueError('INVALID_FRAGMENT')
        if lang is not None:
            if op == 'remove':
                del state['codes'][lang]
            else:
                fence = FENCE.fullmatch(fragment.strip() + '\n')
                if not fence or fence[1] != lang or '```' in fence[2] or not fence[2].strip():
                    raise ValueError('INVALID_LANGUAGE_FRAGMENT')
                state['codes'][lang] = fence[2].rstrip('\n')
        elif op == 'add':
            if 'multipleCode' in fragment:
                raise ValueError('INSERTED_CODE_GROUP_NOT_SUPPORTED')
            state[rule['position']].append(fragment.strip() + '\n\n')
        elif op == 'remove':
            state['removed'] = True
        else:
            state['kind'] = 'code-group' if NAV.match(fragment) else 'markdown'
            state['body'] = fragment
            state['codes'] = code_group(fragment) if state['kind'] == 'code-group' else {}
        consumed.append({'operation': op, 'target': target,
                         **({'position': rule['position']} if 'position' in rule else {}),
                         **({'file': rule['content']['file'], 'fragment_digest': sha(fragment)} if fragment is not None else {}),
                         'source_block_digest': blocks[bid]['digest']})
    result = source
    for bid, block in sorted(blocks.items(), key=lambda item: item[1]['start'], reverse=True):
        state = states[bid]
        if state['removed']:
            content = ''
        elif state['kind'] == 'code-group':
            content = render_tabs(state['codes'], profile)
        else:
            content = state['body'].strip() + '\n'
        replacement = ''.join(state['before']) + content + ''.join(state['after'])
        result = result[:block['start']] + replacement + result[block['end']:]
    result = bind(result, values, exports)
    if 'multipleCode' in result or 'doc:block:' in result:
        raise ValueError('UNCONSUMED_CODE_GROUP')
    return result, blocks, consumed


def split_frontmatter(text):
    header, body = text[4:].split('\n---\n', 1)
    return yaml.safe_load(header), body.lstrip('\n')


def products():
    inputs = {}

    def read(path):
        path = path.resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError('PATH_OUTSIDE_FIXTURE')
        text = path.read_text()
        inputs[str(path.relative_to(ROOT))] = sha(text)
        return text

    reg = yaml.safe_load(read(ROOT / 'zdoc/shared/modules.yaml'))
    if reg.get('schema_version') != 1:
        raise ValueError('UNSUPPORTED_SCHEMA_VERSION')
    page = yaml.safe_load(read(ROOT / 'zdoc/filtered-search.page.yaml'))
    if page['source'] != {'take': 'page', 'module': 'filtered-search'}:
        raise ValueError('UNSUPPORTED_SOURCE')
    module = reg['modules']['filtered-search']
    source = read(ROOT / 'milvus-docs' / module['file'])
    defaults = json.loads(read(ROOT / 'milvus-docs' / reg['variables']['source_file']))
    values = json.loads(read(ROOT / 'zdoc' / page['variables']['file']))
    profile = yaml.safe_load(read(ROOT / 'zdoc' / page['presentation']['code_groups']))
    provenance = json.loads(read(ROOT / 'evidence/provenance.json'))
    result, blocks, consumed = compose(source, page, profile, values, reg['variables']['exports'],
                                       lambda file: read(ROOT / 'zdoc' / file))
    frontmatter, body = split_frontmatter(result)
    for old, new in {**page['links'], **page['assets']}.items():
        body = body.replace('](' + old + ')', '](' + new + ')')
    body = body.replace('<div class="alert note">', '<Admonition type="info" title="Notes">').replace('</div>', '</Admonition>')
    metadata = {**page['metadata'], 'description': frontmatter['summary'] + ' | Cloud'}
    imports = "import Admonition from '@theme/Admonition';\nimport Tabs from '@theme/Tabs';\nimport TabItem from '@theme/TabItem';\n\n"
    mdx = '---\n' + yaml.safe_dump(metadata, sort_keys=False) + '---\n\n' + imports + body
    milvus = bind(END.sub('', START.sub('', source)), defaults, reg['variables']['exports'])
    registry = {
        'schema_version': 1, 'status': 'local-proposal-not-published', 'source_commit': None,
        'based_on_commit': provenance['milvus_base_commit'],
        'modules': {'filtered-search': {'file': module['file'], 'page_digest': sha(source),
            'variables_used': sorted(set(VAR.findall(source))),
            'blocks': {bid: {'kind': b['kind'], 'languages': list(b['codes']), 'content_digest': b['digest']}
                       for bid, b in blocks.items()}}},
    }
    receipt = {'status': 'local-demo-not-a-release-authorization', 'source_commit': None,
               'inputs': inputs, 'builder_digest': sha(Path(__file__).read_text()),
               'transforms': consumed, 'cloud_output_digest': sha(mdx), 'milvus_output_digest': sha(milvus),
               'sdk_cli_execution_verified': False}
    return {'filtered-search.mdx': mdx, 'milvus-filtered-search.md': milvus,
            'registry.json': json.dumps(registry, indent=2) + '\n',
            'build-receipt.json': json.dumps(receipt, indent=2) + '\n'}


def run(check=False):
    output = ROOT / 'generated'
    results = products()
    if check:
        for name, text in results.items():
            if not (output / name).exists() or (output / name).read_text() != text:
                raise ValueError('GENERATED_OUTPUT_DIFFERS:' + name)
        print('Fresh composition matches all generated files.')
    else:
        output.mkdir(exist_ok=True)
        for name, text in results.items():
            (output / name).write_text(text)
        print('Cloud: 2 groups × (7 shared languages + 1 CLI); Milvus: 2 × 7; 3 variables.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    run(parser.parse_args().check)
