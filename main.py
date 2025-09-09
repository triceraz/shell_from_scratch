import sys
import os
import subprocess
import shlex

VALID_COMMANDS = ("exit", "echo", "type")


def cmd_exit(args):
    sys.exit(0)


def cmd_echo(args):
    print(" ".join(args))


def cmd_pwd(args):
    print(os.getcwd())


def cmd_cd(args):
    if not args or args[0] == "~":
        directory = os.path.expanduser("~")
    else:
        directory = args[0]

    try:
        os.chdir(directory)
    except FileNotFoundError:
        print(f"{directory}: No such file or directory")


BUILTINS = {
    "exit": cmd_exit,
    "echo": cmd_echo,
    "pwd": cmd_pwd,
    "cd": cmd_cd,
    "type": lambda args: type_command(args[0]) if args else print("type: missing argument"),
}


def command_not_found(command):
    print(f"{command}: command not found", file=sys.stderr)


def command_description(command):
    print(f"{command} is a shell builtin")


def type_command(command):
    if command in VALID_COMMANDS:
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


def find_executable(command):
    if os.path.isfile(command) and os.access(command, os.X_OK):
        return os.path.abspath(command)

    for directory in os.environ["PATH"].split(os.pathsep):
        fullpath = os.path.join(directory, command)
        if os.path.isfile(fullpath) and os.access(fullpath, os.X_OK):
            return fullpath

    return None


def main():
    while True:
        sys.stdout.write("$ ")
        user_input = input()
        user_input_list = shlex.split(user_input)
        if not user_input_list:
            continue
        command, *args = user_input_list

        executable = find_executable(command)
        if executable:
            subprocess.run([executable] + args)

        else:
            if command in BUILTINS:
                BUILTINS[command](args)
            else:
                command_not_found(command)


if __name__ == "__main__":
    main()
