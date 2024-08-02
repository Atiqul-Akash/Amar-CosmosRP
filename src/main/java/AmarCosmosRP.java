import okhttp3.*;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.io.IOException;
import java.util.Scanner;

public class AmarCosmosRP {

    public static void main(String[] args) {
        AmarCosmosRP bot = new AmarCosmosRP();
        bot.start();
    }

    public void start() {
        System.out.println("Welcome to the CosmosRP ChatBot! Type 'exit' to quit.");
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.print("You: ");
            String userInput = scanner.nextLine();
            if (userInput.equalsIgnoreCase("exit")) {
                break;
            }
            try {
                String response = getCosmosRPResponse(userInput);
                System.out.println("Bot: " + response);
            } catch (IOException e) {
                System.err.println("Error while fetching response from the model: " + e.getMessage());
            }
        }
        scanner.close();
        System.out.println("ChatBot terminated.");
    }

    private String getCosmosRPResponse(String input) throws IOException {
        OkHttpClient client = new OkHttpClient();

        // Create JSON object for the request body
        JsonObject json = new JsonObject();
        json.addProperty("model", "pai-001");

        JsonArray messages = new JsonArray();
        JsonObject message = new JsonObject();
        message.addProperty("role", "user");
        message.addProperty("content", input);
        messages.add(message);
        json.add("messages", messages);

        json.addProperty("max_tokens", 240);
        json.addProperty("temperature", 1.0);

        RequestBody body = RequestBody.create(
                json.toString(),
                MediaType.parse("application/json")
        );

        Request request = new Request.Builder()
                .url("https://api.pawan.krd/cosmosrp/v1/chat/completions")
                .post(body)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                System.out.println("Response code: " + response.code());
                System.out.println("Response message: " + response.message());
                throw new IOException("Unexpected code " + response);
            }
            ResponseBody responseBody = response.body();
            if (responseBody != null) {
                JsonObject responseJson = com.google.gson.JsonParser.parseString(responseBody.string()).getAsJsonObject();
                return responseJson.getAsJsonArray("choices")
                        .get(0).getAsJsonObject()
                        .get("message").getAsJsonObject()
                        .get("content").getAsString();
            }
            return "No response from the model.";
        }
    }
}
