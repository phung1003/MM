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

public class Elgama {
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
    private TextField p;
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

    BigInteger[] encrypt_value = null;
    BigInteger[] sign_value = null;
    BigInteger k;

    @FXML
    void generate(ActionEvent event) {
        try {
            BigInteger p_value = new BigInteger(p.getText());
            BigInteger private_key_value = new BigInteger(private_key.getText());
            BigInteger[] keys = Elgama_API.elgamaGen(p_value, private_key_value);
            BigInteger generator_value = keys[0];
            BigInteger public_key_value = keys[1];
            // Display results in the GUI
            generator.setText(generator_value.toString());
            public_key.setText(public_key_value.toString());


            encrypt.setDisable(false);
            sign.setDisable(false);
            decrypt.setDisable(false);
            verified.setDisable(false);

        } catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }

    @FXML
    void encrypt(ActionEvent event) {
        try {
            BigInteger p_value = new BigInteger(p.getText());
            BigInteger public_key_value = new BigInteger(public_key.getText());
            String message_value = message.getText();
            BigInteger generator_value = new BigInteger(generator.getText());

            Elgama_API elgamaApi = new Elgama_API();
            Elgama_API.ElagamaEncryptResult elgamaEncrypt = elgamaApi.elgamaEncrypt(p_value, public_key_value, generator_value, message_value);

            encrypt_value = elgamaEncrypt.encrypt;
            k = elgamaEncrypt.k;

            StringBuilder str = new StringBuilder("(");
            for (int i = 0; i < encrypt_value.length; i++) {
                str.append(encrypt_value[i]);
                if (i < encrypt_value.length - 1) {
                    str.append(", ");
                }
            }
            str.append(")");
            String formattedString = str.toString();

            result.setText(formattedString);
            verified.setDisable(true);
            decrypt.setDisable(false);
        } catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }

    @FXML
    void decrypt(ActionEvent event) {
        try {
            BigInteger p_value = new BigInteger(p.getText());
            BigInteger private_key_value = new BigInteger(private_key.getText());

            String result_value = Elgama_API.elgamaDecrypt(p_value, private_key_value, k, encrypt_value);
            result2.setText(result_value);
        } catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }

    @FXML
    void sign(ActionEvent event) {
        try {
            BigInteger p_value = new BigInteger(p.getText());
            BigInteger private_key_value = new BigInteger(private_key.getText());
            BigInteger generator_value = new BigInteger(generator.getText());
            String message_value = message.getText();
            sign_value = Elgama_API.elgamaSign(p_value, generator_value, private_key_value, message_value);
            StringBuilder str = new StringBuilder("(");
            for (int i = 0; i < sign_value.length; i++) {
                str.append(sign_value[i]);
                if (i < sign_value.length - 1) {
                    str.append(", ");
                }
            }
            str.append(")");
            String formattedString = str.toString();

            result.setText(formattedString);
            verified.setDisable(false);
            decrypt.setDisable(true);
        } catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }

    @FXML
    void verified(ActionEvent event) {
        try {
            BigInteger p_value = new BigInteger(p.getText());
            BigInteger public_key_value = new BigInteger(public_key.getText());
            String message_value = message.getText();
            BigInteger generator_value = new BigInteger(generator.getText());
            Boolean result_value = Elgama_API.elgamaVerified(p_value, generator_value, public_key_value, message_value, sign_value);
            result2.setText(result_value.toString());
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
