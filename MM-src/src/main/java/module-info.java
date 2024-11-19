module com.example.mm {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;
    requires java.desktop;
    requires okhttp3;
    requires org.json;

    opens com.example.mm to javafx.fxml;
    exports com.example.mm;
}