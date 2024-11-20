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
    
def test_rsa():
    # Bước 1: Sinh khóa RSA
    p = nextprime(61)  # Số nguyên tố đầu tiên lớn hơn 61
    q = nextprime(53)  # Số nguyên tố đầu tiên lớn hơn 53
    print(f"Sử dụng p = {p}, q = {q}")
    
    e, d, n = RSA_gen(p, q)
    print(f"Khóa công khai (e, n): ({e}, {n})")
    print(f"Khóa bí mật (d): {d}")
    
    # Bước 2: Mã hóa tin nhắn
    message = "HELLO"
    print(f"Tin nhắn ban đầu: {message}")
    
    k, encrypted = RSA_encrypt(e, n, message)
    print(f"Mã hóa tin nhắn: k = {k}, mã hóa = {encrypted}")
    
    # Bước 3: Giải mã tin nhắn
    decrypted = RSA_decrypt(d, n, k, encrypted)
    print(f"Tin nhắn sau khi giải mã: {decrypted}")
    
    # Bước 4: Ký số
    k_sign, signature = RSA_sign(d, n, message)
    print(f"Chữ ký số: k = {k_sign}, chữ ký = {signature}")
    
    # Bước 5: Xác minh chữ ký
    verified_hash, is_valid = RSA_verified(e, n, k_sign, signature, message)
    print(f"Hash từ chữ ký: {verified_hash}")
    print(f"Chữ ký hợp lệ: {is_valid}")
    
    # Kết quả cuối cùng
    print("\nTất cả kiểm tra đã hoàn thành.")
    if decrypted == message and is_valid:
        print("RSA hoạt động chính xác.")
    else:
        print("Có lỗi trong RSA.")

# Chạy kiểm tra
if __name__ == "__main__":
    test_rsa()

