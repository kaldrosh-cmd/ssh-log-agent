from ollama import chat
from log_tools import count_attempts, count_targeted_users, extract_ip
SYSTEM_PROMPT = "You are a security assistant that analyzyes SSH log files. Always use the available tools to answer questions instead of asking the user for clarifications. If the user asks for the total number of failed login attempts, sum the results and give one number."
MAX_ROUNDS = 5

def main():
    message = input("Put the message in here: ")
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}]
    available_tools = {"get_failed_attempts": get_failed_attempts, "get_targeted_users": get_targeted_users, "get_users_for_ip": get_users_for_ip}
    round_counter = 0
    while round_counter < MAX_ROUNDS:
        result = chat(model="qwen3:14b", messages=messages, think=False, tools=[get_failed_attempts, get_targeted_users, get_users_for_ip])
        messages.append(result.message)
        round_counter += 1
        if result.message.tool_calls is not None:
            for tool in result.message.tool_calls:
                print(tool.function.name)
                print(tool.function.arguments)
                function_to_call = available_tools[tool.function.name]
                output = function_to_call(**tool.function.arguments)
                print(output)
                messages.append({"role": "tool","content": str(output), "tool_name": tool.function.name})
        else:
            print(result.message.content)
            break
    else:
        print("Agent reached max rounds")


def get_failed_attempts(filename: str) -> dict:
    """Count failed SSH login attempts for every IP address in a log file.

    Args:
        filename: Name of the log file, for example logs.txt

    Returns:
        Dictionary with IP addresses and number of failed attempts of logging in
    """
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        lines = file.readlines()
    return count_attempts(lines)

def get_targeted_users(filename: str) -> dict:
    """Count failed SSH login attempts for every username in a log file.

    Args:
        filename: Name of the log file, for example logs.txt

    Returns:
        Dictionary with usernames and number of failed attempts of logging in
    """
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        lines = file.readlines()
    return count_targeted_users(lines)

def get_users_for_ip(filename: str, ip: str) -> dict:
    """Count failed SSH login attempts for every account attacked by one IP address.

    Args:
        filename: Name of the log file, for example logs.txt
        ip: ip address for example "10.0.0.7"

    Returns:
        Dictionary with username as key and value as failed attempts
    """
    ip_lines = []
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        lines = file.readlines()
        for line in lines:
            if ip == extract_ip(line):
                ip_lines.append(line)
    return count_targeted_users(ip_lines)
                



if __name__ == "__main__":
    main()

