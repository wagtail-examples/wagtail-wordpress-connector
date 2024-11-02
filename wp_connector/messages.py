import sys


class ClientExitException(Exception):
    def error_message(self, message):
        sys.stdout.write(f"ERROR:   {message}\n")
        exit(1)


class ClientMessage:
    def success_message(self, message):
        sys.stdout.write(f"SUCCESS: {message}\n")

    def info_message(self, message):
        sys.stdout.write(f"INFO:    {message}\n")
