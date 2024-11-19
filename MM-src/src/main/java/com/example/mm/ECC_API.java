package com.example.mm;
import okhttp3.*;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.math.BigInteger;

public class ECC_API {
    public class ECCEncryptResult {
        public BigInteger diff;
        public BigInteger k;
        public BigInteger[][] encrypt;

        // Constructor
        public ECCEncryptResult(BigInteger diff, BigInteger k, BigInteger[][] encrypt) {
            this.diff = diff;
            this.k = k;
            this.encrypt = encrypt;
        }
    }

    private static final String BASE_URL = "http://localhost:5000/"; // Update with your server's URL
    private static final OkHttpClient client = new OkHttpClient();

    public static BigInteger[] eccGen(BigInteger p, BigInteger a, BigInteger b, BigInteger private_key) {
        try {
            // Example: Call the /ecc/gen endpoint
            JSONObject eccGenPayload = new JSONObject();
            eccGenPayload.put("p", p); // Example prime
            eccGenPayload.put("b", b);
            eccGenPayload.put("a", a);
            eccGenPayload.put("private_key", private_key);
            Response response = postRequest("/ecc/gen", eccGenPayload);
            if (response.isSuccessful()) {
                JSONObject jsonResponse = new JSONObject(response.body().string());

                JSONArray gArray = jsonResponse.getJSONArray("G"); // Generator point
                BigInteger gX = new BigInteger(gArray.get(0).toString());
                BigInteger gY = new BigInteger(gArray.get(1).toString());

                BigInteger order = new BigInteger(jsonResponse.get("point_number").toString());
                BigInteger privateKey = new BigInteger(jsonResponse.get("private_key").toString());

                JSONArray publicKeyArray = jsonResponse.getJSONArray("public_key"); // Public key
                BigInteger publicKeyX = new BigInteger(publicKeyArray.get(0).toString());
                BigInteger publicKeyY = new BigInteger(publicKeyArray.get(1).toString());

                // Return as BigInteger array
                return new BigInteger[]{gX, gY, publicKeyX, publicKeyY, privateKey, order};
            } else {
                throw new RuntimeException("Error: " + response.body().string());
            }
        } catch (Exception ex) {
            throw new RuntimeException(ex.getMessage(), ex);
        }
    }

    public ECCEncryptResult eccEncrypt(BigInteger p, BigInteger a, BigInteger b, BigInteger[] G, BigInteger[] public_key, String message) {
        try {
            // Example: Call the /ecc/gen endpoint
            JSONObject eccGenPayload = new JSONObject();
            eccGenPayload.put("b", b);
            eccGenPayload.put("a", a);
            eccGenPayload.put("p", p);
            eccGenPayload.put("public_key", public_key);
            eccGenPayload.put("G", G);
            eccGenPayload.put("message", message);

            Response response = postRequest("/ecc/encrypt", eccGenPayload);
            if (response.isSuccessful()) {

                JSONObject jsonResponse = new JSONObject(response.body().string());

                BigInteger diff = new BigInteger(jsonResponse.get("diff").toString());
                BigInteger k = new BigInteger(jsonResponse.get("k").toString());

                JSONArray encryptArray = jsonResponse.getJSONArray("encrypt");

                // Parse encrypted pairs
                BigInteger[][] encrypted = new BigInteger[encryptArray.length()][2];
                for (int i = 0; i < encryptArray.length(); i++) {
                    JSONArray pair = encryptArray.getJSONArray(i);
                    encrypted[i][0] = new BigInteger(pair.get(0).toString());
                    encrypted[i][1] = new BigInteger(pair.get(1).toString());
                }
                return new ECCEncryptResult(diff, k, encrypted);

            } else {
                throw new RuntimeException("Error: " + response.body().string());
            }
        } catch (Exception ex) {
            throw new RuntimeException(ex.getMessage(), ex);
        }
    }

    public static String eccDecrypt(BigInteger p, BigInteger a, BigInteger b, BigInteger[] G, BigInteger private_key, ECCEncryptResult encrypt) {
        try {
            // Example: Call the /ecc/gen endpoint
            JSONObject eccGenPayload = new JSONObject();
            eccGenPayload.put("b", b);
            eccGenPayload.put("a", a);
            eccGenPayload.put("p", p);
            eccGenPayload.put("G", G);
            eccGenPayload.put("p", p); // Example prime
            eccGenPayload.put("private_key", private_key); // Example prime
            eccGenPayload.put("encrypt", encrypt.encrypt);
            eccGenPayload.put("diff", encrypt.diff);
            eccGenPayload.put("k", encrypt.k);

            Response response = postRequest("/ecc/decrypt", eccGenPayload);
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

    public static BigInteger[] eccSign(BigInteger p, BigInteger a, BigInteger b, BigInteger[] G, BigInteger q, BigInteger private_key, String message) {
        try {
            // Example: Call the /ecc/gen endpoint
            JSONObject eccGenPayload = new JSONObject();
            eccGenPayload.put("b", b);
            eccGenPayload.put("a", a);
            eccGenPayload.put("p", p);
            eccGenPayload.put("q", q);
            eccGenPayload.put("G", G);
            eccGenPayload.put("private_key", private_key);
            eccGenPayload.put("message", message);


            Response response = postRequest("/ecc/sign", eccGenPayload);
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

    public static Boolean eccVerified(BigInteger p, BigInteger a, BigInteger b, BigInteger[] G, BigInteger q, BigInteger[] public_key, String message, BigInteger[] sign) {
        try {
            // Example: Call the /ecc/gen endpoint
            JSONObject eccGenPayload = new JSONObject();
            eccGenPayload.put("b", b);
            eccGenPayload.put("a", a);
            eccGenPayload.put("p", p);
            eccGenPayload.put("q", q);
            eccGenPayload.put("G", G);
            eccGenPayload.put("message", message);
            eccGenPayload.put("sign", sign);
            eccGenPayload.put("public_key", public_key);

            Response response = postRequest("/ecc/verified", eccGenPayload);
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
