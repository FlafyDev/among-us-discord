import requests
import base64
from urllib.parse import urljoin

class FormattedKey:
    def __init__(self,  key):
        key = key.strip()

        self.data = base64.b64decode(key.encode("utf-8")).decode("utf-8").split("$")
        self.data_base64 = key

        self.url = self.data[0]
        self.secret_key = self.data[1]
        self.secret_key_base64 = base64.b64encode(self.secret_key.encode("utf-8")).decode("utf-8")

def valid_and_different_key(new_key, old_key=""):
    if new_key == "":
        return False

    try:
        new_key = FormattedKey(new_key)
    except:
        return False

    print(new_key.secret_key, len(new_key.secret_key))

    if len(new_key.secret_key) != 8:
        return False

    if old_key == "":
        return True

    try:
        old_key = FormattedKey(old_key)
    except:
        return True

    return old_key.data != new_key.data

class Communicator:
    def __init__(self, secret_key):
        self.key = FormattedKey(secret_key)

    def set_mute(self, mute):
        print("mute set to", mute)
        try:
            return requests.post(urljoin(self.key.url, 'mute'), params={
                "secret": self.key.secret_key_base64,
                "mute": str(int(mute))
            }).status_code == 200
        except Exception as e:
            print("Mute request failed.", e)
            return False

    def set_code(self, room_code):
        try:
            return requests.post(urljoin(self.key.url, 'roomCode'), params={
                "secret": self.key.secret_key_base64,
                "roomCode": room_code
            }).status_code == 200
        except Exception as e:
            print("Room code request failed.", e)
            return False

    def test_server(self):
        try:
            req =  requests.post(urljoin(self.key.url, 'check'), params={
                "secret": self.key.secret_key_base64
            })
            return req.status_code == 200, req.status_code
        except Exception as e:
            print("Test server request failed.", e)
            return False, None