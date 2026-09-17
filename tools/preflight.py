"""lego-pipe-memo/v1 preflight (minimal reference implementation). Usage: preflight.py MEMO.md REGISTER.md"""
import sys, re, yaml
path, reg = sys.argv[1], sys.argv[2]
raw = open(path, encoding='utf-8').read()
errs, warns = [], []
if '\t' in raw.split('\n---',2)[1]: errs.append('tab in frontmatter')
m = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
if not m: sys.exit('no frontmatter')
fm_text = m.group(1)
# duplicate top-level keys
tops = re.findall(r'^([A-Za-z_][\w-]*):', fm_text, re.M)
dups = {k for k in tops if tops.count(k) > 1}
if dups: errs.append(f'duplicate keys {dups}')
fm = yaml.safe_load(fm_text)
REQ = {'correspondence_schema': str, 'memo': str, 'revision': str, 'status': str, 'memo_type': str,
       'title': str, 'date': (str, object), 'from': (str, dict), 'to': (list, dict), 'thread': str, 'cluster': str,
       'repos': list, 'tags': list, 'argument': str, 'parts': dict, 'provenance': dict}
for k, ty in REQ.items():
    if k not in fm: errs.append(f'missing {k}')
    elif not isinstance(fm[k], ty if isinstance(ty, tuple) else (ty,)): errs.append(f'type {k}: {type(fm[k]).__name__}')
if fm.get('correspondence_schema') != 'lego-pipe-memo/v1': errs.append('schema id')
if fm.get('status') not in {'draft','for_review','for_reconciliation','accepted','accepted_work_order','superseded'}: errs.append(f"status {fm.get('status')}")
if fm.get('memo_type') not in {'handoff','review_response','decision','work_order','findings','review'}: errs.append('memo_type')
if not str(fm.get('argument','')).lstrip().startswith('In which'): warns.append('argument does not begin "In which"')
# finding IDs in body must be declared
body = raw[m.end():]
used = set(re.findall(r'\b([RNC]-\d{1,2})\b', body))
declared = {f['id'] for f in fm.get('findings', [])} if 'findings' in fm else set()
if 'findings' in fm:
    undeclared = sorted(u for u in used if u not in declared)
    if undeclared: errs.append(f'finding ids used but not declared: {undeclared}')
# register uniqueness + references
regtxt = open(reg, encoding='utf-8').read()
num = fm['memo'].split('-')[-1]
key = f"{num}-{fm['revision']}"
if key in regtxt and 'superseded' not in regtxt.split(key,1)[1].split('\n',1)[0]:
    warns.append(f'{key} already listed in register (expected on re-run)')
irt = fm.get('in_reply_to')
if irt:
    n = str(irt['memo'] if isinstance(irt, dict) else irt).split('-')[-1]
    if n not in regtxt: errs.append(f'in_reply_to {n} not in register')
sup = fm.get('supersedes')
if sup and str(sup).split('-')[-2] not in regtxt: errs.append(f'supersedes {sup} not in register')
print(f"{path}: memo={fm['memo']} rev={fm['revision']} status={fm['status']} keys={len(fm)} findings={len(fm.get('findings',[]))} ids_used_in_body={len(used)}")
for w in warns: print('  WARN', w)
for e in errs: print('  ERROR', e)
sys.exit(1 if errs else 0)
