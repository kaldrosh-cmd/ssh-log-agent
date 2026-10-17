from ollama import chat
from log_tools import count_attempts

def main():
    message = input("Put the message in here: ")
    messages = [{"role": "user", "content": message}]
    result = chat(model="qwen3:14b", messages=messages, think=False, tools=[get_failed_attempts])
    messages.append(result.message)
    available_tools = {"get_failed_attempts": get_failed_attempts}
    if result.message.tool_calls is not None:
        for tool in result.message.tool_calls:
            print(tool.function.name)
            print(tool.function.arguments)
            function_to_call = available_tools[tool.function.name]
            output = function_to_call(**tool.function.arguments)
            print(output)
            messages.append({"role": "tool","content": str(output), "tool_name": tool.function.name})
        final = chat(model="qwen3:14b", messages=messages, think=False, tools=[get_failed_attempts])
        print(final.message.content)
    else:
        print(result.message.content)

def get_failed_attempts(filename: str) -> dict:
    """Count failed SSH login attempts for every IP address in a log file.

    Args:
        filename: Name of the log file, for example logs.txt

    Returns:
        Dictionary with IP addresses and number of failed attempts of loging in
    """
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        lines = file.readlines()
    return count_attempts(lines)

if __name__ == "__main__":
    main()

