#Kí ECC và Mã hoá ECC-Elgama
import random
from sympy.ntheory import legendre_symbol
from sympy import isprime, nextprime
from math import isqrt, gcd
import random
# Hàm tính toán modulo nghịch đảo
def mod_inv(a, p):
    return pow(a, p - 2, p)

def choose_k(p):
   
    while True:
        k = random.randint(1, p - 1)  # Chọn k ngẫu nhiên trong [1, p-2]
        if gcd(k, p) == 1:  # Kiểm tra điều kiện gcd
            return k 

# Hàm băm đơn giản, chuyển đổi chuỗi ký tự thành số
def simple_hash(txt):
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

def find_points_on_curve(a, b, p):
    points = []
    
    for x in range(p):
        rhs = (x**3 + a*x + b) % p  # vế phải y^2 = x^3 + ax + b mod p
        # Dùng ký hiệu Legendre để kiểm tra có bao nhiêu nghiệm y
        if legendre_symbol(rhs, p) == 1:
            # Tìm các nghiệm y của phương trình y^2 = rhs mod p
            for y in range(1, p):
                if (y * y) % p == rhs:
                    points.append((x, y))
                    points.append((x, p - y))  # Thêm cả (x, -y)
        elif legendre_symbol(rhs, p) == 0:
            points.append((x, isqrt(rhs)))  # Nếu rhs là một bình phương hoàn hảo, thêm một nghiệm

    # Thêm điểm vô cực (None đại diện cho điểm vô hạn)
    points.append((None, None))
    
    return points

def find_point_with_given_x(a, b, p, x):
    original_x = x  # Lưu giá trị ban đầu của x
    while True:
        rhs = (x**3 + a*x + b) % p  # Tính giá trị vế phải của phương trình
        # Kiểm tra xem rhs có phải là bình phương (có nghiệm y) hay không
        if legendre_symbol(rhs, p) == 1:
            for y in range(p):
                if (y * y) % p == rhs:
                    return (x, y, (x - original_x) % p)  # Trả về x, y, chênh lệch
        elif legendre_symbol(rhs, p) == 0:
            return (x, isqrt(rhs), (x - original_x) % p)  # Trả về x, y, chênh lệch
        x = (x + 1) % p  # Không có nghiệm y với x cho trước


# def legendre_symbol(a, p):
#     """Tính ký hiệu Legendre (a/p)."""
#     return pow(a, (p - 1) // 2, p)

# def isqrt(n):
#     """Tính căn bậc hai nguyên của n."""
#     return int(n**0.5)

def find_point_up_to_i(a, b, p, i):
    """Tìm điểm thứ i trên đường cong y^2 = x^3 + ax + b mod p."""
    point_count = 0  # Biến đếm số điểm đã tìm thấy

    for x in range(p):
        rhs = (x**3 + a*x + b) % p  # vế phải y^2 = x^3 + ax + b mod p
        
        # Kiểm tra có nghiệm không
        if legendre_symbol(rhs, p) == 1:
            # Tìm các nghiệm y của phương trình y^2 = rhs mod p
            for y in range(1, p):
                if (y * y) % p == rhs:
                    point_count += 1
                    if point_count == i:
                        return (x, y)
                    point_count += 1
                    if point_count == i:
                        return (x, p - y)  # Trả về điểm (x, -y)
        elif legendre_symbol(rhs, p) == 0:
            point_count += 1
            if point_count == i:
                return (x, isqrt(rhs))  # Trả về điểm (x, y)

    # Nếu không tìm thấy điểm thứ i
    return None


def count_points_on_curve(a, b, p):
    count = 0
    for x in range(p):
        rhs = (x**3 + a*x + b) % p  # vế phải y^2 = x^3 + ax + b mod p
        # Dùng ký hiệu Legendre để kiểm tra có bao nhiêu nghiệm y
        if legendre_symbol(rhs, p) == 1:
            count += 2  # Có 2 nghiệm y
        elif legendre_symbol(rhs, p) == 0:
            count += 1  # Có 1 nghiệm y
    # Thêm 1 cho điểm vô hạn
    return count + 1


