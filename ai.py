def ask_ai(question):
    try:
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1000,
            system="You are Smart Student AI, a helpful tutor. Explain answers in a simple way for students.",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {e}"
