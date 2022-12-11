from passlib.hash import pbkdf2_sha256

class Hash:
    def hash(password : str):
        return pbkdf2_sha256.hash(password)

    def verify(hashedPassword : str, plainPassword: str):
        return pbkdf2_sha256.verify(plainPassword,hashedPassword)
