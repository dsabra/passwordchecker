#project to check your passwords and see if has been leaked.
#will not show password on screen, just hash.

import requests
import hashlib
import sys
import stdiomask

#check api response 
def request_api_data(query_char):
	url= 'https://api.pwnedpasswords.com/range/' + query_char
	res= requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f'Error fetching: {res.status_code}, check api and try again.')
	return res

#compare user hash to hashes from api and see how many times password has been leaked
def get_password_leaks_count(hashes, hash_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h, count in hashes:
		if h == hash_to_check:
			return count
	return 0

#hash password, and split first 5 char from the rest for api. 
def pwned_api_check(password):
	sha1password= hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char, tail = sha1password[:5], sha1password[5:]
	response = request_api_data(first5_char)
	print(first5_char,tail)
	return get_password_leaks_count(response, tail)

#get password, run and return results
# def main(args):
# 	for password in args:
# 		count = pwned_api_check(password)
# 		if count:
# 			print(f'{password} was found {count} times. Change your password!')
# 		else:
# 			print(f"{password} was not found. Good job.")
# 		return 'Done!'

def main(args):
	for password in args:
		count = pwned_api_check(password)
		if count:
			print(f'Your password was found {count} times. Change your password!')
		else:
			print(f"Your password was not found. Good job.")
		return 'Done!'

#turn user input to ***, run then exit
if __name__ == '__main__':
    while True:
        password = stdiomask.getpass('Enter password to check: ')
        password_check = stdiomask.getpass('Enter password again: ')
        if (password == password_check):
            break
        print('Error:  Passwords do not match, please try again. \n')
    sys.exit(main([password]))