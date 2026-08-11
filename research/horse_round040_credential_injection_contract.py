from __future__ import annotations

import base64
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from nacl import encoding, public

OUT = Path('research_outputs/horse_round040')
OUT.mkdir(parents=True, exist_ok=True)

CONTRACT_SHA256 = 'e446a15ebc40bd4ad7ccc820e60ec829d623311f22d71b425c98c01fc13724e3'
EXPECTED = {
    'BETFAIR_USERNAME': 'text',
    'BETFAIR_PASSWORD': 'text',
    'BETFAIR_DELAYED_APP_KEY': 'text',
    'BETFAIR_CERT_PEM': 'certificate_pem',
    'BETFAIR_CERT_KEY_PEM': 'private_key_pem',
}
OPTIONAL = ['BETFAIR_SESSION_TOKEN', 'BETFAIR_SSOID']
SENTINEL_NAME = 'FUTURE_ABILITY_SECRET_WRITE_PROBE'
SENTINEL_VALUE = 'round040-control-plane-probe-v1'


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_material(name: str, value: str) -> dict:
    rec = {'present': bool(value), 'format_valid': None}
    if not value:
        return rec
    if name == 'BETFAIR_CERT_PEM':
        rec['format_valid'] = '-----BEGIN CERTIFICATE-----' in value and '-----END CERTIFICATE-----' in value
    elif name == 'BETFAIR_CERT_KEY_PEM':
        rec['format_valid'] = (
            ('-----BEGIN PRIVATE KEY-----' in value and '-----END PRIVATE KEY-----' in value)
            or ('-----BEGIN RSA PRIVATE KEY-----' in value and '-----END RSA PRIVATE KEY-----' in value)
            or ('-----BEGIN EC PRIVATE KEY-----' in value and '-----END EC PRIVATE KEY-----' in value)
        )
    else:
        rec['format_valid'] = len(value.strip()) > 0
    return rec


def github_secret_control_probe() -> dict:
    token = os.getenv('GITHUB_TOKEN', '').strip()
    repo = os.getenv('GITHUB_REPOSITORY', '').strip()
    if not token or not repo:
        return {'status': 'GITHUB_CONTROL_AUTH_MISSING', 'public_key_http': None, 'sentinel_write_http': None, 'sentinel_delete_http': None}

    h = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    base = f'https://api.github.com/repos/{repo}/actions/secrets'
    try:
        r = requests.get(base + '/public-key', headers=h, timeout=30)
        result = {
            'public_key_http': r.status_code,
            'sentinel_write_http': None,
            'sentinel_delete_http': None,
            'sentinel_name': SENTINEL_NAME,
            'sentinel_contains_sensitive_material': False,
        }
        if r.status_code != 200:
            result['status'] = 'SECRET_PUBLIC_KEY_UNAVAILABLE'
            return result
        j = r.json()
        key_id = str(j.get('key_id') or '')
        key_b64 = str(j.get('key') or '')
        if not key_id or not key_b64:
            result['status'] = 'SECRET_PUBLIC_KEY_MALFORMED'
            return result

        pk = public.PublicKey(key_b64.encode(), encoding.Base64Encoder())
        sealed = public.SealedBox(pk).encrypt(SENTINEL_VALUE.encode())
        encrypted_value = base64.b64encode(sealed).decode()
        put = requests.put(
            base + '/' + SENTINEL_NAME,
            headers=h,
            json={'encrypted_value': encrypted_value, 'key_id': key_id},
            timeout=30,
        )
        result['sentinel_write_http'] = put.status_code
        if put.status_code not in (201, 204):
            result['status'] = 'SECRET_WRITE_FORBIDDEN'
            return result

        delete = requests.delete(base + '/' + SENTINEL_NAME, headers=h, timeout=30)
        result['sentinel_delete_http'] = delete.status_code
        if delete.status_code == 204:
            result['status'] = 'SECRET_WRITE_DELETE_CONTROL_PLANE_READY'
        else:
            result['status'] = 'SECRET_WRITE_READY_DELETE_FAILED_SENTINEL_MAY_REMAIN'
        return result
    except Exception as e:
        return {'status': 'SECRET_CONTROL_PROBE_EXCEPTION', 'error': repr(e), 'public_key_http': None, 'sentinel_write_http': None, 'sentinel_delete_http': None}


def main() -> None:
    materials = {name: validate_material(name, os.getenv(name, '').strip()) for name in EXPECTED}
    optional = {name: bool(os.getenv(name, '').strip()) for name in OPTIONAL}
    present = [k for k, v in materials.items() if v['present']]
    missing = [k for k, v in materials.items() if not v['present']]
    bad_format = [k for k, v in materials.items() if v['present'] and v['format_valid'] is False]

    control = github_secret_control_probe()

    if not missing and not bad_format:
        material_state = 'IDENTITY_SECRET_SET_COMPLETE'
    elif present:
        material_state = 'IDENTITY_SECRET_SET_PARTIAL'
    else:
        material_state = 'IDENTITY_SECRET_SET_EMPTY'

    control_ready = control.get('status') == 'SECRET_WRITE_DELETE_CONTROL_PLANE_READY'
    if material_state == 'IDENTITY_SECRET_SET_COMPLETE':
        classification = 'CREDENTIAL_INJECTION_COMPLETE_RUNTIME_READY_FOR_CERTLOGIN'
        blocker = None
    elif control_ready:
        classification = 'SECRET_CONTROL_PLANE_READY_AWAITING_BETFAIR_IDENTITY_MATERIAL'
        blocker = 'BETFAIR_IDENTITY_MATERIAL_NOT_YET_PROVIDED_TO_SECRET_STORE'
    else:
        classification = 'CREDENTIAL_INJECTION_CONTRACT_READY_CONTROL_PLANE_WRITE_UNAVAILABLE'
        blocker = 'NO_CONNECTED_CAPABILITY_CAN_WRITE_GITHUB_ACTIONS_SECRETS'

    status = {
        'round': 40,
        'capability': 'HorseRacing.BetfairCredentialInjectionContract',
        'status': 'COMPLETE',
        'captured_at_utc': now(),
        'contract_sha256': CONTRACT_SHA256,
        'strategy_tuning': False,
        'paper_only': True,
        'real_betting_allowed': False,
        'required_secret_contract': {
            'required_names': list(EXPECTED),
            'optional_session_names': OPTIONAL,
            'secrets_must_never_be_committed': True,
            'workflow_dispatch_plaintext_inputs_forbidden': True,
            'issue_pr_comment_injection_forbidden': True,
            'chat_password_paste_not_required': True,
        },
        'runtime_material_validation': materials,
        'optional_session_presence': optional,
        'material_state': material_state,
        'missing_required_secrets': missing,
        'bad_format_secrets': bad_format,
        'github_actions_secret_control_probe': control,
        'classification': classification,
        'remaining_blocker': blocker,
        'next_capability': 'HorseRacing.BetfairSecretControlPlaneActivation' if blocker else 'HorseRacing.FirstImmutablePreOffPaperSnapshot',
        'governance': {
            'sentinel_only_control_plane_probe': True,
            'sentinel_contains_no_sensitive_material': True,
            'orders_forbidden': True,
            'live_key_activation_forbidden': True,
            'no_strategy_changes': True,
        },
    }
    (OUT / 'status.json').write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(status, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
