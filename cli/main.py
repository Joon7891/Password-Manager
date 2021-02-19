from os import path
from cryptography_helpers import AESCipher, sha256_string
from getpass import getpass
import json

data_file = 'data.json'

def main():
    password = ''
    if not path.exists(data_file):
        pass_input1, pass_input2 = 1, 2

        while pass_input1 != pass_input2:
            pass_input1 = getpass('New Password:')
            pass_input2 = getpass('Confirm Password:')

            if pass_input1 != pass_input2:
                print('Passwords did not match, please try again.')
            
            password = pass_input1
        
        file = open(data_file, 'w')
        pass_hash = sha256_string(password)        
        file_data = {
            'password_hash': pass_hash
        }
        file.write(json.dumps(file_data))
    
    else:
        file = open(data_file, 'r')
        file_data = json.loads(file.readline())

        pass_guess = getpass('Enter Password:')
        hashed_guess = sha256_string(pass_guess)

        if hashed_guess != file_data['password_hash']:
            print('Incorrect password.')
        else:
            print('Correct password.')

        
if __name__ == '__main__':
    main()