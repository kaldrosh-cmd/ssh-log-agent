import sys
import re
import csv

def main():

    if len(sys.argv) != 2:
        sys.exit("Usage: python project.py <log_file>")

    filename = sys.argv[1]
    try:
        with open(filename, "r", encoding="utf-8", errors="replace") as file:
            lines = file.readlines()

        attempts = count_attempts(lines)
        users = count_targeted_users(lines)

        sorted_attempts = sort_attempts(attempts)
        output_file = "log_results.csv"
        headers = ["IP", "Attempts"]

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for ip, count in sorted_attempts:
                writer.writerow({"IP": ip, "Attempts": count})

        print(f"Report saved to {output_file}")
        for user, count in sort_attempts(users):
            if count == 1:
                print(f"Attacked user: {user}, {count} time")
            else:
                print(f"Attacked user: {user}, {count} times")

    except FileNotFoundError:
        sys.exit(f"Error: The file '{filename}' does not exist.")

def extract_ip(line):
    match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
    if not match:
        return None
    return match.group(0)

def count_attempts(lines):
    failed_attempts = {}
    for line in lines:
        if "Failed password" in line:
            ip = extract_ip(line)
            if ip:
                failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
    return failed_attempts

def sort_attempts(attempts):
    return sorted(attempts.items(), key=lambda pair: pair[1], reverse=True)

def count_targeted_users(lines):
    users = {}
    for line in lines:
        if "Failed password" in line:
            match = re.search(r"for (?:invalid user )?(\S+) from", line)
            if match:
                user = match.group(1)
                users[user] = users.get(user, 0) + 1
    return users


if __name__ == "__main__":
    main()
