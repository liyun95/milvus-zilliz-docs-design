"""One-time preparation from pinned evidence; overwrites demonstration inputs.

Not the writer workflow. Actual upstream changes require content/SDK review.
"""
from pathlib import Path
import difflib
import json
import re
import yaml

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'evidence'
SOURCE_PATH = 'site/en/userGuide/search-query-get/filtered-search.md'
LANGS = ['python', 'java', 'go', 'rust', 'c++', 'javascript', 'bash']
LABELS = ['Python', 'Java', 'Go', 'Rust', 'C++', 'NodeJS', 'cURL']
GROUPS = ['standard-filtering-code', 'iterative-filtering-code']
FENCE = re.compile(r'^```([^\n]+)\n(.*?)^```[ \t]*(?:\n|$)', re.M | re.S)


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def dump(value):
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True)


def main():
    m = (EVIDENCE / 'milvus.original.md').read_text()
    c = (EVIDENCE / 'cloud.original.md').read_text()
    write('evidence/milvus.original.md', m)
    write('evidence/cloud.original.md', c)
    groups = re.findall(r'<Tabs\b[^\n]*>\n(.*?)</Tabs>', c, re.S)
    assert len(groups) == 2
    replacement = []
    for bid, group in zip(GROUPS, groups):
        codes = dict(FENCE.findall(group))
        assert set(codes) == set(LANGS) | {'shell'}
        write(f'zdoc/fragments/filtered-search/{bid.removesuffix("-code")}-cli.md',
              '```shell\n' + codes['shell'].rstrip() + '\n```\n')
        nav = '<div class="multipleCode">\n' + ''.join(
            f'    <a href="#{lang}">{label}</a>\n' for lang, label in zip(LANGS, LABELS)) + '</div>\n\n'
        content = nav + '\n\n'.join(f'```{lang}\n{codes[lang].rstrip()}\n```' for lang in LANGS)
        replacement.append(f'<!-- doc:block:start id="{bid}" -->\n{content}\n<!-- doc:block:end id="{bid}" -->\n\n')
    # Milvus prose and structure; shared code reconciled to Cloud's seven SDKs.
    pattern = re.compile(r'<div class="multipleCode">.*?</div>\s*(?:```[^\n]+\n.*?^```[ \t]*\s*)+', re.M | re.S)
    counter = iter(replacement)
    s, count = pattern.subn(lambda _: next(counter), m)
    assert count == 2
    s = s.replace('YOUR_CLUSTER_ENDPOINT', '{{var.example_endpoint}}').replace('YOUR_CLUSTER_TOKEN', '{{var.example_token}}')
    # Only prose/frontmatter product mentions are parameterized, not code symbols.
    parts = re.split(r'(^```[^\n]+\n.*?^```[ \t]*(?:\n|$))', s, flags=re.M | re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'\bMilvus\b', '{{var.product_name}}', parts[i])
        parts[i] = parts[i].replace('[Filtering](', '[Filtering Explained](')
    s = ''.join(parts)
    # Correct JSON punctuation only; retain example values for independent review.
    def fix_json(match):
        lang, code = match.groups()
        if lang == 'json':
            code = code.replace('，', ',')
            code = re.sub(r',\s*\]', '\n]', code)
            json.loads(code)
        return f'```{lang}\n{code.rstrip()}\n```\n'
    s = FENCE.sub(fix_json, s)
    write('milvus-docs/' + SOURCE_PATH, s)
    write('evidence/shared-source-changes.diff', ''.join(difflib.unified_diff(m.splitlines(True), s.splitlines(True),
          fromfile='Milvus pinned original', tofile='Proposed shared source')))
    defaults = {'product_name': 'Milvus', 'example_endpoint': 'http://localhost:19530', 'example_token': 'root:Milvus'}
    cloud = {'product_name': 'Zilliz Cloud', 'example_endpoint': 'YOUR_CLUSTER_ENDPOINT', 'example_token': 'YOUR_CLUSTER_TOKEN'}
    write('milvus-docs/site/en/Variables.json', json.dumps(defaults, indent=2) + '\n')
    write('zdoc/Variables.json', json.dumps(cloud, indent=2) + '\n')
    write('zdoc/shared/modules.yaml', '# Shared registration rules: one file entry, no manual block inventory.\n' + dump({
        'schema_version': 1,
        'source': {'repository': 'https://github.com/milvus-io/milvus-docs', 'track': 'refs/heads/v3.0.x'},
        'variables': {'source_file': 'site/en/Variables.json', 'exports': {key: {'type': 'text'} for key in defaults}},
        'modules': {'filtered-search': {'file': SOURCE_PATH, 'export_page': True, 'export_blocks': 'marked'}},
    }))
    metadata = yaml.safe_load(c.split('---', 2)[1])
    metadata = {key: value for key, value in metadata.items() if key not in ('token', 'type', 'description')}
    # Preserve Cloud image references; visual equivalence with Milvus is not asserted.
    m_images = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', m)
    c_images = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', c)
    assert len(m_images) == len(c_images) == 2
    write('zdoc/filtered-search.page.yaml', '# Proposed whole-page consumption plus explicit Cloud-only tabs.\n' + dump({
        'schema_version': 1, 'page': 'cloud.filtered-search',
        'source': {'take': 'page', 'module': 'filtered-search'},
        'variables': {'file': 'Variables.json'},
        'presentation': {'code_groups': 'presentation/cloud-sdk-tabs.yaml'},
        'metadata': metadata,
        'links': {'primary-key-search.md': './primary-key-search', 'filtering': './filtering-overview'},
        'assets': dict(zip(m_images, c_images)),
        'transforms': [
            {'operation': 'add',
             'target': {'module': 'filtered-search', 'block': bid, 'language': 'shell'},
             'content': {'file': f'fragments/filtered-search/{bid.removesuffix("-code")}-cli.md'}}
            for bid in GROUPS],
    }))
    write('zdoc/presentation/cloud-sdk-tabs.yaml', '# Site policy: shell is optional and appears only when explicitly supplied.\n' + dump({
        'group_id': 'code', 'default': 'python',
        'languages': [{'label': label, 'value': lang, 'required': True} for lang, label in zip(LANGS, LABELS)] +
                     [{'label': 'Zilliz CLI', 'value': 'shell', 'required': False}],
    }))
    write('evidence/provenance.json', json.dumps({
        'status': 'local-proposal-not-published', 'source_commit': None,
        'milvus_base_commit': '7d87b0bf26d7cbc713f40af6453ea2f925367901',
        'cloud_base_commit': '05e31600f14326073a2c25c1a1eeda8e8d8fcc81',
        'changes': ['Common SDK fixes retained from Cloud; Go v3 compatibility requires review',
                    'Cloud Rust/C++ proposed as shared source; applicability requires review',
                    'Three shared product variables; Go uses the same token',
                    'Two stable code-group markers for Cloud CLI insertion',
                    'JSON output punctuation fixed without changing data',
                    'Filtering link label harmonized; Cloud image URLs retained'],
        'known_content_review': ['Prose says top-K 3 while requests use limit 5',
                                 'Result distances and language output comments require runtime verification',
                                 'Images have not been compared visually'],
        'sdk_cli_execution_verified': False,
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()
