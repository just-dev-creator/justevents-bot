import urllib3
import certifi
import json
import uuid


def is_username_valid(username: str) -> bool:
    if (len(username)) < 3:
        return False
    req = create_request(username)
    req_data = req.data.decode('utf-8')
    return "BadRequestException" not in req_data


def get_uuid(username: str) -> uuid.UUID:
    req = create_request(username)
    req_data = req.data.decode('utf-8')
    json_d = json.loads(req_data)
    json_id = json_d["id"]
    user_uuid = uuid.UUID(json_id)
    return user_uuid


def create_request(username: str):
    url = "https://api.mojang.com/users/profiles/minecraft/"
    http_req = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    req = None
    try:
        req = http_req.request('GET', url + username)
    except urllib3.exceptions.SSLError as e:
        print(f"An error occurred while requesting the account {username}:\n" + str(e))
        return None

    return req


if __name__ == '__main__':
    print(str(is_username_valid("justde")))
