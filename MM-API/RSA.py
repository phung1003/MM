#chữ ký RSA
from sympy import nextprime, isprime
import math

# Reusing the hashing function
def hashing(txt):
    txt = txt.upper()
    ans = 0
    for c in txt:
        if c == ' ':
            value = 27  # Gán dấu cách là 27
        elif c == '.':
            value = 28  # Gán dấu chấm là 28
        elif c == ',':
            value = 29  # Gán dấu phẩy là 29
        elif '0' <= c <= '9':
            value = ord(c) - ord('0') + 30  # Gán số 0-9 từ 30 đến 39
        else:
            value = ord(c) - ord('A') + 1  # Gán A-Z từ 1 đến 26
        ans = ans * 40 + value  # Nhân 40 để có thêm không gian cho tất cả các ký tự
    return ans

def reverse_hashing(num):
    result = []
    while num > 0:
        value = (num - 1) % 40 + 1
        if value == 27:
            char = ' '  # Nếu là 27 thì là dấu cách
        elif value == 28:
            char = '.'  # Nếu là 28 thì là dấu chấm
        elif value == 29:
            char = ','  # Nếu là 29 thì là dấu phẩy
        elif 30 <= value <= 39:
            char = chr(value - 30 + ord('0'))  # Nếu từ 30-39 thì là các số 0-9
        else:
            char = chr(value - 1 + ord('A'))  # Nếu từ 1-26 thì là A-Z
        result.append(char)
        num = (num - 1) // 40
    return ''.join(result[::-1])  # Đảo chuỗi để trả về kết quả đúng





def modular_exponential(a, b, n):
    return pow(a, b, n)

class RSA:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = self.public_key()
        self.d = self.secret_key() % self.n

    def public_key(self):
        for i in range(max(self.p, self.q) + 1, self.n):
            if (math.gcd(i, self.phi) == 1):
                return i

    def secret_key(self):
        x, _ = self.dophatine_equation(self.e, self.phi)
        return x % self.phi

    def gcd_dophatine(self, a, b):
        if b == 0:
            return (1, 0)
        x1, y1 = self.gcd_dophatine(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (x, y)

    def dophatine_equation(self, a, b):
        x, _ = self.gcd_dophatine(a, b)
        return (x, 0)

    def encrypt(self, txt, e, n):
        hashed = hashing(txt)
        return modular_exponential(hashed, e, n)

    def decrypt(self, cipher, d, n):
        return modular_exponential(cipher, d, n)

    def sign(self, txt):
        hashed = hashing(txt)
        return modular_exponential(hashed, self.d, self.n)

    def verify_signature(self, signature, e, n):
        decrypted_hash = modular_exponential(signature, e, n)
        return decrypted_hash


# A generates RSA keys
# B = RSA(p=100000000003, q=100000000019)
# print("A's Public Key: (e = {}, n = {})".format(A.e, A.n))
# print("A's Private Key: d =", A.d)

# # B generates RSA keys

# print("B's Public Key: (e = {}, n = {})".format(B.e, B.n))
# print("B's Private Key: d =", B.d)

# # Step 2: A encrypts the message using B's public key
# message = "ANHUNG"
# encrypted_message = A.encrypt(message, B.e, B.n)
# print("Encrypted message from A to B:", encrypted_message)

# # Step 3: A signs the message using A's private key
# signature = A.sign(message)
# print("A's signature on the message:", signature)

# # Step 4: B decrypts the message using B's private key
# decrypted_message = B.decrypt(encrypted_message, B.d, B.n)
# print("Decrypted message by B:", decrypted_message)

# # Step 5: B verifies the signature
# verified_hash = B.verify_signature(signature, A.e, A.n)
# print("Verified hash:", verified_hash)

# expected_hash = hashing(message)
# print("Signature valid:", verified_hash == expected_hash)

def RSA_gen(p, q):
    if not isprime(p):
        raise ValueError("p is not prime")
    if not isprime(q):
        raise ValueError("q is not prime")
    A = RSA(p=p, q=q)
    return A.e, A.d, A.n

def RSA_encrypt(e, n, message):
    hashed = hashing(message)
    k = hashed // n
    return k, modular_exponential(hashed, e, n)
    
    

def RSA_decrypt(d, n, k, encrypted):
    return reverse_hashing(pow(encrypted, d, n)+k*n)

def RSA_sign(d, n, message):
    hashed = hashing(message)
    k = hashed // n
    return k, modular_exponential(hashed, d, n)#chuyển số thành chữ


def RSA_verified(e, n, k, sign, message):
    message = hashing(message)
    verified = pow(sign, e, n)+k*n
    return verified, message == verified
    
# A = RSA(p=nextprime(2**2048), q=nextprime(p))

# message = "ANHUNG"
# encrypted_message = A.encrypt(message, A.e, A.n)
# print("Encrypted message from A:", encrypted_message)
# decrypted_message = A.decrypt(encrypted_message, A.d, A.n)
# print("Decrypted message by A:", decrypted_message)

# signature = A.sign(message)
# print("A's signature on the message:", signature)
# verified_hash = A.verify_signature(signature, A.e, A.n)
# print("Verified hash:", verified_hash)

# print(reverse_hashing(hashing("ABC")))    # AZ

