from RSA import RSA_gen, RSA_encrypt, RSA_decrypt, RSA_sign, RSA_verified
from Elgama import Elgama_gen, Elgama_encrypt, Elgama_decrypt, Elgama_sign, Elgama_verified
from ECC import ECC_gen, ECC_encrypt, ECC_decrypt, ECC_sign, ECC_verified
from flask import Flask, request, json, session, jsonify

app = Flask(__name__)

@app.route('/rsa/gen', methods = ['POST'])
def rsa_init():
    data = request.json
    p = data.get("p")
    q = data.get("q")
    try:
        e, d, n = RSA_gen(p, q)
        result = {'e': e, 'd': d, 'n': n}
        return jsonify(result), 200
    
    except ValueError as ve:
        return str(ve), 400
    except Exception as ex:
        return str(ex), 400

@app.route('/rsa/encrypt', methods = ['POST'])
def rsa_encrypt():
    data = request.json
    e = data.get("e")
    n = data.get("n")
    message = data.get("message")
    
    try:
        k, encrypted = RSA_encrypt(e, n, message)
        result = {'k': k, 'encrypted': encrypted}
        return jsonify(result), 200
    
    except ValueError as ve:
        return str(ve), 400
    except Exception as ex:
        return str(ex), 400

@app.route('/rsa/decrypt', methods = ['POST'])
def rsa_decrypt():
    data = request.json
    d = data.get("d")
    n = data.get("n")
    k = data.get("k")
    try:
        encrypted = data.get("encrypt")
        decrypted = RSA_decrypt(d, n, k, encrypted)
        result = {'message': decrypted}
        return jsonify(result), 200
    except ValueError as ve:
        return str(ve), 400
    except Exception as ex:
        return str(ex), 400

@app.route('/rsa/sign', methods = ['POST'])
def rsa_sign():
    data = request.json
    d = data.get("d")
    n = data.get("n")
    message = data.get("message")
    
    try:
        k, sign = RSA_sign(d, n, message)
        result = {'k': k, 'sign': sign}
        return jsonify(result), 200
    
    except ValueError as ve:
        return str(ve), 400
    except Exception as ex:
        return str(ex), 400

@app.route('/rsa/verified', methods = ['POST'])
def rsa_verified():
    data = request.json
    e = data.get("e")
    n = data.get("n")
    k = data.get("k")
    sign = data.get("sign")
    message = data.get("message")
    try:
        sign_decrypted, verified = RSA_verified(e, n, k, sign, message)
        result = {'sign_decrypted': sign_decrypted, 'verified': verified}
        return jsonify(result)
    except Exception as ex:
        return str(ex), 400

@app.route('/elgama/gen', methods = ['POST'])
def elgama_gen():
    data = request.json
    p = data.get("p")
    private_key = data.get("private_key")
    try:
        g, private_key, public_key, p = Elgama_gen(private_key, p)
        result = {'private_key': private_key, 'g': g, 'public_key': public_key, 'p': p}
        return jsonify(result), 200
    
    except ValueError as ve:
        return str(ve), 400
    except Exception as ex:
        return str(ex), 400


@app.route('/elgama/encrypt', methods = ['POST'])
def elgama_encrypt():
    data = request.json
    p = data.get("p")
    public_key = data.get("public_key")
    g = data.get("g")
    message = data.get("message")
    
    try:
        k, encrypted = Elgama_encrypt(g, public_key, p, message)
        result = {'k': k, 'encrypted': encrypted}
        return jsonify(result), 200
    
    except ValueError as ve:
        return str(ve), 400
    except Exception as ex:
        return str(ex), 400
    
@app.route('/elgama/decrypt', methods = ['POST'])
def elgama_decrypt():
    data = request.json
    p = data.get("p")
    k = data.get("k")
    private_key = data.get("private_key")
    encrypted = data.get("encrypted")
    try:
        decrypted = Elgama_decrypt(private_key, p, k, encrypted)
        result = {'message': decrypted}
        return jsonify(result)
    except Exception as ex:
        return str(ex), 400

@app.route('/elgama/sign', methods = ['POST'])
def elgama_sign():
    data = request.json
    private_key = data.get("private_key")
    g = data.get("g")
    p = data.get("p")
    message = data.get("message")
    try:
        sign = Elgama_sign(private_key, g, p, message)
        result = {'sign': sign}
        return jsonify(result)
    except Exception as ex:
        return str(ex), 400

@app.route('/elgama/verified', methods = ['POST'])
def elgama_verified():
    data = request.json
    p = data.get("p")
    g = data.get("g")
    public_key = data.get("public_key")
    sign = data.get("sign")
    message = data.get("message")
    data = request.json
    try:
        verified = Elgama_verified(g, public_key, p, sign, message)
        result = {'verified': verified
        }
        return jsonify(result)
    except Exception as ex:
        return str(ex), 400


@app.route('/ecc/gen', methods = ['POST'])
def ecc_gen():
    data = request.json
    p = data.get("p")
    a = data.get("a")
    b = data.get("b")
    private_key = data.get("private_key")
    try:
        G, private_key, public_key, q, p = ECC_gen(a, b, p, private_key)
        result = {"G": G, "private_key": private_key, "public_key": public_key, "point_number": q, "p": p}
        return jsonify(result)
    
    except Exception as ex:
        return str(ex), 400

@app.route('/ecc/encrypt', methods = ['POST'])
def ecc_encrypt():
    data = request.json
    a = data.get("a")
    b = data.get("b")
    p = data.get("p")
    G = data.get("G")
    public_key = data.get("public_key")
    message = data.get("message")
    try: 
        diff, k,  encrypt = ECC_encrypt(a, b, p, G, public_key, message)
        return ({"encrypt": encrypt, "diff": diff, "k": k})
    except Exception as ex:
        return str(ex), 400

@app.route('/ecc/decrypt', methods = ['POST'])
def ecc_decrypt():
    data = request.json
    a = data.get("a")
    b = data.get("b")
    p = data.get("p")
    G = data.get("G")
    diff = data.get("diff")
    k = data.get("k")
    private_key = data.get("private_key")
    encrypt = data.get("encrypt")
    try:
        decrypt = ECC_decrypt(a, b, p, k, diff, private_key, encrypt)
        return ({"message": decrypt})
    except Exception as ex:
        return str(ex), 400

@app.route('/ecc/sign', methods = ['POST'])
def ecc_sign():
    data = request.json
    a = data.get("a")
    b = data.get("b")
    p = data.get("p")
    G = data.get("G")
    q = data.get("q")
    private_key = data.get("private_key")
    message = data.get("message")
    try:
        sign = ECC_sign(a, b, p , q, G, private_key, message)
        return({"sign": sign})
    except Exception as ex:
        return str(ex), 400

@app.route('/ecc/verified', methods = ['POST'])
def ecc_verified():
    data = request.json
  
    a = data.get("a")
    b = data.get("b")
    p = data.get("p")
    G = data.get("G")
    q = data.get("q")
    public_key = data.get("public_key")
    message = data.get("message")
    sign = data.get("sign")
    try:
        verified = ECC_verified(a, b, p, q, G, public_key, message, sign)
        return({"verified": verified})
    except Exception as ex:
        return str(ex), 400

if __name__ == '__main__':
    app.run()
