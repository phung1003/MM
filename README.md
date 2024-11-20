# Tổng quan về project
## Sử dụng 
   Project bao gồm 3 hệ mật RSA, Elgama và ECC Elgama. 
   Đối với mỗi hệ mật, nhập các thành phần khởi tạo cần thiết và bấm generate để tạo hệ mật: 
   - RSA: Nhập `p`, `q` là số nguyên tố 
   - Elgama: Nhập `p` là số nguyên tố và `private key` là một số ngẫu nhiên nhỏ hơn `p`
   - ECC Elgama: Nhập `p` là số nguyên tố, `a` và `b` thoả mãn $4a^3 + 27b^2 \neq 0 \mod p$, `private key` là một số ngẫu nhiên nhỏ hơn `p` 
   Sau khi đã tạo xong hệ mật, nhập message là các kí tự thuộc bảng chữ cái latin, các chữ số, dấu cách, phẩy, chấm.
   Có thể thêm chạy trực tiếp code python ở các file RSA.py, Elgama.py, ECC.py. 
## Cải tiến so với code trước
   - Thêm phần giao diện bằng javafx. 
   - Có thể mã hoá các bản tin `m` lớn dù cho hệ mật nhỏ bằng cách tính modulo, cụ thể:
     + Tính modulo của bản tin `m`:  
        $a = m \mod p$  
        $k = m \div p$  
     + Mã hoá bản tin `a`:  
       $y_a = encrypt(a)$
     + Giải mã $y_a$, tính `m`:  
        $m = kp+a$
   

# Project Setup


1. **Java 21**  
   Download Java 21 tại [Oracle website](https://www.oracle.com/java/technologies/downloads/#java21).  
   Download [JavaFX 21](https://gluonhq.com/products/javafx/).
3. **Python**  
   Cài đặt Python:
   - **Mac**:  
     ```bash
     brew install python
     ```
   - **Windows**:  
     Download Python tại [python.org](https://www.python.org/downloads/).
   - **Ubuntu**:  
     ```bash
     sudo apt update
     sudo apt install python3
     ```



4. **Git**  
   Clone repository:  
   ```bash
   git clone https://github.com/phung1003/MM.git
   cd MM
   pip install -r requirements.txt
   ```
   
# Chạy project
1. **Chạy API**  
   Chuyển đến project API:
   ```bash
   cd MM/MM-API
   ```
   chạy API
   ```bash
   python main.py
   ```
2. **Chạy App Java**  
   Chuyển đến file jar:
   ```bash
   cd MM/MM-src/target
   ``` 
   Chạy file jar với module-path là đường dẫn đến folder lib của javafx
   ```bash
   java --module-path <module-path> --add-modules javafx.controls,javafx.fxml -jar original-MM-1.0-SNAPSHOT.jar
   ```

