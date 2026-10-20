"""Explicit human approval receipts bound to exact skill files."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

def tree_hash(files):
    return hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()

def read_manifest(path):
    path=Path(path)
    if not path.exists(): return {'schema_version':1,'approvals':[]}
    data=json.loads(path.read_text(encoding='utf-8-sig'))
    if data.get('schema_version')!=1 or not isinstance(data.get('approvals'),list):
        raise ValueError('Approval manifest schema invalid.')
    seen=set()
    for row in data['approvals']:
        key=(row.get('skill'),row.get('sha256'))
        if key in seen: raise ValueError('Approval receipt duplicated.')
        seen.add(key)
    return data

def valid_receipt(entry,row):
    if (row.get('skill'),row.get('sha256'))!=(entry['name'],entry['sha256']): return False
    if row.get('status')!='approved' or row.get('kind')!='explicit-human': return False
    creator=row.get('creator','').strip()
    if not creator or creator.casefold()!=row.get('approved_by','').strip().casefold(): return False
    if not row.get('evidence','').strip(): return False
    try: when=datetime.fromisoformat(row.get('approved_at','').replace('Z','+00:00'))
    except (ValueError,TypeError): return False
    return when.tzinfo is not None and bool(re.fullmatch('[0-9a-f]{64}',entry['sha256']))

def pending(entries,manifest):
    result=[]
    for entry in entries:
        if entry.get('files') is not None and tree_hash(entry['files'])!=entry['sha256']:
            raise ValueError('Approval tree hash differs from catalog: '+entry['name'])
        if not any(valid_receipt(entry,row) for row in manifest['approvals']):
            result.append({'skill':entry['name'],'sha256':entry['sha256'],'status':'awaiting-human-approval'})
    return result

def require(entries,path):
    missing=pending(entries,read_manifest(path))
    if missing:
        names=', '.join(sorted({row['skill'] for row in missing}))
        raise ValueError('Human approval required for exact skill versions: '+names+'. No publication or shared installation allowed.')
    return {'approved_versions':len(entries)}

def filtered(manifest,entries):
    keys={(e['name'],e['sha256']) for e in entries}
    return {'schema_version':1,'approvals':[r for r in manifest['approvals'] if (r.get('skill'),r.get('sha256')) in keys]}
