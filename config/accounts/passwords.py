from random import randint


def one_time_password() -> str:
    return str(randint(100000000, 999999999))
