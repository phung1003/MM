package com.example.mm;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.stage.Stage;

import javafx.event.ActionEvent;
import java.io.IOException;

public class MainMenu {
    private Stage stage;
    private Scene scene;
    private Parent root;
    @FXML
    private Button RSA;
    @FXML
    private Button Elgama;
    @FXML
    private Button ECC;


    @FXML
    private void switchRSA(ActionEvent event) throws IOException {
        Parent root = FXMLLoader.load(getClass().getResource("rsa.fxml"));
        stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        scene = new Scene(root, 900, 700);
        stage.setScene(scene);
        stage.show();
    }

    @FXML
    private void switchElgama(ActionEvent event) throws IOException {
        Parent root = FXMLLoader.load(getClass().getResource("elgama.fxml"));
        stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        scene = new Scene(root, 900, 700);
        stage.setScene(scene);
        stage.show();
    }

    @FXML
    private void switchECC(ActionEvent event) throws IOException {
        Parent root = FXMLLoader.load(getClass().getResource("ecc.fxml"));
        stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        scene = new Scene(root, 900, 700);
        stage.setScene(scene);
        stage.show();
    }


}
