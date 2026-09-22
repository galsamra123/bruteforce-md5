import hashlib

PASSWORD = '525557'
LENGTH = 6

class Bruteforce:
    def __init__(self, password_hashed, length):
        self.password = password_hashed
        self.length = length

    def find(self, password_encoded, rng, length):
        password_try = str(rng[0]).zfill(length)
        for i in range(rng[0], rng[1] + 1):
            password_try_afterhsh = hashlib.md5(password_try.encode('utf-8')).hexdigest().upper()
            if password_try_afterhsh == password_encoded:
                return password_try
            password_try = str(int(password_try) + 1).zfill(length)
        return None

after_hash = hashlib.md5(PASSWORD.encode('utf-8')).hexdigest().upper()

# Create instance first, then call find()
bf_instance = Bruteforce(after_hash, LENGTH)
print(bf_instance.find(after_hash, (0, 600000), LENGTH))