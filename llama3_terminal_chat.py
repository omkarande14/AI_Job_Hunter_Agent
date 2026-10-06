import ollama

print("="*50)
print("🤖 Llama 3 (8B) AI Bot - Memory Mode Enabled")
print("💡 बाहेर पडण्यासाठी 'exit' किंवा हिस्ट्री साफ करण्यासाठी 'clear' टाईप करा.")
print("="*50 + "\n")

# चॅट हिस्ट्री स्टोअर करण्यासाठी रिकामी लिस्ट
conversation_history = []

while True:
    user_input = input("\nYou: ")
    
    # बाहेर पडण्यासाठी
    if user_input.lower() == 'exit':
        print("\nBot: धन्यवाद! पुन्हा भेटूया 👋")
        break
    
    # जुनी हिस्ट्री क्लिअर करण्यासाठी
    if user_input.lower() == 'clear':
        conversation_history = []
        print("\n🧹 चॅट हिस्ट्री क्लिअर झाली आहे!")
        continue

    if not user_input.strip():
        continue

    # युझरचा मेसेज लिस्टमध्ये ॲड करणे
    conversation_history.append({'role': 'user', 'content': user_input})

    print("\nAI Bot: ", end="", flush=True)
    
    # संपूर्ण हिस्ट्री Ollama ला पाठवणे
    stream = ollama.chat(
        model='llama3:8b',
        messages=conversation_history,
        stream=True,
    )

    full_response = ""
    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        full_response += content
        
    print()  # New line
    
    # AI चे उत्तरसुद्धा लिस्टमध्ये सेव्ह करणे (पुढच्या संवादासाठी)
    conversation_history.append({'role': 'assistant', 'content': full_response})!