# Định nghĩa đường cong elliptic y^2 = x^3 + ax + b mod p
class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        # Kiểm tra điều kiện 4a^3 + 27b^2 != 0 mod p
        if (4 * a**3 + 27 * b**2) % p == 0:
            raise ValueError("Tham số a và b không hợp lệ: 4a^3 + 27b^2 phải khác 0 mod p.")

    # Kiểm tra xem điểm có thuộc đường cong không
    def is_on_curve(self, P):
        if P is None:
            return True
        x, y = P
        return (y ** 2) % self.p == (x ** 3 + self.a * x + self.b) % self.p

    # Phép cộng điểm trên đường cong
    def point_add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and y1 != y2:
            return None

        if x1 == x2:
            m = (3 * x1 * x1 + self.a) * mod_inv(2 * y1, self.p)
        else:
            m = (y2 - y1) * mod_inv(x2 - x1, self.p)

        m = m % self.p

        x3 = (m * m - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p

        return (x3, y3)

    # Phép nhân điểm với một số nguyên
    def point_mul(self, k, P):
        R = None
        N = P

        while k:
            if k & 1:
                R = self.point_add(R, N)
            N = self.point_add(N, N)
            k >>= 1

        return R

# ECC - Khóa công khai và riêng tư
class ECCKeyPair:
    def __init__(self, curve, G, x):
        self.curve = curve
        self.G = G
        self.private_key = x
        self.public_key = curve.point_mul(self.private_key, G)
        print("Public key", self.public_key)
        self.q = count_points_on_curve(curve.a, curve.b, curve.p)
        

    def sign(self, message):
        z = simple_hash(message)
        r, s = 0, 0
        while s == 0:
            k = 10
            x, _ = self.curve.point_mul(k, self.G)
            r = x % self.q
            s = ((z + r * self.private_key) * mod_inv(k, self.q)) % self.q

        return (r, s)

    def verify(self, message, signature, curve, G, public_key, q):
        r, s = signature
        z = simple_hash(message)

        w = mod_inv(s, q)
        u1 = (z * w) % q
        u2 = (r * w) % q
        P = curve.point_add(
            curve.point_mul(u1, G),
            curve.point_mul(u2, public_key)
        )

        if P is None:
            return False
        print(P)
        x, _ = P
        return r == x % q
    
    def encrypt(self, P_M, public_key, curve, G):
        k_A = 7209  # Khóa tạm thời của Alice
        print('k_A:', k_A)
        C1 = curve.point_mul(k_A, G)  # C1 = k_A * G
        C2 = curve.point_add(P_M, curve.point_mul(k_A, public_key))  # C2 = P_M + k_A * P_B
        return (C1, C2)

    def decrypt(self, msg):
        C1, C2 = msg
        temp = self.curve.point_mul(self.private_key, C1)  # k_B * C1
        # P_M = C2 - k_B * C1
        P_M = self.curve.point_add(C2, (temp[0], -temp[1] % self.curve.p))  # Phép trừ điểm
        return P_M







# aA = 1297
# bA = 2414
# pA = nextprime(2**15)
# print(pA)
# GA = find_point_up_to_i(aA,bA,pA,1) #Chọn điểm thứ 2 làm điểm sinh


# print(GA)
# try:
#     curveA = EllipticCurve(aA, bA, pA)
# except ValueError as e:
#     print(e)
#     exit()

# # Kiểm tra xem G có thuộc đường cong không
# if not curveA.is_on_curve(GA):
#     print("Điểm G không thuộc đường cong elliptic đã chọn.")
#     exit()

# A = ECCKeyPair(curveA, GA)

# message = "AN HUNG 2134,"
# print("Original MSG", simple_hash(message))
# x, y, diff = find_point_with_given_x(aA, bA, pA, simple_hash(message) % A.curve.p)
# point_msg = (x, y)
# k = simple_hash(message) // A.curve.p

# encrypted = A.encrypt(point_msg, A.public_key, A.curve, A.G)
# print("Original MSG point", point_msg)
# print("Encrypted", encrypted)
# print(k)
# decrypted = A.decrypt(encrypted)
# print(decrypted)
# decrypted_x = decrypted[0]-diff+k*A.curve.p
# print("Derypted", reverse_hashing(decrypted_x))


# # Ký một thông điệp

# signature = A.sign(message)

# print(f"Chữ ký cho thông điệp: {signature}")

# # Xác thực chữ ký
# is_valid = A.verify(message, signature, A.curve, A.G, A.public_key, A.q)
# print(f"Chữ ký hợp lệ: {is_valid}")



def ECC_gen(a, b, p, private_key):
    if not isprime(p):
        raise ValueError("p is not prime")
    try:
        curve = EllipticCurve(a, b, p)
    except ValueError as e:
        raise ValueError(str(e))
    
    G = find_point_up_to_i(a, b, p, 1)
    A = ECCKeyPair(curve, G, private_key)
    return A.G, A.private_key, A.public_key, A.q, A.curve.p

def ECC_encrypt(a, b, p, G, public_key, message):
    print("Original MSG", simple_hash(message))
    x, y, diff = find_point_with_given_x(a, b, p, simple_hash(message) % p)
    P_M = (x,y)
    k = simple_hash(message) // p
    k_A = random.randint(1, p-1)
    curve = EllipticCurve(a, b, p)
    C1 = curve.point_mul(k_A, G)  # C1 = k_A * G
    C2 = curve.point_add(P_M, curve.point_mul(k_A, public_key))  # C2 = P_M + k_A * P_B
    return diff, k, (C1, C2)

def ECC_decrypt(a, b, p, k, diff, private_key, encrypt):
    C1, C2 = encrypt
    curve = EllipticCurve(a, b, p)
    temp = curve.point_mul(private_key, C1)  # k_B * C1
    # P_M = C2 - k_B * C1
    P_M = curve.point_add(C2, (temp[0], -temp[1] % curve.p))  # Phép trừ điểm
    
    return reverse_hashing(P_M[0]-diff+k*p)

def ECC_sign(a, b, p, q, G, private_key, message):
    if not isprime(q):
        raise Exception("Can't sign because order is not prime")
    z = simple_hash(message)
    curve = EllipticCurve(a, b, p)
    r, s = 0, 0
    while s == 0:
        k = choose_k(q)
        x, _ = curve.point_mul(k, G)
        r = x % q
        s = ((z + r * private_key) * mod_inv(k, q)) % q
    return (r, s)

def ECC_verified(a, b, p, q, G, public_key, message, signature):
        r, s = signature
        z = simple_hash(message)
        curve = EllipticCurve(a, b, p)
        w = mod_inv(s, q)
        u1 = (z * w) % q
        u2 = (r * w) % q
        P = curve.point_add(
            curve.point_mul(u1, G),
            curve.point_mul(u2, public_key)
        )

        if P is None:
            return False
        print(P)
        x, _ = P
        return r == x % q

from sympy import nextprime
from ECC import ECC_gen, ECC_encrypt, ECC_decrypt, ECC_sign, ECC_verified

def test_ecc():
    # Bước 1: Sinh khóa ECC
    a = 1297  # Tham số a của đường cong
    b = 2414  # Tham số b của đường cong
    p = nextprime(2**15)  # Số nguyên tố p
    private_key = 123456  # Khóa bí mật của người dùng
    print(f"Sử dụng a = {a}, b = {b}, p = {p}, private_key = {private_key}")
    
    G, private_key, public_key, q, p = ECC_gen(a, b, p, private_key)
    print(f"Phần tử sinh (G): {G}")
    print(f"Khóa công khai (public_key): {public_key}")
    print(f"Khóa bí mật (private_key): {private_key}")
    
    # Bước 2: Mã hóa tin nhắn
    message = "HELLO"
    print(f"Tin nhắn ban đầu: {message}")
    
    diff, k, encrypted = ECC_encrypt(a, b, p, G, public_key, message)
    print(f"Mã hóa tin nhắn: diff = {diff}, k = {k}, mã hóa = {encrypted}")
    
    # Bước 3: Giải mã tin nhắn
    decrypted = ECC_decrypt(a, b, p, k, diff, private_key, encrypted)
    print(f"Tin nhắn sau khi giải mã: {decrypted}")
    
    # Bước 4: Ký số
    signature = ECC_sign(a, b, p, q, G, private_key, message)
    print(f"Chữ ký số: {signature}")
    
    # Bước 5: Xác minh chữ ký
    is_valid = ECC_verified(a, b, p, q, G, public_key, message, signature)
    print(f"Chữ ký hợp lệ: {is_valid}")
    
    # Kết quả cuối cùng
    print("\nTất cả kiểm tra đã hoàn thành.")
    if decrypted == message and is_valid:
        print("ECC hoạt động chính xác.")
    else:
        print("Có lỗi trong ECC.")

# Chạy kiểm tra
if __name__ == "__main__":
    test_ecc()
