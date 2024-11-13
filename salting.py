import bcrypt

password = b"PrashantTakeOver@5399"

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)

print("Salt :")
print(salt)

print("Hashed")
print(hashed)

import hashlib

# Declaring Password
password = "PrashantTakeOver@5399"
# adding 5gz as password
salt = "PassWordSalt"

# Adding salt at the last of the password
dataBase_password = password + salt
# Encoding the password
hashed = hashlib.md5(dataBase_password.encode())

# Printing the Hash
print(hashed.hexdigest())

from argon2 import PasswordHasher
password = b"PrashantTakeOver@5399"
ph = PasswordHasher()
hash_text = ph.hash("correct horse battery staple")
print(hash_text)
ph.verify(hash_text, "correct horse battery staple")
ph.check_needs_rehash(hash_text)
ph.verify(hash_text, "Tr0ub4dor&3")
