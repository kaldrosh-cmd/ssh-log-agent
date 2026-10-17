from ollama import chat
from log_tools import count_attempts

def main():
    message = input("Put the message in here: ")
    result = chat(model="qwen3:14b", messages=[{"role": "user", "content": message}], think=False, tools=[get_failed_attempts])
    print(result.message.tool_calls)

def get_failed_attempts(filename: str) -> dict:
    """This function returns failed attempts of logging in through a dictionary where filename is log file which conatins those failed attempts"""
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        lines = file.readlines()
    return count_attempts(lines)

if __name__ == "__main__":
    main()

