from passlib.hash import bcrypt
def encrypt_password(password):
    hashed_password = bcrypt.hash(password)  # Generar el hash bcrypt
    return hashed_password

print(encrypt_password("Admin"))