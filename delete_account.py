import requests
import re
import os
from colorama import Fore

session = requests.Session()


def is_from_iran():
    print('Step [ 1 / 5 ] '.center(os.get_terminal_size().columns))

    ip_response = session.get('http://ip-api.com/json').json()

    if ip_response.get('countryCode') == 'IR':
        return True
    else:
        return False


def do_delete(stel_token: str, telegram_delete_hash: str):
    print('Step [ 6 / 6 ] '.center(os.get_terminal_size().columns))
    params = {'hash': telegram_delete_hash, 'message': 'Thank You Telegram'}
    headers = {'Cookie' 'stel_token=' + stel_token}
    do_delete_response = session.post(
        'https://my.telegram.org/deactivate/do_delete', headers=headers, params=params)
    print('Your Account is Succesfully Deleted')


def request_to_delete():
    print('Step [ 5 / 6 ] '.center(os.get_terminal_size().columns))
    cookies = session.cookies.get_dict()
    stel_token = cookies.get('stel_token')
    headers = {'Cookie': 'stel_token=' + stel_token}
    deactive_response = session.get(
        'https://my.telegram.org/deactivate', headers=headers)
    page = deactive_response.text
    regex = re.findall(r'hash: .+', page)
    telegram_delete_hash = (regex[0])[7:25]
    do_delete(stel_token, telegram_delete_hash)


def login(phone_number: str, random_hash: str):
    print('Step [ 4 / 6 ] '.center(os.get_terminal_size().columns))
    password = input('Please Enter The webcode sent to your Telegram : ')
    params = {'phone': phone_number,
              'random_hash': random_hash, 'password': password}
    login_request = session.post(
        'https://my.telegram.org/auth/login', params=params)
    if login_request:
        request_to_delete()
    else:
        print(f'{Fore.RED}something went Wrong, Please try again. ')
        exit()

    #print(f' login request {login_request.text}')


def send_password(phone_number: str):
    isFromIran = is_from_iran()
    if isFromIran:
        print(f'{Fore.RED}Your Region is iran and You nees to Use VPN')
        return
    params = {'phone': phone_number}
    #print(f'params is {params}')
    print('Step [ 3 / 6 ] '.center(os.get_terminal_size().columns))
    send_pass = session.post(
        'https://my.telegram.org/auth/send_password', params=params)

    print(f'{Fore.GREEN}Code Sent To your Telegram App! ')

    login(phone_number, send_pass.json().get('random_hash'))


if __name__ == '__main__':
    print('Step [ 1 / 6 ] '.center(os.get_terminal_size().columns))
    phone_number = input(
        'Please Enter Your Phone number? ( with your country code ) : ')

    send_password(phone_number)
