# Project Setup

## Requirements

1. **Java 21**  
   Download Java 21 from the [Oracle website](https://www.oracle.com/java/technologies/downloads/#java21).
   Download [JavaFX 21](https://gluonhq.com/products/javafx/)
3. **Python**  
   Install Python on your operating system:
   - **Mac**:  
     ```bash
     brew install python
     ```
   - **Windows**:  
     Download and install Python from [python.org](https://www.python.org/downloads/).
   - **Ubuntu**:  
     ```bash
     sudo apt update
     sudo apt install python3
     ```



4. **Git**  
   Clone the repository:  
   ```bash
   git clone https://github.com/phung1003/MM.git
   cd MM
   pip install -r requirements.txt
   ```
   
# Chạy project
1. **Run API**
   cd đến project API:
   ```bash
   cd MM/MM-API
   ```
   chạy API
   ```bash
   python main.py
   ```
3. **Chạy app Java
   cd đến file jar
   ```bash
   cd MM/MM-src/target
   ```
   chạy file jar với module-path là đường dẫn đến folder lib của javafx
   ```bash
   java --module-path <module-path> --add-modules javafx.controls,javafx.fxml -jar original-MM-1.0-SNAPSHOT.jar
   ```

