from ollama import chat

def main():
    message = input("Put the message in here: ")
    result = chat(model="qwen3:14b", messages=[{"role": "user", "content": message}], think=False)
    print(result.message.content)

if __name__ == "__main__":
    main()

