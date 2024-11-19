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

public class RSA {
    private Stage stage;
    private Scene scene;
    private Parent root;

    @FXML
    private TextField p;
    @FXML
    private TextField q;
    @FXML
    private TextField n;
    @FXML
    private TextField e;
    @FXML
    private TextField d;
    @FXML
    private TextField message;
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
    private TextField result;
    @FXML
    private TextField result2;


    BigInteger k;

    @FXML
    private void generate(ActionEvent event) {
        try {
            // Convert input to BigInteger
            BigInteger p_value = new BigInteger(p.getText());
            BigInteger q_value = new BigInteger(q.getText());

            BigInteger[] keys = RSA_API.rsaGen(p_value, q_value);

            BigInteger e_value = keys[0];
            BigInteger d_value = keys[1];
            BigInteger n_value = keys[2];

            // Display results in the GUI
            e.setText(e_value.toString());
            d.setText(d_value.toString());
            n.setText(n_value.toString());

            encrypt.setDisable(false);
            decrypt.setDisable(false);
            sign.setDisable(false);
            verified.setDisable(false);

        } catch (NumberFormatException ex) {
            // Handle invalid input
            error.setText("Please enter valid integers for p and q.");
            errorBox.setVisible(true);
        }
        catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }

    @FXML void encrypt(ActionEvent event) {
        try {
            BigInteger e_value = new BigInteger(e.getText());
            BigInteger n_value = new BigInteger(n.getText());
            String message_value = message.getText();
            BigInteger[] result_value = RSA_API.rsaEncrypt(e_value, n_value, message_value);
            result.setText(result_value[1].toString());
            k = result_value[0];
            verified.setDisable(true);
            decrypt.setDisable(false);
        } catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }

    @FXML void decrypt(ActionEvent event) {
        try {
            BigInteger d_value = new BigInteger(d.getText());
            BigInteger n_value = new BigInteger(n.getText());
            BigInteger result_value =new BigInteger(result.getText());
            String message_value = RSA_API.rsaDecrypt(d_value, n_value, k, result_value);
            result2.setText(message_value);
        } catch (Exception ex) {
            // Handle other exceptions
            error.setText(ex.getMessage());
            errorBox.setVisible(true);
        }
    }

    @FXML void sign(ActionEvent event) {
        try {
            BigInteger d_value = new BigInteger(d.getText());
            BigInteger n_value = new BigInteger(n.getText());
            String message_value = message.getText();
            BigInteger[] result_value = RSA_API.rsaSign(d_value, n_value, message_value);
            result.setText(result_value[1].toString());
            k = result_value[0];
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
            BigInteger e_value = new BigInteger(e.getText());
            BigInteger n_value = new BigInteger(n.getText());
            String message_value = message.getText();
            BigInteger sign_value = new BigInteger(result.getText());
            Boolean verified_value = RSA_API.rsaVerified(e_value, n_value, k, message_value, sign_value);
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
