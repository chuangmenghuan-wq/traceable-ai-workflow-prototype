from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

OUT = Path('research_outputs/horse_round038')
OUT.mkdir(parents=True, exist_ok=True)

ENDPOINTS = {
    'interactive_login': 'https://identitysso.betfair.com/api/login',
    'cert_login': 'https://identitysso-cert.betfair.com/api/certlogin',
    'keep_alive': 'https://identitysso.betfair.com/api/keepAlive',
}

S = requests.Session()
S.headers.update({'User-Agent': 'FutureAbilityHorsePaper/1.0 (identity-bootstrap transport audit)'})


def probe(name: str, url: str) -> dict:
    try:
        # Deliberately send no credentials/session so this is transport-only and cannot consume account login attempts.
        if name == 'keep_alive':
            r = S.get(url, headers={'Accept': 'application/json'}, timeout=30)
        else:
            r = S.post(url, headers={'Accept': 'application/json'}, data={}, timeout=30)
        body = r.text[:700]
        try:
            j = r.json()
        except Exception:
            j = None
        low = body.lower()
        cloudflare = 'cloudflare' in low or 'attention required' in low
        betfair_json = isinstance(j, dict)
        return {
            'url': url,
            'http_status': r.status_code,
            'content_type': r.headers.get('content-type'),
            'cloudflare_block': cloudflare,
            'betfair_json_response': betfair_json,
            'json_status': (j or {}).get('status') if betfair_json else None,
            'json_error': (j or {}).get('error') if betfair_json else None,
            'body_prefix': None if betfair_json else body,
        }
    except Exception as e:
        return {'url': url, 'error': repr(e), 'cloudflare_block': False, 'betfair_json_response': False}


def main() -> None:
    probes = {k: probe(k, v) for k, v in ENDPOINTS.items()}
    secret_presence = {
        'BETFAIR_SESSION_TOKEN': bool(os.getenv('BETFAIR_SESSION_TOKEN', '').strip()),
        'BETFAIR_SSOID': bool(os.getenv('BETFAIR_SSOID', '').strip()),
        'BETFAIR_APP_KEY': bool(os.getenv('BETFAIR_APP_KEY', '').strip()),
        'BETFAIR_DELAYED_APP_KEY': bool(os.getenv('BETFAIR_DELAYED_APP_KEY', '').strip()),
        'BETFAIR_USERNAME': bool(os.getenv('BETFAIR_USERNAME', '').strip()),
        'BETFAIR_PASSWORD': bool(os.getenv('BETFAIR_PASSWORD', '').strip()),
        'BETFAIR_CERT_PEM': bool(os.getenv('BETFAIR_CERT_PEM', '').strip()),
        'BETFAIR_CERT_KEY_PEM': bool(os.getenv('BETFAIR_CERT_KEY_PEM', '').strip()),
    }

    cert_transport = probes['cert_login'].get('betfair_json_response', False) and not probes['cert_login'].get('cloudflare_block', False)
    interactive_transport = probes['interactive_login'].get('betfair_json_response', False) and not probes['interactive_login'].get('cloudflare_block', False)
    keepalive_transport = probes['keep_alive'].get('betfair_json_response', False) and not probes['keep_alive'].get('cloudflare_block', False)

    if secret_presence['BETFAIR_SESSION_TOKEN'] or secret_presence['BETFAIR_SSOID']:
        classification = 'ONE_TIME_SESSION_BOOTSTRAP_AVAILABLE'
        blocker = None
    elif all([secret_presence['BETFAIR_USERNAME'], secret_presence['BETFAIR_PASSWORD'], secret_presence['BETFAIR_APP_KEY'], secret_presence['BETFAIR_CERT_PEM'], secret_presence['BETFAIR_CERT_KEY_PEM']]):
        classification = 'NONINTERACTIVE_CERT_IDENTITY_MATERIAL_PRESENT'
        blocker = None
    elif cert_transport:
        classification = 'IDENTITY_TRANSPORT_READY_EXTERNAL_ACCOUNT_BOOTSTRAP_REQUIRED'
        blocker = 'ONE_TIME_BETFAIR_ACCOUNT_AUTH_AND_CERTIFICATE_REGISTRATION_REQUIRED'
    else:
        classification = 'IDENTITY_TRANSPORT_BLOCKED_OR_UNVERIFIED'
        blocker = 'GITHUB_RUNNER_CANNOT_YET_PROVE_CERTLOGIN_TRANSPORT'

    status = {
        'round': 38,
        'capability': 'HorseRacing.BetfairIdentityBootstrap',
        'status': 'COMPLETE',
        'captured_at_utc': datetime.now(timezone.utc).isoformat(),
        'strategy_tuning': False,
        'paper_only': True,
        'real_betting_allowed': False,
        'secret_presence': secret_presence,
        'transport': {
            'interactive_login_reachable': interactive_transport,
            'cert_login_reachable': cert_transport,
            'keep_alive_reachable': keepalive_transport,
            'probes': probes,
        },
        'target_architecture': {
            'bootstrap': 'One authenticated Betfair browser/session is sufficient to create/retrieve Delayed App Key.',
            'persistent_runtime': 'Non-interactive certificate login renews session autonomously; KeepAlive extends active session.',
            'two_factor_note': 'Betfair documents that website 2FA does not prevent non-interactive certificate login.',
            'secret_storage_required': ['BETFAIR_USERNAME','BETFAIR_PASSWORD','BETFAIR_APP_KEY','BETFAIR_CERT_PEM','BETFAIR_CERT_KEY_PEM'],
            'session_material_must_never_be_committed': True,
        },
        'classification': classification,
        'remaining_blocker': blocker,
        'governance': {
            'orders_forbidden': True,
            'live_key_activation_forbidden': True,
            'no_credentials_written_to_repo': True,
            'no_account_login_attempts_performed': True,
        },
    }
    (OUT / 'status.json').write_text(json.dumps(status, indent=2), encoding='utf-8')
    print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
