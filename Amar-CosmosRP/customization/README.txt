Customization Folder Instructions:
1. Add your own identity in the custom_identity.json file.
   Format: {"bot_name": "...", "user_name": "...", "identity_text": "..."}
2. Add custom conversation history in the custom_history.json file.
   Format: [{"role": "system/user/assistant", "content": "...", "timestamp": "..."}, ...]
3. If these files are populated, they will override the default identity and conversation history.