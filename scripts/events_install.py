"""Discover Windows receiver enrollment without changing accounts or permissions."""
import json
import os
from pathlib import Path


def status(home=None, scripts=None):
    home=Path(home or Path.home()).expanduser().resolve()
    scripts=Path(scripts or Path(__file__).resolve().parent)
    state=home/'.codex/hub/skills-events'
    config=state/'config.json'
    service=scripts/'skills-events.json'
    if os.name!='nt': return {'enabled':False,'reason':'windows-only'}
    if config.exists():
        data=json.loads(config.read_text(encoding='utf-8-sig'))
        return {'enrolled':True,'device_id':data['device_id'],'status_file':str(state/'status.json'),
                'note':'Existing receiver is pinned locally; run setup to update its runtime explicitly.'}
    if service.exists():
        endpoint=json.loads(service.read_text(encoding='utf-8-sig'))['endpoint']
        return {'enrolled':False,'reason':'one-time-invitation-required','endpoint':endpoint,
                'setup_script':str(scripts/'setup-skills-events.ps1'),
                'next_action':'Ask the Redoma administrator for a one-use invitation and run the setup script with Endpoint and RepositoryRoot.'}
    return {'enrolled':False,'reason':'service-not-configured'}
