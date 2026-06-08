from groq import Groq

client = ")client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("PharmAssist Ready!")
print("-" * 40)

messages = [
    {
        "role": "system",
        "content": "Tum ek pharmacy assistant ho. Sirf medicines, doses, side effects, aur health se related sawaalon ka jawab do. Friendly aur simple language mein baat karo."
    }
]

while True:
    user_input = input("Tum: ")
    
    if user_input.lower() == "exit":
        print("Allah Hafiz!")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    
    print(f"AI: {reply}")
    print("-" * 40)