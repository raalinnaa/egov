import requests
import random

from utils.models import Address


def get_jwt_token():
    url = "http://hakaton-idp.gov4c.kz/auth/realms/con-web/protocol/openid-connect/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "username": "test-operator",
        "password": "DjrsmA9RMXRl",
        "client_id": "cw-queue-service",
        "grant_type": "password"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.json()["access_token"]


def get_random_request_id():
    # random_requests = [
    #     ("002241054097", "860904350504"),
    #     ("002241054795", "930823300880"),
    #     ("002241054954", "900319450997"),
    #     ("002241055082", "950905451464"),
    #     ("002241055257", "000430000049"),
    #     ("002241055387", "921123351335"),
    #     ("002241055659", "960217351422"),
    #     ("002241055886", "860729351086"),
    #     ("002241056742", "830730300232"),
    # ]
    # token = "eyJG6943LMReKj_kqdAVrAiPbpRloAfE1fqp0eVAJ-IChQcV-kv3gW-gBAzWztBEdFY"
    # url = "http://89.218.80.61/vshep-api/con-sync-service"
    # random_request = random.choice(random_requests)
    # print("Random request: ", random_request)
    # response = requests.get(f"{url}?requestId={random_request[0]}&requestIIN={random_request[1]}&token={token}")
    # return response.json()
    return ''.join(random.choice('0123456789') for i in range(12))


def send_sms(phone, message):
    token = get_jwt_token()
    url = "http://hak-sms123.gov4c.kz/api/smsgateway/send"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "phone": phone,
        "smsText": message
    }
    print(payload)
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.json()


def get_user_info(iin):
    token = get_jwt_token()
    url = f"http://hakaton-fl.gov4c.kz/api/persons/{iin}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_phone(iin):
    token = get_jwt_token()
    url = f"http://hakaton.gov4c.kz/api/bmg/check/{iin}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_request_message(random_request_id):
    random_request_id = "002241054954"
    url = f"hacknu://89.218.80.61/?requestId={random_request_id}"
    message = f"""Сіздің #{random_request_id} құжатыңыз дайын. 
{url} сілтемесін басу арқылы құжатты жеткізуді пайдалана аласыз. 
Құжатты жеткізу курьерлік қызметтің жеткізу мерзімдеріне сәйкес жүзеге асырылады. 
Ваш документ #{random_request_id} готов. 
Можете воспользоваться доставкой документа следуя по ссылке {url} 
Доставка осуществляется в соответствии со сроками доставки курьерской службы"""
    return message


def generate_otp():
    return ''.join(random.choice('0123456789') for i in range(6))


def get_data(A, B):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    params = {
        'origins': f'{A[1]},{A[0]}',
        'destinations': f'{B[1]},{B[0]}',
        'traffic_model': 'best_guess',
        'departure_time': 'now',
        'mode': 'driving',
    }
    API_KEY = 'AIzaSyD7s4PzstYghKQt9a6SkIbv8PkSzWIOhSQ'
    for key, value in params.items():
        url += key + '=' + value + '&'
    url += 'key=' + API_KEY

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)


    return response.json()


def get_longitude_longitude(address_id: Address):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = {
        'address': f'Kazakhstan, {address_id.oblast}, {address_id.city}, {address_id.street}, {address_id.entrance}, {address_id.house_number}',
        'key': 'AIzaSyD7s4PzstYghKQt9a6SkIbv8PkSzWIOhSQ'
    }
    for key, value in params.items():
        url += key + '=' + value + '&'
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    if response.json()['status'] == 'ZERO_RESULTS':
        return None, None

    latitude = response.json()['results'][0]['geometry']['location']['lat']
    longitude = response.json()['results'][0]['geometry']['location']['lng']

    return longitude, latitude
