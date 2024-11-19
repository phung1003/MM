package com.example.mm;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.io.IOException;
import java.math.BigInteger;

public class ECC {
    private Stage stage;
    private Scene scene;
    private Parent root;

    @FXML
    private Button generate;
    @FXML
    private Button encrypt;
    @FXML
    private Button sign;
    @FXML
    private Button decrypt;
    @FXML
    private Button verified;
    @FXML
    private TextField a;
    @FXML
    private TextField b;
    @FXML
    private TextField p;
    @FXML
    private TextField order;
    @FXML
    private TextField private_key;
    @FXML
    private TextField public_key;
    @FXML
    private TextField generator;
    @FXML
    private TextField message;
    @FXML
    private TextField result;
    @FXML
    private TextField result2;

    BigInteger[] generator_value;
    BigInteger[] public_key_value;
    BigInteger[] sign_value;
    ECC_API.ECCEncryptResult encrypt_result;

    private String arrToString(BigInteger[] arr) {
        StringBuilder str = new StringBuilder("(");
        for (int i = 0; i < arr.length; i++) {
            str.append(arr[i]);
            if (i < arr.length - 1) {
                str.append(", ");
            }
        }
        str.append(")");
        return str.toString();
    }

    @FXML
    void generate(ActionEvent event) {
        try {
            BigInteger a_value = new BigInteger(a.getText());
            BigInteger b_value = new BigInteger(b.getText());
            BigInteger p_value = new BigInteger(p.getText());
            BigInteger private_key_value = new BigInteger(private_key.getText());

            BigInteger[] result = ECC_API.eccGen(p_value, a_value, b_value, private_key_value);

            BigInteger gx = result[0];
            BigInteger gy = result[1];
            generator_value = new BigInteger[]{gx, gy};

            generator.setText(arrToString(generator_value));

            BigInteger pubx = result[2];
            BigInteger puby = result[3];
            public_key_value = new BigInteger[]{pubx, puby};
            public_key.setText(arrToString(public_key_value));
            

            BigInteger order_value = result[5];
            order.setText(order_value.toString());

            encrypt.setDisable(false);
            decrypt.setDisable(false);
            sign.setDisable(false);
            verified.setDisable(false);
        }catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }

    @FXML
    public void encrypt(ActionEvent event) {
        try {
            BigInteger a_value = new BigInteger(a.getText());
            BigInteger b_value = new BigInteger(b.getText());
            BigInteger p_value = new BigInteger(p.getText());
            String message_value = message.getText();

            ECC_API api = new ECC_API();
            encrypt_result = api.eccEncrypt(p_value, a_value, b_value, generator_value, public_key_value, message_value);

            StringBuilder str = new StringBuilder("[");
            str.append(arrToString(encrypt_result.encrypt[0]));
            str.append(", ");
            str.append(arrToString(encrypt_result.encrypt[1]));
            str.append("]");

            result.setText(str.toString());

            verified.setDisable(true);
            decrypt.setDisable(false);
        }catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }

    @FXML void decrypt(ActionEvent event) {
        try {
            BigInteger a_value = new BigInteger(a.getText());
            BigInteger b_value = new BigInteger(b.getText());
            BigInteger p_value = new BigInteger(p.getText());
            BigInteger private_key_value = new BigInteger(private_key.getText());
            String result_value = ECC_API.eccDecrypt(p_value, a_value, b_value, generator_value, private_key_value, encrypt_result);
            result2.setText(result_value);
        } catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }
    @FXML void sign(ActionEvent event) {
        try {
            BigInteger a_value = new BigInteger(a.getText());
            BigInteger b_value = new BigInteger(b.getText());
            BigInteger p_value = new BigInteger(p.getText());
            String message_value = message.getText();
            BigInteger q_value = new BigInteger(order.getText());
            BigInteger private_key_value = new BigInteger(private_key.getText());
            sign_value = ECC_API.eccSign(p_value, a_value, b_value, generator_value, q_value, private_key_value, message_value);
            result.setText(arrToString(sign_value));

            decrypt.setDisable(true);
            verified.setDisable(false);
        } catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }

    @FXML void verified(ActionEvent event) {
        try {
            BigInteger a_value = new BigInteger(a.getText());
            BigInteger b_value = new BigInteger(b.getText());
            BigInteger p_value = new BigInteger(p.getText());
            String message_value = message.getText();
            BigInteger q_value = new BigInteger(order.getText());
            Boolean verified_value = ECC_API.eccVerified(p_value, a_value, b_value, generator_value, q_value, public_key_value, message_value, sign_value);
            result2.setText(verified_value.toString());
        } catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }



    @FXML void back(ActionEvent event) throws IOException {
        Parent root = FXMLLoader.load(getClass().getResource("main-menu.fxml"));
        stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        scene = new Scene(root, 900, 700);
        stage.setScene(scene);
        stage.show();
    }

    @FXML
    private Label error;
    @FXML
    private VBox errorBox;

    @FXML void exit(ActionEvent event) {
        errorBox.setVisible(false);
    }

}
