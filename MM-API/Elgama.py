#Chữ ký ElGama
import random
from sympy import isprime, primitive_root, nextprime, mod_inverse
from math import gcd

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


def find_generator(p):
    """
    Tìm phần tử sinh g của nhóm Z_p*.
    """
    p_minus_1 = p - 1
    factors = set()
    # Phân tích (p-1) thành các thừa số nguyên tố
    d = 2
    n = p_minus_1
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    
    # Duyệt các phần tử từ 2 đến p-1
    for g in range(2, p):
        valid = True
        for factor in factors:
            # Kiểm tra g^(p-1)/factor mod p != 1
            if pow(g, p_minus_1 // factor, p) == 1:
                valid = False
                break
        if valid:
            return g
    return None  # Không tìm thấy (hiếm khi xảy ra với số nguyên tố)


def choose_k(p):
    
    while True:
        k = random.randint(1, p- 1)  # Chọn k ngẫu nhiên trong [1, p-2]
        if gcd(k, p) == 1:  # Kiểm tra điều kiện gcd
            return k  # Trả về k hợp lệ

def mod_exp(base, exp, mod):
    return pow(base, exp, mod)


class ElGamal:
    def __init__(self, bits, p, x = 10000):
        """Khởi tạo lớp ElGamal với số bit xác định."""
        if bits > 0:
          self.p = generate_prime(bits)  # Số nguyên tố
        else:
          self.p = p
        self.g = 2      # Phần tử sinh
        self.x = x # Khóa bí mật
        self.y = pow(self.g, self.x, self.p)  # Khóa công khai

    def encrypt(self, message, p, g, y):
        """Mã hóa một thông điệp bằng ElGamal."""
        message = hashing(message)
        k =  random.randint(2, p-1)# Chọn k ngẫu nhiên
        c1 = pow(g, k, p)  # c1 = alpha^k mod p
        s = pow(y, k, p)    # s = beta^k mod p
        c2 = (message * s) % p   # c2 = x * s mod p
        return (c1, c2)

    def decrypt(self, ciphertext):
        """Giải mã một thông điệp đã mã hóa bằng ElGamal."""
        c1, c2 = ciphertext
        s = pow(c1, self.x, self.p)  # s = c1^a mod p
        print(s)
        s_inv = mod_inverse(s, self.p)  # Tìm nghịch đảo của s
        print(s_inv)
        message = (c2 * s_inv) % self.p  # m = c2 * s_inv mod p
        return message

    def sign(self, message):
        """Tạo chữ ký bằng ElGamal."""
        k = random.randint(2, self.p-1)
        r = pow(self.g, k, self.p) # gamma alpha^k mod p
        s = (message - self.x * r) * mod_inverse(k, self.p - 1) % (self.p - 1) #sigma (x - a*r) * (k^-1 mod p-1) mod p-1
        return (r, s)

    def verify_signature(self, txt, r, s, p, g, y):
        """Xác minh chữ ký bằng ElGamal."""
        hashed = hashing(txt)
        v1 = pow(y, r, p) * pow(r, s, p) % p # (beta^r mod p) * (r^s mod p)
        v2 = pow(g, hashed, p) # alpha^m mod p với m là bản tin đc mã hoá
        print(v1, v2)
        v = v1 == v2
        return v


def generate_prime(bits):
    """Tìm số nguyên tố đầu tiên lớn hơn 2^bits."""
    # Tính giá trị tối thiểu cho số nguyên tố với số bit nhất định
    min_value = 1 << (bits - 1)  # 2^(bits - 1)
    # Tìm số nguyên tố lớn hơn min_value
    prime = nextprime(min_value)
    return prime

# A = ElGamal(150, 0)
# message = "HUY"

# print("Original Message:", hashing(message))

# encrypted = A.encrypt(message, A.p, A.g, A.y)
# print("Mã hoá bản tin :", encrypted)

# decrypted = A.decrypt(encrypted)
# print("Giải mã bản tin :", decrypted)

# signature = A.sign(hashing(message))
# print("Tạo chữ ký bằng khoá của A:", signature)

# verified = A.verify_signature(message, signature[0], signature[1], A.p, A.g, A.y)
# print("Xác minh chữ ký bằng khoá của A:", verified)

def Elgama_gen(x, p):
    if not isprime(p):
        raise ValueError("p is not prime")
    A = ElGamal(0, p, x)
    return A.g, A.x, A.y, A.p

def Elgama_encrypt(g, y, p, message):
    message = hashing(message)
    k =  random.randint(2, p-1)# Chọn k ngẫu nhiên
    c1 = pow(g, k, p)  # c1 = alpha^k mod p
    s = pow(y, k, p) 
    div = message // p   # s = beta^k mod p
    c2 = (message % p * s) % p   # c2 = x * s mod p
    return div, (c1, c2)
    

def Elgama_decrypt(x, p, k, message):
    c1, c2 = message
    s = mod_exp(c1, x, p)  # s = c1^a mod p
    print(s)
    s_inv = mod_inverse(s, p)  # Tìm nghịch đảo của s
    print(s_inv)
    message = (c2 * s_inv) % p  # m = c2 * s_inv mod p
    return reverse_hashing(message+k*p)

def Elgama_sign(x, g, p, message):
    message = hashing(message)
    k = choose_k(p-1)
    r = pow(g, k, p) # gamma alpha^k mod p
    s = (message - x * r) * mod_inverse(k, p - 1) % (p - 1) #sigma (x - a*r) * (k^-1 mod p-1) mod p-1
    return (r, s)

def Elgama_verified(g, y, p, sign, message):
    r, s = sign
    hashed = hashing(message)
    v1 = pow(y, r, p) * pow(r, s, p) % p # (beta^r mod p) * (r^s mod p)
    v2 = pow(g, hashed, p) # alpha^m mod p với m là bản tin đc mã hoá
    print(v1, v2)
    v = v1 == v2
    return v

def test_elgama():
    # Bước 1: Sinh khóa ElGama
    p = nextprime(1000)  # Số nguyên tố lớn hơn 1000
    x = 123  # Khóa bí mật
    print(f"Sử dụng p = {p}, x = {x}")
    
    g, private_key, public_key, p = Elgama_gen(x, p)
    print(f"Phần tử sinh (g): {g}")
    print(f"Khóa công khai (y): {public_key}")
    print(f"Khóa bí mật (x): {private_key}")
    
    # Bước 2: Mã hóa tin nhắn
    message = "HELLO"
    print(f"Tin nhắn ban đầu: {message}")
    
    k, encrypted = Elgama_encrypt(g, public_key, p, message)
    print(f"Mã hóa tin nhắn: k = {k}, mã hóa = {encrypted}")
    
    # Bước 3: Giải mã tin nhắn
    decrypted = Elgama_decrypt(private_key, p, k, encrypted)
    print(f"Tin nhắn sau khi giải mã: {decrypted}")
    
    # Bước 4: Ký số
    signature = Elgama_sign(private_key, g, p, message)
    print(f"Chữ ký số: {signature}")
    
    # Bước 5: Xác minh chữ ký
    is_valid = Elgama_verified(g, public_key, p, signature, message)
    print(f"Chữ ký hợp lệ: {is_valid}")
    
    # Kết quả cuối cùng
    print("\nTất cả kiểm tra đã hoàn thành.")
    if decrypted == message and is_valid:
        print("ElGama hoạt động chính xác.")
    else:
        print("Có lỗi trong ElGama.")

# Chạy kiểm tra
if __name__ == "__main__":
    test_elgama()



