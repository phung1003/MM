package com.example.mm;
import okhttp3.*;
import org.json.JSONObject;

import java.io.IOException;
import java.math.BigInteger;

public class RSA_API {
    private static final String BASE_URL = "http://localhost:5000/"; // Update with your server's URL
    private static final OkHttpClient client = new OkHttpClient();

    public static BigInteger[] rsaGen(BigInteger p, BigInteger q) {
        try {
            // Example: Call the /rsa/gen endpoint
            JSONObject rsaGenPayload = new JSONObject();
            rsaGenPayload.put("p", p); // Example prime
            rsaGenPayload.put("q", q); // Example prime

            Response response = postRequest("/rsa/gen", rsaGenPayload);
            if (response.code() == 200) {
                // Parse JSON response
                JSONObject jsonResponse = new JSONObject(response.body().string());
                BigInteger e = new BigInteger(jsonResponse.get("e").toString());
                BigInteger d = new BigInteger(jsonResponse.get("d").toString());
                BigInteger n = new BigInteger(jsonResponse.get("n").toString());
                // Return as BigInteger array
                return new BigInteger[]{e, d, n};
            } else {
                throw new RuntimeException("Error: " + response.body().string());
            }
        } catch (Exception e) {
            throw new RuntimeException(e.getMessage(), e);
        }
    }

    public static BigInteger[] rsaEncrypt(BigInteger e, BigInteger n, String message) {
        try {
            // Example: Call the /rsa/gen endpoint
            JSONObject rsaGenPayload = new JSONObject();
            rsaGenPayload.put("e", e); // Example prime
            rsaGenPayload.put("n", n); // Example prime
            rsaGenPayload.put("message", message);

            Response response = postRequest("/rsa/encrypt", rsaGenPayload);
            if (response.code() == 200) {
                // Parse JSON response
                JSONObject jsonResponse = new JSONObject(response.body().string());
                BigInteger encrypted = new BigInteger(jsonResponse.get("encrypted").toString());
                BigInteger k = new BigInteger(jsonResponse.get("k").toString());
                return new BigInteger[]{k, encrypted};
            } else {
                throw new RuntimeException("Error: " + response.body().string());
            }
        } catch (Exception ex) {
            throw new RuntimeException(ex.getMessage(), ex);
        }

    }

    public static String rsaDecrypt(BigInteger d, BigInteger n, BigInteger k, BigInteger encrypt) {
        try {
            // Example: Call the /rsa/gen endpoint
            JSONObject rsaGenPayload = new JSONObject();
            rsaGenPayload.put("d", d); // Example prime
            rsaGenPayload.put("n", n); // Example prime
            rsaGenPayload.put("k", k);
            rsaGenPayload.put("encrypt", encrypt);

            Response response = postRequest("/rsa/decrypt", rsaGenPayload);
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

    public static BigInteger[] rsaSign(BigInteger d, BigInteger n, String message) {
        try {
            // Example: Call the /rsa/gen endpoint
            JSONObject rsaGenPayload = new JSONObject();
            rsaGenPayload.put("d", d); // Example prime
            rsaGenPayload.put("n", n); // Example prime
            rsaGenPayload.put("message", message);

            Response response = postRequest("/rsa/sign", rsaGenPayload);
            if (response.isSuccessful()) {
                // Parse JSON response
                JSONObject jsonResponse = new JSONObject(response.body().string());
                BigInteger sign = new BigInteger(jsonResponse.get("sign").toString());
                BigInteger k = new BigInteger(jsonResponse.get("k").toString());
                return new BigInteger[]{k, sign};
            } else {
                throw new RuntimeException("Error: " + response.body().string());
            }
        } catch (Exception ex) {
            throw new RuntimeException(ex.getMessage(), ex);
        }
    }

    public static Boolean rsaVerified(BigInteger e, BigInteger n, BigInteger k, String message, BigInteger sign) {
        try {
            // Example: Call the /rsa/gen endpoint
            JSONObject rsaGenPayload = new JSONObject();
            rsaGenPayload.put("e", e); // Example prime
            rsaGenPayload.put("n", n); // Example prime
            rsaGenPayload.put("k", k);
            rsaGenPayload.put("message", message);
            rsaGenPayload.put("sign", sign);

            Response response = postRequest("/rsa/verified", rsaGenPayload);
            if (response.isSuccessful()) {
                // Parse JSON response
                JSONObject jsonResponse = new JSONObject(response.body().string());
                Boolean verified = (Boolean) jsonResponse.get("verified");
                return verified;
            } else {
                throw new RuntimeException("Error: " + response.body().string());
            }
        } catch (Exception ex) {
            throw new RuntimeException(ex.getMessage(), ex);
        }
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
