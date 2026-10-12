"""One-time construction of the proposed writer inputs from pinned evidence.

Not part of consumption: writers edit the resulting source, config and Cloud content files.
Running this script again overwrites those example inputs.
"""
from pathlib import Path
import difflib
import hashlib
import json
import re
import yaml

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'evidence'
SOURCE_PATH = 'site/en/userGuide/insert-and-delete/delete-entities.md'
LANGS = ['python', 'java', 'javascript', 'go', 'rust', 'c++', 'bash']
LABELS = dict(zip(LANGS, ['Python', 'Java', 'NodeJS', 'Go', 'Rust', 'C++', 'cURL']))
FENCE = re.compile(r'^```([^\n]+)\n(.*?)^```\s*$', re.M | re.S)


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def dump(value):
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True)


def main():
    milvus = (EVIDENCE / 'milvus.original.md').read_text()
    cloud = (EVIDENCE / 'cloud.original.md').read_text()
    tabs = re.findall(r'<Tabs\b[^\n]*>\n(.*?)</Tabs>', cloud, re.S)
    assert len(tabs) == 3
    groups = [dict(FENCE.findall(tab)) for tab in tabs]
    assert all(set(g) == set(LANGS) for g in groups)
    for side, text in [('milvus', milvus), ('cloud', cloud)]:
        write(f'evidence/{side}.original.md', text)

    # Go Cloud auth omission corrected only in this proposal; SDK field was read.
    groups[0]['go'] = groups[0]['go'].replace(
        '    Address: milvusAddr,\n',
        '    Address: milvusAddr,\n    APIKey: "YOUR_CLUSTER_TOKEN",\n')

    # Existing md2md variable syntax. Defaults are merged into the real Variables.json.
    defaults = {'example_endpoint': 'http://localhost:19530',
                'example_token': 'root:Milvus'}
    cloud_values = {'example_endpoint': 'YOUR_CLUSTER_ENDPOINT',
                    'example_token': 'YOUR_CLUSTER_TOKEN'}
    write('milvus-docs/site/en/Variables.json', json.dumps(defaults, indent=2) + '\n')
    write('zdoc/Variables.json', json.dumps(cloud_values, indent=2) + '\n')
    prepared = []
    for index, group in enumerate(groups):
        chunks = []
        for lang in LANGS:
            code = group[lang].rstrip() + '\n'
            code = code.replace('YOUR_CLUSTER_ENDPOINT', '{{var.example_endpoint}}')
            code = code.replace('YOUR_CLUSTER_TOKEN', '{{var.example_token}}')
            chunks.append(f'```{lang}\n{code}```')
        nav = '<div class="multipleCode">\n' + ''.join(f'    <a href="#{lang}">{LABELS[lang]}</a>\n' for lang in LANGS) + '</div>'
        prepared.append(nav + '\n\n' + '\n\n'.join(chunks) + '\n\n')

    # Preserve Milvus prose/chapters; use reconciled Cloud code for all languages.
    group_pattern = re.compile(r'<div class="multipleCode">.*?</div>\s*(?:```[^\n]+\n.*?^```\s*)+', re.M | re.S)
    counter = iter(prepared)
    source, count = group_pattern.subn(lambda _: next(counter), milvus)
    assert count == 3
    write('milvus-docs/' + SOURCE_PATH, source)
    write('evidence/shared-source-changes.diff', ''.join(difflib.unified_diff(
        milvus.splitlines(True), source.splitlines(True), fromfile='Milvus pinned original', tofile='Proposed shared source')))
    write('evidence/provenance.json', json.dumps({
        'status': 'local-design-fixture-not-upstream', 'source_commit': None,
        'milvus_base_commit': '7d87b0bf26d7cbc713f40af6453ea2f925367901',
        'cloud_base_commit': '05e31600f14326073a2c25c1a1eeda8e8d8fcc81',
        'original_hashes': {side: hashlib.sha256(text.encode()).hexdigest() for side, text in [('milvus', milvus), ('cloud', cloud)]},
        'changes': ['Cloud corrections for common code retained', 'Go v3 imports retained from Cloud, compatibility pending',
                    'Cloud Rust/C++ examples proposed as shared content, compatibility pending',
                    'All SDKs share example_token; proposed Go authentication now matches other SDK examples, runtime review pending',
                    'Go local address standardized to http://localhost:19530 (supported by ClientConfig.parse)',
                    'Two scalar variables; zero named regions or Cloud content files'],
        'go_sdk_reference': json.loads((ROOT / 'evidence/go-sdk-reference.json').read_text()),
        'sdk_execution_verified': False,
    }, indent=2) + '\n')
    write('zdoc/shared/modules.yaml', '# Shared registration rules: one entry per source file, not per block.\n' + dump({
        'schema_version': 1,
        'source': {'repository': 'https://github.com/milvus-io/milvus-docs', 'track': 'refs/heads/v3.0.x'},
        'variables': {'source_file': 'site/en/Variables.json', 'exports': {key: {'type': 'text'} for key in defaults}},
        'modules': {'delete-entities': {'file': SOURCE_PATH, 'export_page': True, 'export_blocks': 'marked'}},
    }))
    write('zdoc/shared-pages/delete-entities/page.yaml', '# Proposed consumption schema; executed by the local fixture builder only.\n' + dump({
        'schema_version': 1, 'page': 'cloud.delete-entities',
        'source': {'take': 'page', 'module': 'delete-entities'},
        'presentation': {'code_groups': 'presentation/cloud-sdk-tabs.yaml'},
        'metadata': {'title': 'Delete Entities | Cloud', 'slug': '/delete-entities', 'sidebar_label': 'Delete'},
        'links': {'boolean.md': './filtering-overview'},
        'variables': {'file': 'Variables.json'},
    }))
    cloud_order = ['python', 'java', 'go', 'rust', 'c++', 'javascript', 'bash']
    write('zdoc/presentation/cloud-sdk-tabs.yaml', '# Site policy: shell is optional and appears only when explicitly supplied.\n' + dump({
        'group_id': 'code', 'default': 'python',
        'languages': [{'label': LABELS[lang], 'value': lang, 'required': True} for lang in cloud_order] +
                     [{'label': 'Zilliz CLI', 'value': 'shell', 'required': False}],
    }))


if __name__ == '__main__':
    main()
