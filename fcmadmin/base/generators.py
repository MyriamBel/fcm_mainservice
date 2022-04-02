import random
import string


def generate_checkoutterminal_login():
    length = 7
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.choice(letters_and_digits) for i in range(length))
    return rand_string


def generate_checkoutterminal_password():
    length = 10
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.choice(letters_and_digits) for i in range(length))
    return rand_string
