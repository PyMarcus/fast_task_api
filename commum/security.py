import bcrypt


def hash_password(password: str) -> str:
    pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return pw.decode('utf-8')


