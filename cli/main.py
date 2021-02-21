from os import path
from cryptography_helpers import AESCipher, sha256_string
from getpass import getpass
import json
import click

data_file = 'data.json'

def get_password():
    if not path.exists(data_file):
        password_input1, password_input2 = 1, 2

        while password_input1 != password_input2:
            password_input1 = getpass('New Password:')
            password_input2 = getpass('Confirm Password:')

            if password_input1 != password_input2:
                print('Passwords did not match, please try again.')
        
        file = open(data_file, 'w')
        file_data = {
            'password_hash': sha256_string(password_input1)
        }
        file.write(json.dumps(file_data))

        return password_input1
    
    file = open(data_file, 'r')
    file_data = json.loads(file.readline())

    password_guess = getpass('Enter Password:')
    hashed_guess = sha256_string(password_guess)

    if hashed_guess != file_data['password_hash']:
        raise Exception('Incorrect Password.')
    
    return password_guess

def handle_read(password, account):
    file = open(data_file, 'r')
    file_data = json.loads(file.readline())

    if account in file_data:
        encrypted_data = file_data[account]
        cipher = AESCipher(password)
        data = cipher.decrypt(encrypted_data)

        print(f'Password for \'{account}\' is: \'{data}\'')
    else:
        print(f'No entry exists for {account}.')

def handle_write(password, account):
    file = open(data_file, 'r')
    file_data = json.loads(file.readline())

    account_pass1, account_pass2 = 1, 2
    while account_pass1 != account_pass2:
        account_pass1 = getpass(f'Enter password for \'{account}\':')
        account_pass2 = getpass(f'Confirm password for \'{account}\':')

        if account_pass1 != account_pass2:
            print('Passwords did not match, please try again.')

    cipher = AESCipher(password)
    file_data[account] = cipher.encrypt(account_pass1)

    file = open(data_file, 'w')
    file.write(json.dumps(file_data))

@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('access')
@click.argument('account')
def main(access, account):
    if access != '-r' and access != '-w':
        print('Must specify read/write access via -r or -w flag.')
        raise Exception('No access flag passed')

    password = get_password()

    if access == '-r': handle_read(password, account)
    else: handle_write(password, account)
        
if __name__ == '__main__':
    main()
