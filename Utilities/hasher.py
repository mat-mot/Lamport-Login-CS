import hashlib


def set_password(user, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    for _ in range(user.repetitions - 1):
        hashed_password = hashlib.sha256(hashed_password.encode('utf-8')).hexdigest()
    user.password = hashed_password
    return


def check_password(user, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password == user.password


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password
