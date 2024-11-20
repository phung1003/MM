module com.example.mm {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;
    requires okhttp3;
    requires org.json;
    requires java.desktop;

    opens com.example.mm to javafx.fxml;
    exports com.example.mm;
}