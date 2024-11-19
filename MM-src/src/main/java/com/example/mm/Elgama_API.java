package com.example.mm;
import okhttp3.*;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.math.BigInteger;

public class Elgama_API {
    private static final String BASE_URL = "http://localhost:5000/"; // Update with your server's URL
    private static final OkHttpClient client = new OkHttpClient();

    public class ElagamaEncryptResult {
        public BigInteger k;
        public BigInteger[] encrypt;

        // Constructor
        public ElagamaEncryptResult(BigInteger k, BigInteger[] encrypt) {
            this.k = k;
            this.encrypt = encrypt;
        }
    }
    public static BigInteger[] elgamaGen(BigInteger p, BigInteger private_key) {
        try {
            // Example: Call the /elgama/gen endpoint
            JSONObject elgamaGenPayload = new JSONObject();
            elgamaGenPayload.put("p", p); // Example prime
            elgamaGenPayload.put("private_key", private_key);
            Response response = postRequest("/elgama/gen", elgamaGenPayload);
            if (response.isSuccessful()) {
                // Parse JSON response
                JSONObject jsonResponse = new JSONObject(response.body().string());
                BigInteger g = new BigInteger(jsonResponse.get("g").toString());
                BigInteger publicKey = new BigInteger(jsonResponse.get("public_key").toString());
                // Return as BigInteger array
                return new BigInteger[]{g, publicKey};
            } else {
                throw new RuntimeException("Error: " + response.body().string());
            }
        } catch (Exception ex) {
            throw new RuntimeException(ex.getMessage(), ex);
        }
    }

    public ElagamaEncryptResult elgamaEncrypt(BigInteger p, BigInteger public_key, BigInteger g, String message) {
        try {
            // Example: Call the /elgama/gen endpoint
            JSONObject elgamaGenPayload = new JSONObject();
            elgamaGenPayload.put("p", p);
            elgamaGenPayload.put("public_key", public_key);
            elgamaGenPayload.put("g", g); // Example prime// Example prime
            elgamaGenPayload.put("message", message);

            Response response = postRequest("/elgama/encrypt", elgamaGenPayload);
            if (response.isSuccessful()) {
                // Parse JSON response
                JSONObject jsonResponse = new JSONObject(response.body().string());
                JSONArray encryptedArray = jsonResponse.getJSONArray("encrypted");
                BigInteger k = new BigInteger(jsonResponse.get("k").toString());

                BigInteger[] encrypted = new BigInteger[encryptedArray.length()];

                for (int i = 0; i < encryptedArray.length(); i++) {
                    encrypted[i] = new BigInteger(encryptedArray.get(i).toString());
                }
                return new ElagamaEncryptResult(k, encrypted);
            } else {
                throw new RuntimeException("Error: " + response.body().string());
            }
        } catch (Exception ex) {
            throw new RuntimeException(ex.getMessage(), ex);
        }

    }

    public static String elgamaDecrypt(BigInteger p, BigInteger private_key, BigInteger k, BigInteger[] encrypt) {
        try {
            // Example: Call the /elgama/gen endpoint
            JSONObject elgamaGenPayload = new JSONObject();
            elgamaGenPayload.put("p", p); // Example prime
            elgamaGenPayload.put("private_key", private_key); // Example prime
            elgamaGenPayload.put("encrypted", encrypt);
            elgamaGenPayload.put("k", k);

            Response response = postRequest("/elgama/decrypt", elgamaGenPayload);
            if (response.isSuccessful()) {
                // Parse JSON response
                JSONObject jsonResponse = new JSONObject(response.body().string());
                String message = jsonResponse.get("message").toString();
                return message;
            } else {
                throw new RuntimeException("Error: " + response.body().string());
            }
        } catch (Exception ex) {
            throw new RuntimeException(ex.getMessage(), ex);
        }

    }

    public static BigInteger[] elgamaSign(BigInteger p, BigInteger g, BigInteger private_key, String message) {
        try {
            // Example: Call the /elgama/gen endpoint
            JSONObject elgamaGenPayload = new JSONObject();
            elgamaGenPayload.put("p", p); // Example prime
            elgamaGenPayload.put("g", g); // Example prime
            elgamaGenPayload.put("private_key", private_key);
            elgamaGenPayload.put("message", message);


            Response response = postRequest("/elgama/sign", elgamaGenPayload);
            if (response.isSuccessful()) {
                // Parse JSON response
                JSONObject jsonResponse = new JSONObject(response.body().string());
                JSONArray encryptedArray = jsonResponse.getJSONArray("sign");

                BigInteger[] sign = new BigInteger[encryptedArray.length()];

                for (int i = 0; i < encryptedArray.length(); i++) {
                    sign[i] = new BigInteger(encryptedArray.get(i).toString());
                }
                return sign;
            } else {
                throw new RuntimeException("Error: " + response.body().string());
            }
        } catch (Exception ex) {
            throw new RuntimeException(ex.getMessage(), ex);
        }
    }

    public static Boolean elgamaVerified(BigInteger p, BigInteger g, BigInteger public_key, String message, BigInteger[] sign) {
        try {
            // Example: Call the /elgama/gen endpoint
            JSONObject elgamaGenPayload = new JSONObject();
            elgamaGenPayload.put("p", p); // Example prime
            elgamaGenPayload.put("g", g); // Example prime
            elgamaGenPayload.put("message", message);
            elgamaGenPayload.put("sign", sign);
            elgamaGenPayload.put("public_key", public_key);

            Response response = postRequest("/elgama/verified", elgamaGenPayload);
            if (response.isSuccessful()) {
                // Parse JSON response
                JSONObject jsonResponse = new JSONObject(response.body().string());
                Boolean verified = (Boolean) jsonResponse.get("verified");
                return verified;
            } else {
                System.out.println("Error: " + response.body().string());
            }
        } catch (Exception err) {
            err.printStackTrace();
        }
        return null;
    }



    private static Response postRequest(String endpoint, JSONObject payload) throws IOException {
        RequestBody body = RequestBody.create(
                payload.toString(),
                MediaType.get("application/json; charset=utf-8")
        );

        Request request = new Request.Builder()
                .url(BASE_URL + endpoint)
                .post(body)
                .build();

        return client.newCall(request).execute();
    }
}
