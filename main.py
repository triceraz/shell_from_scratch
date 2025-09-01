import sys
import os
import subprocess

valid_commands = ("exit", "echo", "type")


def main():
    global valid_commands
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        user_input = input()
        user_input_list = user_input.split(" ", 1)
        command = user_input_list[0]
        if len(user_input_list) > 1:
            args = user_input_list[1].split()
        else:
            args = []

        if os.path.isfile(command) and os.access(command, os.X_OK):
            fullpath = os.path.abspath(command)
            subprocess.run([fullpath] + args)

        elif command == "exit":
            sys.exit(0)

        elif command == "echo":
            print(args)

        elif command == "type":
            type_command(user_input_list[1])

        elif command == "pwd":
            print(os.path.abspath)

        else:
            command_not_found(command)


def command_not_found(command):
    print(f"{command}: command not found")


def command_description(command):
    print(f"{command} is a shell builtin")


def type_command(command):
    if command in valid_commands:
        command_description(command)
        return

    PATH = os.environ["PATH"]
    dirs = PATH.split(":")

    found = False
    for d in dirs:
        fullpath = os.path.join(d, command)
        if os.path.isfile(fullpath) and os.access(fullpath, os.X_OK):
            print(f"{command} is {fullpath}")
            found = True
            break
    if not found:
        print(f"{command}: not found")


if __name__ == "__main__":
    main()
