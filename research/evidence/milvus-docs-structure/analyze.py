"""Read-only structure analysis of milvus-docs shared-page candidates.

Measures what structural targeting and product-name handling would face:
heading duplicates, sections with several code groups, heading renames over
the last year, and how "Milvus" appears in prose. Reads Git objects only;
never checks out or modifies the repository.

Usage: python3 analyze.py <milvus-docs clone> <ref> <since YYYY-MM-DD> > results.json
"""
import collections
import json
import re
import subprocess
import sys

PATHS = ['site/en/userGuide', 'site/en/embeddings']
FENCE = re.compile(r'^\s*(```|~~~)')
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
BADGE = re.compile(r'\s*\|\s*Milvus [\d.]+(\.x|\+)?\s*$')
NAME_CLASSES = [  # first match wins; checked on a window around each hit
    ('edition', r'Milvus (Lite|Standalone|Distributed|Operator|Helm|Backup|CDC|WebUI|Web UI|CLI|Client)'),
    ('version', r'Milvus v?\d'),
    ('identifier', r'pymilvus|MilvusClient|AsyncMilvusClient|milvus\.yaml|milvus-io|milvus\.io|milvusdb|milvus-sdk'
                   r'|milvus_|_milvus|milvus-|-milvus|\.milvus|milvus\.|MilvusException|/milvus|Milvus[A-Z]'),
    ('plain_name', r'Milvus'),
    ('other_lowercase', r'milvus'),
]


class Repo:
    def __init__(self, path):
        self.path = path
        self.cat = subprocess.Popen(['git', '-C', path, 'cat-file', '--batch'],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def git(self, *args):
        return subprocess.run(['git', '-C', self.path, *args], capture_output=True, text=True, check=True).stdout

    def show(self, spec):
        self.cat.stdin.write((spec + '\n').encode())
        self.cat.stdin.flush()
        header = self.cat.stdout.readline().decode()
        if header.endswith('missing\n'):
            return None
        size = int(header.split()[2])
        data = self.cat.stdout.read(size)
        self.cat.stdout.read(1)
        return data.decode('utf-8', 'replace')


def scan(text):
    """Headings outside fences, and the section path of each multi-language code group."""
    heads, groups, path, fenced = [], [], [], False
    for line in text.split('\n'):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = HEADING.match(line)
        if match:
            level, title = len(match[1]), match[2]
            path = [p for p in path if p[0] < level] + [(level, title)]
            heads.append(title)
        elif 'class="multipleCode"' in line:
            groups.append(tuple(t for _, t in path))
    return heads, groups


def normalize(title):
    return BADGE.sub('', title.replace('​', '')).lower().rstrip(':').strip()


def structure(repo, ref, files):
    stats = collections.Counter()
    duplicates, multi_group = {}, {}
    for name in files:
        heads, groups = scan(repo.show(f'{ref}:{name}'))
        stats['pages'] += 1
        stats['headings'] += len(heads)
        stats['headings_with_version_badge'] += sum(1 for h in heads if BADGE.search(h))
        stats['explicit_heading_ids'] += sum(1 for h in heads if re.search(r'\{#[^}]+\}$|<!--\s*#', h))
        dups = {t: c for t, c in collections.Counter(heads).items() if c > 1}
        if dups:
            duplicates[name] = dups
        per_section = collections.Counter(groups)
        stats['code_groups'] += len(groups)
        stats['sections_with_code_group'] += len(per_section)
        many = {(p[-1] if p else '(top)'): c for p, c in per_section.items() if c > 1}
        if many:
            multi_group[name] = many
            stats['sections_with_several_code_groups'] += len(many)
    stats['pages_with_duplicate_heading_text'] = len(duplicates)
    stats['pages_with_a_section_holding_several_code_groups'] = len(multi_group)
    return stats, duplicates, multi_group


def heading_churn(repo, ref, since):
    log = repo.git('log', ref, f'--since={since}', '--no-merges', '--format=@%H', '--name-only', '--', *PATHS)
    stats, events, commit = collections.Counter(), [], None
    pages_any, pages_real = set(), set()
    for line in log.split('\n'):
        if line.startswith('@'):
            commit = line[1:]
            stats['commits'] += 1
            continue
        if not line.endswith('.md'):
            continue
        stats['file_changes'] += 1
        before, after = repo.show(f'{commit}^:{line}'), repo.show(f'{commit}:{line}')
        if before is None or after is None:
            continue
        old, new = collections.Counter(scan(before)[0]), collections.Counter(scan(after)[0])
        removed, added = old - new, new - old
        if not removed:
            continue
        pages_any.add(line)
        stats['file_changes_removing_or_renaming_a_heading'] += 1
        added_norm = collections.Counter(normalize(t) for t in added.elements())
        real = []
        for title in removed.elements():
            stats['headings_removed_or_renamed'] += 1
            if added_norm[normalize(title)]:
                added_norm[normalize(title)] -= 1
                stats['cosmetic_only'] += 1
            else:
                real.append(title)
        if real:
            pages_real.add(line)
        events.append({'commit': commit[:8], 'file': line, 'removed': list(removed.elements()),
                       'added': list(added.elements())})
    stats['pages_with_any_heading_change'] = len(pages_any)
    stats['pages_with_real_heading_change'] = len(pages_real)
    return stats, events


def product_names(repo, ref, files):
    counts, pages_plain, in_code = collections.Counter(), set(), 0
    for name in files:
        fenced = False
        for line in repo.show(f'{ref}:{name}').split('\n'):
            if FENCE.match(line):
                fenced = not fenced
                continue
            if fenced:
                in_code += len(re.findall(r'(?i)milvus', line))
                continue
            if line.startswith('---') or re.match(r'^(id|title|summary|beta|related_key):', line):
                continue
            for hit in re.finditer(r'(?i)milvus', line):
                if HEADING.match(line) and BADGE.search(line) and line.rfind('| Milvus') <= hit.start() + 2:
                    counts['heading_version_badge'] += 1
                    continue
                window = line[max(0, hit.start() - 10):hit.end() + 12]
                for label, pattern in NAME_CLASSES:
                    found = re.search(pattern, window)
                    if found and found.start() <= 10 + len(hit[0]) and found.end() >= 10:
                        counts[label] += 1
                        if label == 'plain_name':
                            pages_plain.add(name)
                        break
    return {'prose': counts, 'pages_with_plain_name': len(pages_plain), 'in_code_blocks': in_code}


def main():
    path, ref, since = sys.argv[1:4]
    repo = Repo(path)
    files = [f for f in repo.git('ls-tree', '-r', '--name-only', ref, *PATHS).split('\n') if f.endswith('.md')]
    stats, duplicates, multi_group = structure(repo, ref, files)
    churn, events = heading_churn(repo, ref, since)
    print(json.dumps({
        'ref': ref, 'commit': repo.git('rev-parse', '--short', ref).strip(), 'paths': PATHS, 'since': since,
        'structure': stats, 'heading_churn': churn, 'product_names': product_names(repo, ref, files),
        'duplicate_headings': duplicates, 'sections_with_several_code_groups': multi_group,
        'heading_change_events': events,
    }, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
