"""Offline executable illustration, not the production md2md/zdoc pipeline.

Supports this fixture's standalone fences, multipleCode navigation, and scalar
variables using the existing md2md notation. General Markdown/MDX parsing and language lexers are integration
work, not claimed by this bounded demonstration. Does not fetch, approve or publish.
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
NAV = re.compile(r'<div class="multipleCode">\n(.*?)</div>\s*', re.S)


def sha(text):
    return 'sha256:' + hashlib.sha256(text.encode()).hexdigest()


def read_yaml(path):
    return yaml.safe_load(path.read_text())


def bind_variables(source, values, exports):
    used = set(VAR.findall(source))
    if used - set(exports):
        raise ValueError('UNEXPORTED_VARIABLE:' + ','.join(sorted(used - set(exports))))
    if used - values.keys():
        raise ValueError('MISSING_VARIABLE:' + ','.join(sorted(used - values.keys())))
    for key in used:
        # Bounded example: literal values inside double-quoted code strings.
        # Empty string is valid, but code, quoting and interpolation are not.
        if not isinstance(values[key], str) or not re.fullmatch(r'[A-Za-z0-9_:/.-]*', values[key]):
            raise ValueError('UNSAFE_EXAMPLE_VALUE:' + key)
    result = VAR.sub(lambda m: values[m[1]], source)
    if '{{var.' in result:
        raise ValueError('UNRESOLVED_VARIABLE')
    return result


def render_groups(body, profile):
    languages = [item['value'] for item in profile['languages']]
    required = {item['value'] for item in profile['languages'] if item.get('required')}
    if len(languages) != len(set(languages)) or profile['default'] not in languages:
        raise ValueError('INVALID_PROFILE')
    output, cursor, counts = [], 0, []
    for nav in NAV.finditer(body):
        if nav.start() < cursor:
            raise ValueError('OVERLAPPING_GROUP')
        output.append(body[cursor:nav.start()])
        pos, codes = nav.end(), {}
        while True:
            fence = FENCE.match(body, pos)
            if not fence:
                break
            lang, code = fence.groups()
            if lang in codes:
                raise ValueError('DUPLICATE_LANGUAGE:' + lang)
            codes[lang] = code.rstrip('\n')
            pos = fence.end()
            while pos < len(body) and body[pos].isspace():
                pos += 1
        source_languages = re.findall(r'<a href="#([^"]+)">[^<]+</a>', nav[1])
        if source_languages != list(codes):
            raise ValueError('NAV_CODE_MISMATCH')
        if set(codes) - set(languages) or required - set(codes) or profile['default'] not in codes:
            raise ValueError('LANGUAGE_COVERAGE_MISMATCH')
        present = [item for item in profile['languages'] if item['value'] in codes]
        values = json.dumps([{'label': item['label'], 'value': item['value']} for item in present], separators=(',', ':'))
        output.append(f'<Tabs groupId="{profile["group_id"]}" defaultValue="{profile["default"]}" values={{{values}}}>\n')
        for item in present:
            lang = item['value']
            output.append(f'<TabItem value="{lang}">\n\n```{lang}\n{codes[lang]}\n```\n\n</TabItem>\n')
        output.append('</Tabs>\n\n')
        counts.append([item['value'] for item in present])
        cursor = pos
    output.append(body[cursor:])
    if not counts:
        raise ValueError('NO_CODE_GROUPS')
    rendered = ''.join(output)
    if 'multipleCode' in rendered:
        raise ValueError('UNRECOGNIZED_GROUP')
    return rendered, counts


def validate_page(page):
    # This example exercises only whole-page consumption without differences.
    # The transform implementation and tests live with Filtered Search.
    if page.get('schema_version') != 1:
        raise ValueError('UNSUPPORTED_SCHEMA_VERSION')
    if set(page) - {'schema_version', 'page', 'source', 'variables', 'presentation', 'metadata', 'links', 'transforms'}:
        raise ValueError('UNKNOWN_PAGE_FIELD')
    if 'transforms' in page and page['transforms'] != []:
        raise ValueError('TRANSFORMS_NOT_SUPPORTED_BY_THIS_DEMO')


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
    page = yaml.safe_load(read(ROOT / 'zdoc/shared-pages/delete-entities/page.yaml'))
    validate_page(page)
    if reg.get('schema_version') != 1:
        raise ValueError('UNSUPPORTED_SCHEMA_VERSION')
    if page['source'] != {'take': 'page', 'module': 'delete-entities'}:
        raise ValueError('UNSUPPORTED_SOURCE')
    module = reg['modules']['delete-entities']
    source = read(ROOT / 'milvus-docs' / module['file'])
    profile = yaml.safe_load(read(ROOT / 'zdoc' / page['presentation']['code_groups']))
    provenance = json.loads(read(ROOT / 'evidence/provenance.json'))
    defaults = json.loads(read(ROOT / 'milvus-docs' / reg['variables']['source_file']))
    values = json.loads(read(ROOT / 'zdoc' / page['variables']['file']))
    exports = reg['variables']['exports']
    if 'doc:block:' in source:
        raise ValueError('UNEXPECTED_BLOCK_IN_WHOLE_PAGE_EXAMPLE')
    replaced = bind_variables(source, values, exports)
    milvus_output = bind_variables(source, defaults, exports)
    _, body = replaced[4:].split('\n---\n', 1)
    for old, new in page['links'].items():
        body = body.replace('](' + old + ')', '](' + new + ')')
    rendered, groups = render_groups(body.lstrip('\n'), profile)
    imports = "import Tabs from '@theme/Tabs';\nimport TabItem from '@theme/TabItem';\n\n"
    mdx = '---\n' + yaml.safe_dump(page['metadata'], sort_keys=False) + '---\n\n' + imports + rendered
    registry = {
        'schema_version': 1, 'status': 'local-proposal-not-published', 'source_commit': None,
        'based_on_commit': provenance['milvus_base_commit'],
        'modules': {'delete-entities': {
            'file': module['file'], 'page_digest': sha(source),
            'blocks': {}, 'variables_used': sorted(set(VAR.findall(source))),
        }},
    }
    receipt = {
        'status': 'local-demo-not-a-production-release-receipt',
        'source_commit': None, 'inputs': inputs,
        'builder_digest': sha(Path(__file__).read_text()),
        'code_groups': groups, 'replacement_files': {},
        'variables_used': sorted(set(VAR.findall(source))),
        'milvus_output_digest': sha(milvus_output),
        'output_digest': sha(mdx), 'sdk_execution_verified': False,
    }
    return {'delete-entities.mdx': mdx, 'milvus-delete-entities.md': milvus_output,
            'registry.json': json.dumps(registry, indent=2) + '\n',
            'build-receipt.json': json.dumps(receipt, indent=2) + '\n'}


def run(check=False):
    output = ROOT / 'generated'
    results = products()
    if check:
        for name, text in results.items():
            if not (output / name).exists() or (output / name).read_text() != text:
                raise ValueError('GENERATED_OUTPUT_DIFFERS:' + name)
        print('Generated files match fresh composition from writer inputs.')
    else:
        output.mkdir(exist_ok=True)
        for name, text in results.items():
            (output / name).write_text(text)
        print('Generated 3 groups × 7 languages; 2 variables, zero blocks or replacement files.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    run(parser.parse_args().check)
