import random
import string
import cryptocode

letters_and_digits = string.ascii_letters + string.digits
digits = string.digits


def generate_pin():
    """
    Генерация пин-кодов сотрудникам заведений.
    """
    pin_string = ''.join(random.choice(digits) for i in range(4))
    return pin_string


def generate_random_string(leng):
    try:
        rand_string = ''.join(random.choice(letters_and_digits) for i in range(leng))
    except TypeError:
        raise TypeError("Only digits allowed.")
    return rand_string


def encrypt_string(to_encrypt):
    salt = generate_random_string(10)
    str_encoded = cryptocode.encrypt(to_encrypt, salt) + ":" + salt
    return str_encoded


def decrypt_string(to_decrypt):
    print(to_decrypt)
    text, salt = to_decrypt.split(":")
    str_decoded = cryptocode.decrypt(text, salt)
    print(str_decoded)
    return str_decoded


def generate_checkoutterminal_login():
    length = 7
    rand_string = generate_random_string(length)
    return rand_string


def generate_checkoutterminal_password():
    length = 10
    rand_string = generate_random_string(length)
    return rand_string


def generate_hash_string(*args):
    output = ''
    for i in args:
        output += str(i)
    return hash(output)
