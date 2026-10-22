#!/usr/bin/env python3
"""Maintain a three-column research catalog. Python 3 standard library only."""

import argparse
import csv
import datetime as dt
import fcntl
import html
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import parse_qs, quote, urlsplit, urlunsplit

START = '<!-- HOT_TOPICS:START -->'
END = '<!-- HOT_TOPICS:END -->'
HEADER = ['名称', '详细信息', '原始链接']
EMPTY = '当前尚未收录真实热点。第一条材料到来后更新表格。'
KINDS = {'douyin', 'bilibili', 'youtube', 'wechat', 'web', 'screenshot'}
SECTIONS = ['一句话结论', '原始线索', '技术实现', '复现路径', '待核实事项', '来源与证据']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value, label):
    require(isinstance(value, str) and value.strip(), label + ' must be nonempty text')
    require(not any(ord(c) < 32 for c in value), label + ' contains control characters')
    return value.strip()


def inside(root, relative):
    path = root / relative
    require(root in path.resolve().parents, 'path escapes repository: ' + relative)
    return path


def source(value):
    require(isinstance(value, dict), 'source must be an object')
    kind = value.get('kind', 'web')
    require(kind in KINDS, 'unsupported source kind')
    raw = value.get('url')
    note = value.get('note', '')
    title = value.get('title', '')
    require(isinstance(note, str) and isinstance(title, str), 'source title/note must be text')
    for field in (note, title):
        require(not any(ord(c) < 32 for c in field), 'source contains control characters')
    if raw is not None:
        raw = text(raw, 'source url')
        url = urlsplit(raw)
        require(url.scheme in ('http', 'https') and url.hostname, 'source URL must be HTTP(S)')
        require(not url.username and not url.password, 'source URL must not contain credentials')
    else:
        require(kind == 'screenshot' and note.strip(), 'missing URL needs screenshot kind and a provenance note')
    return {'kind': kind, 'url': raw, 'title': title.strip(), 'note': note.strip()}


def canonical(item):
    if not item['url']:
        return 'screenshot:' + item['note']
    u = urlsplit(item['url'])
    host = (u.hostname or '').lower().removeprefix('www.')
    q = parse_qs(u.query)
    if host == 'youtu.be':
        return 'youtube:' + u.path.strip('/')
    if host in ('youtube.com', 'm.youtube.com'):
        ident = q.get('v', [''])[0]
        if not ident:
            m = re.match(r'^/(?:shorts|embed|live)/([^/]+)', u.path)
            ident = m.group(1) if m else ''
        if ident:
            return 'youtube:' + ident
    if host in ('bilibili.com', 'm.bilibili.com'):
        m = re.search(r'/video/((?:BV|av)[A-Za-z0-9]+)', u.path)
        if m:
            return 'bilibili:' + m.group(1) + ':p' + q.get('p', ['1'])[0]
    if host in ('douyin.com', 'm.douyin.com'):
        m = re.search(r'/video/(\d+)', u.path)
        if m:
            return 'douyin:' + m.group(1)
    if host == 'mp.weixin.qq.com' and all(k in q for k in ('__biz', 'mid', 'idx', 'sn')):
        return 'wechat:' + ':'.join(q[k][0] for k in ('__biz', 'mid', 'idx', 'sn'))
    return urlunsplit((u.scheme.lower(), u.netloc.lower(), u.path, u.query, ''))


def load(root):
    data = json.loads(inside(root, 'data/topics.json').read_text(encoding='utf-8'))
    require(isinstance(data, dict) and data.get('schema_version') == 1, 'unsupported catalog schema')
    require(isinstance(data.get('topics'), list), 'topics must be a list')
    seen = set()
    for item in data['topics']:
        ident = item.get('id', '')
        require(isinstance(ident, str) and re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}', ident), 'invalid topic id')
        require(ident not in seen, 'duplicate topic id: ' + ident)
        seen.add(ident)
        text(item.get('name'), 'name')
        require(item.get('report') == 'topics/' + ident + '/README.md', 'invalid report path')
        require(isinstance(item.get('sources'), list) and item['sources'], 'topic needs sources')
        for s in item['sources']:
            require(source(s) == s, 'source is not normalized')
        for key in ('created_at', 'updated_at'):
            dt.datetime.fromisoformat(item[key])
    return data


def md(value):
    value = html.escape(value, quote=False)
    return re.sub(r'([\\`*_{}\[\]<>])', r'\\\1', value).replace('|', '&#124;')


def url_md(value):
    return quote(value, safe=':/?&=#%+@,;~-._')


def source_cell(s):
    if s['url']:
        label = s['title'] or s['kind']
        return '[' + md(label) + '](' + url_md(s['url']) + ')'
    return '截图提供，原链接待补（' + md(s['note']) + '）'


def csv_safe(value):
    return "'" + value if value.lstrip().startswith(('=', '+', '-', '@')) else value


def outputs(root, data):
    readme = inside(root, 'README.md').read_text(encoding='utf-8')
    require(readme.count(START) == readme.count(END) == 1, 'README needs exactly one index marker pair')
    before, rest = readme.split(START)
    _, after = rest.split(END)
    lines = ['| ' + ' | '.join(HEADER) + ' |', '| --- | --- | --- |']
    buf = io.StringIO(newline='')
    writer = csv.writer(buf, lineterminator='\n')
    writer.writerow(HEADER)
    for t in data['topics']:
        links = '<br>'.join(source_cell(s) for s in t['sources'])
        lines.append('| ' + md(t['name']) + ' | [查看详细信息](' + t['report'] + ') | ' + links + ' |')
        sources = '\n'.join(s['url'] or '截图提供，原链接待补（' + s['note'] + '）' for s in t['sources'])
        writer.writerow([csv_safe(t['name']), t['report'], csv_safe(sources)])
    if data['topics']:
        after = after.replace('\n\n' + EMPTY, '')
    elif EMPTY not in after:
        after = '\n\n' + EMPTY + after
    return {'README.md': before + START + '\n' + '\n'.join(lines) + '\n' + END + after,
            '热点信息汇总.csv': '\ufeff' + buf.getvalue()}


