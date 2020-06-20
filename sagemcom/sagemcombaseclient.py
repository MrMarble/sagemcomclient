import hashlib
import requests
import random
import json
from datetime import datetime, timezone, timedelta


class SagemcomBaseClient:
    def __init__(self, user: str, password: str, host: str = 'http://192.168.1.1'):
        self.sess = requests.session()
        self.path = '/cgi/json-req'
        self.id, self.sessId = (0, 0)
        self.lastNonce = ''
        self.datamodel = None
        self.setdatamodel()

        self.host = host
        self.user = user
        self.password = hashlib.md5(password.encode('utf-8')).hexdigest()

    def login(self):
        params = {
            "parameters": {
                "user": self.user,
                "persistent": "true",
                "session-options": {
                    "nss": self.datamodel['nss'],
                    "language": "ident",
                    "context-flags": {
                        "get-content-name": True,
                        "local-time": True
                    },
                    "capability-depth": 2,
                    "capability-flags": {
                        "name": True,
                        "default-value": True,
                        "restriction": True,
                        "description": True
                    },
                    "time-format": "ISO_8601",
                    "write-only-string": "_XMO_WRITE_ONLY_",
                    "undefined-write-only-string": "_XMO_UNDEFINED_WRITE_ONLY_"
                }
            }
        }
        result = self._request(self._createAction('logIn', params), True)
        self.sessId = result['parameters']['id']
        self.lastNonce = result['parameters']['nonce']

    def setdatamodel(self, model: dict = None):
        if model is None:
            self.datamodel = {
                "name": 'Internal',
                "nss": [
                    {
                        "name": "gtw",
                        "uri": "http://sagemcom.com/gateway-data"
                    }
                ]
            }
        else:
            self.datamodel = model

    def _createAction(self, method: str, params: dict) -> list:
        action = {
            "id": 0,
            "method": method
        }
        action.update(params)
        return [action]

    def _request(self, action: list, priority: bool = False) -> dict:
        auth = self._getauth()
        body = {"request": {"id": self.id, "session-id": self.sessId, "priority": priority, "actions": action,
                            "cnonce": auth['cnonce'], "auth-key": auth['auth-key']}}
        cookie = self._getcookie(auth['ha1'], auth['cnonce'])
        self.id += 1
        r = self.sess.post(f'{self.host}{self.path}', data={"req": json.dumps(body)}, cookies=cookie)

        if r.status_code == 200:
            response = r.json()
            if response['reply']['error']['description'] == 'XMO_REQUEST_NO_ERR':
                return response['reply']['actions'][0]['callbacks'][0]
        raise Exception('Authentication error')

    def _getcookie(self, ha1: str, nonce: int) -> dict:
        expires = datetime.now(timezone.utc) + timedelta(days=1)
        cookie = {
            "name": "session",
            "value": json.dumps({
                "req_id": self.id,
                "sess_id": self.sessId,
                "basic": False,
                "user": self.user,
                "dataModel": self.datamodel,
                "ha1": f'{ha1[:10]}{self.password}{ha1[:10]}',
                "nonce": nonce
            }),
            "expires": expires.strftime("%Y%m%d"),
            "path": '/'
        }
        return cookie

    def _getauth(self) -> dict:
        current_nonce = random.randint(0, 4294967295)
        ha1 = hashlib.md5(f'{self.user}:{self.lastNonce}:{self.password}'.encode('utf-8')).hexdigest()
        self.lastNonce = current_nonce
        return {
            "ha1": ha1,
            "cnonce": current_nonce,
            "auth-key": hashlib.md5(f'{ha1}:{self.id}:{current_nonce}:JSON:{self.path}'.encode('utf-8')).hexdigest()
        }
