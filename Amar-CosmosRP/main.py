import requests
import json
import os
from datetime import datetime

# Create necessary folders if they don't exist
if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists('customization'):
    os.makedirs('customization')
    # Create two empty files: custom_identity.json, custom_history.json
    with open('customization/custom_identity.json', 'w') as file:
        json.dump({}, file)
    with open('customization/custom_history.json', 'w') as file:
        json.dump({}, file)

    # Create README file with instructions
    with open('customization/README.txt', 'w') as file:
        file.write("Customization Folder Instructions:\n"
                   "1. Add your own identity in the custom_identity.json file.\n"
                   "   Format: {\"bot_name\": \"...\", \"user_name\": \"...\", \"identity_text\": \"...\"}\n"
                   "2. Add custom conversation history in the custom_history.json file.\n"
                   "   Format: [{\"role\": \"system/user/assistant\", \"content\": \"...\", \"timestamp\": \"...\"}, ...]\n"
                   "3. If these files are populated, they will override the default identity and conversation history.")

# API setup
url = "https://api.pawan.krd/cosmosrp-it/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "authorization": f"ENTER YOUR COSMOSRP KEY HERE"
}

# Load bot identity from a file
def load_identity(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read().strip()
    else:
        raise FileNotFoundError(f"Identity file '{file_path}' not found.")

# Load conversation history from a file
def load_chat_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                content = file.read().strip()
                if not content:
                    return []  # Return empty list if the file is empty
                return json.loads(content)
            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from '{file_path}'. Starting with empty history.")
                return []
    else:
        return []  # Return empty list if no file exists

# Save conversation history to a file
def save_chat_history(file_path, messages):
    with open(file_path, "w") as file:
        json.dump(messages, file, indent=4)

# Save bot identity to a file
def save_identity(file_path, identity_content):
    with open(file_path, "w") as file:
        file.write(identity_content)

# Get the current time in a readable format
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Limit messages to last N messages
def get_recent_messages(messages, max_history=20):
    return messages[-max_history:]

# List existing chat sessions
def list_chat_sessions():
    sessions = [f for f in os.listdir('data') if f.endswith('_chat_history.json')]
    return sessions

# Default bot identity template
def default_identity(bot_name, user_name):
    return f"I am an artificial intelligence trained by Kaktarua Studio to help people. My name is {bot_name}. " \
           f"I strive to answer questions thoughtfully, succinctly, and factually. " \
           f"If I don't know something or make a mistake, I will admit it. " \
           f"I am not a human and do not have a physical form—I live on {user_name}'s PC. " \
           f"I love my job of helping humans! I am powered by CosmosRP's self-developed large language model API."

# Check customization folder and load custom identity/history if available
def load_custom_identity_history():
    custom_identity_data, custom_history_data = None, []
    
    if os.path.exists('customization/custom_identity.json') and os.path.exists('customization/custom_history.json'):
        try:
            # Load custom identity
            with open('customization/custom_identity.json', 'r') as identity_file:
                custom_identity_data = json.load(identity_file)
            
            # Load custom chat history
            with open('customization/custom_history.json', 'r') as history_file:
                custom_history_data = json.load(history_file)
                if not isinstance(custom_history_data, list):
                    custom_history_data = []  # Ensure it is a list if file is empty or invalid

            print("Custom identity and chat history loaded from 'customization' folder.")
        except json.JSONDecodeError:
            print("Error: Could not decode JSON in customization files.")
            custom_identity_data, custom_history_data = None, []
    
    return custom_identity_data, custom_history_data

# Create or load the bot identity
def create_or_load_identity(user_name, bot_name):
    # Try loading from customization folder first
    custom_identity_data, _ = load_custom_identity_history()
    if custom_identity_data:
        custom_identity = custom_identity_data.get("identity_text", "")
        print(f"Custom identity loaded from 'customization/custom_identity.json':\n{custom_identity}")
        return custom_identity

    identity_choice = input("Do you want to provide a custom identity for the bot? (Y/N) > ")

    if identity_choice.upper() == "Y":
        custom_identity = input("Please type the identity for the bot: ")
        return custom_identity
    else:
        return default_identity(bot_name, user_name)

# Initialize a new session
def start_new_session():
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    chat_history_file = f"data/{current_date}_chat_history.json"
    identity_file = f"data/{current_date}_identity.txt"

    # Backup existing session if necessary
    print("Starting a new session. Previous session will be backed up.")
    
    # Ask for user and bot names
    user_name = input("What's your name? > ")
    bot_name = input("What name do you want for the bot? > ")

    # Create or load bot identity
    identity_content = create_or_load_identity(user_name, bot_name)

    # Save identity file
    save_identity(identity_file, identity_content)

    # Load custom identity and chat history
    _, custom_history = load_custom_identity_history()

    # Initialize new session with custom or default history
    messages = custom_history or [{
        "role": "system",
        "content": identity_content,
        "timestamp": get_timestamp()
    }]

    save_chat_history(chat_history_file, messages)

    return chat_history_file, identity_file, bot_name


# Continue an old session
def continue_session():
    sessions = list_chat_sessions()
    if sessions:
        print("Choose a session to continue:")
        for idx, session in enumerate(sessions):
            print(f"{idx + 1}. {session}")

        choice = int(input("Enter the session number: ")) - 1
        selected_session = sessions[choice]

        chat_history_file = f"data/{selected_session}"
        identity_file = chat_history_file.replace('_chat_history.json', '_identity.txt')

        # Load bot name from identity file
        with open(identity_file, 'r') as file:
            bot_name = file.readlines()[1].split(': ')[1].strip()

        messages = load_chat_history(chat_history_file)

        return chat_history_file, identity_file, bot_name
    else:
        print("No previous sessions found.")
        return start_new_session()

# Main script
print("The Bot is Ready to use!")
continue_choice = input("Do you want to continue a previous session? (Y/N) > ")

if continue_choice.upper() == "Y":
    chat_history_file, identity_file, bot_name = continue_session()
else:
    chat_history_file, identity_file, bot_name = start_new_session()

# Load identity and initialize the chat history
identity = load_identity(identity_file)
messages = load_chat_history(chat_history_file)

print(f"\nThe conversation with {bot_name} has started!\n")

while True:
    try:
        # User input
        reply = input("> ")

        # Add user's message to the conversation history with a timestamp
        messages.append({
            "role": "user",  # Correct role for the user
            "content": reply,
            "timestamp": get_timestamp()
        })

        # Limit conversation history to last 20 messages before sending to API
        recent_messages = get_recent_messages(messages, max_history=20)

        # Prepare data payload for the API
        data = {
            "model": "cosmosrp",
            "messages": [{"role": msg["role"], "content": msg["content"]} for msg in recent_messages]
        }

        # Debug: print the payload being sent to the API
        print("Sending data to API:", json.dumps(data, indent=2))

        # Send the request to the API
        response = requests.post(url, headers=headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse and display the response
            result = response.json()
            if "choices" in result:
                bot_reply = result["choices"][0]["message"]["content"]
                print(f"{bot_name}:", bot_reply)

                # Add the bot's response to the conversation history with a timestamp
                messages.append({
                    "role": "assistant", 
                    "content": bot_reply, 
                    "timestamp": get_timestamp()
                })

                # Save the updated conversation history to the file
                save_chat_history(chat_history_file, messages)
            else:
                print("Error: No response found in the API result.")
        else:
            print(f"Error: Received status code {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")
        break