def report_check(body):
    require(isinstance(body, str) and body.startswith('# '), 'report needs an H1 title')
    require('{{' not in body and '}}' not in body, 'report still contains template placeholders')
    for section in SECTIONS:
        require(re.search(r'^## ' + section + r'\s*$', body, re.M), 'report missing section: ' + section)
    require(len(body.strip()) > 180, 'report is too short to contain useful research')


def write_all(root, files):
    staged = []
    try:
        for relative, content in files.items():
            path = inside(root, relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
                staged.append((Path(f.name), path))
        for temp, path in staged:
            os.replace(temp, path)
    finally:
        for temp, _ in staged:
            temp.unlink(missing_ok=True)


def check(root, data):
    for t in data['topics']:
        report_check(inside(root, t['report']).read_text(encoding='utf-8'))
    for relative, expected in outputs(root, data).items():
        require(inside(root, relative).read_text(encoding='utf-8') == expected,
                relative + ' differs from catalog; run render')
    print(json.dumps({'ok': True, 'topics': len(data['topics']), 'columns': HEADER}, ensure_ascii=False))


def execute(args, root):
    if args.command == 'init':
        if inside(root, 'data/topics.json').exists():
            return check(root, load(root))
        if not inside(root, 'README.md').exists():
            write_all(root, {'README.md': '# 热点信息汇总\n\n' + START + '\n' + END + '\n'})
        data = {'schema_version': 1, 'topics': []}
        files = outputs(root, data)
        files['data/topics.json'] = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
        write_all(root, files)
        return check(root, data)
    data = load(root)
    if args.command == 'list':
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if args.command == 'check':
        return check(root, data)
    if args.command == 'render':
        for t in data['topics']:
            report_check(inside(root, t['report']).read_text(encoding='utf-8'))
        write_all(root, outputs(root, data))
        return check(root, data)
    entry = json.loads(Path(args.entry).read_text(encoding='utf-8'))
    require(isinstance(entry, dict), 'entry must be an object')
    ident = entry.get('id', '')
    require(isinstance(ident, str) and re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}', ident), 'id must use 1-80 lowercase letters, digits and hyphens')
    name = text(entry.get('name'), 'name')
    require(isinstance(entry.get('sources'), list) and entry['sources'], 'entry needs sources')
    incoming = [source(s) for s in entry['sources']]
    body = Path(args.report).read_text(encoding='utf-8').rstrip() + '\n'
    report_check(body)
    # Refuse to mutate an already inconsistent catalog; repair with render first.
    check(root, data)
    old = next((t for t in data['topics'] if t['id'] == ident), None)
    merged = list(old['sources']) if old else []
    for s in incoming:
        # Keep distinct original URLs even when they refer to the same platform ID.
        match = next((i for i, existing in enumerate(merged)
                      if (existing['url'] == s['url'] if s['url'] else existing == s)), None)
        if match is None:
            merged.append(s)
        else:
            merged[match] = {k: s[k] or merged[match][k] for k in s}
    keys = {canonical(s) for s in merged}
    for other in data['topics']:
        if other['id'] != ident and keys.intersection(canonical(s) for s in other['sources']):
            require(args.allow_shared_source, 'source already belongs to ' + other['id'] + '; reuse that id or confirm multiple topics with --allow-shared-source')
    relative = 'topics/' + ident + '/README.md'
    if old and old['name'] == name and old['sources'] == merged and inside(root, relative).read_text(encoding='utf-8') == body:
        print(json.dumps({'ok': True, 'changed': False, 'id': ident}))
        return
    if not old:
        require(not inside(root, relative).exists(), 'untracked topic report exists; refusing to overwrite')
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    record = {'id': ident, 'name': name, 'report': relative, 'sources': merged,
              'created_at': old['created_at'] if old else now, 'updated_at': now}
    if old:
        data['topics'][data['topics'].index(old)] = record
    else:
        data['topics'].append(record)
    files = outputs(root, data)
    files[relative] = body
    files['data/topics.json'] = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    write_all(root, files)
    check(root, data)
    print(json.dumps({'ok': True, 'changed': True, 'id': ident, 'report': relative}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, help='Repository root')
    commands = parser.add_subparsers(dest='command', required=True)
    for command in ('init', 'list', 'render', 'check'):
        commands.add_parser(command)
    upsert = commands.add_parser('upsert')
    upsert.add_argument('--entry', required=True, help='Topic metadata JSON')
    upsert.add_argument('--report', required=True, help='Completed Markdown report')
    upsert.add_argument('--allow-shared-source', action='store_true', help='One source really describes multiple independent topics')
    args = parser.parse_args()
    root = Path(args.repo).expanduser().resolve()
    if args.command == 'init':
        root.mkdir(parents=True, exist_ok=True)
    require(root.is_dir(), 'repository directory does not exist')
    with inside(root, '.hot-topics.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        execute(args, root)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        sys.exit(1)
