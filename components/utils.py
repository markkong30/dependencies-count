import platform
import subprocess


def prompt_yes_no(question: str):
    while True:
        response = input(question + " (y/n): ")
        if response in ["y", "n"]:
            return response == "y"
        else:
            print("Invalid response. Please answer with 'yes' or 'no'.")


def open_file(file_path: str):
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.call(["open", file_path])
    elif system == "Windows":
        subprocess.call(["start", file_path], shell=True)
