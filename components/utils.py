def prompt_yes_no(question):
    while True:
        response = input(question + " (y/n): ")
        if response in ["y", "n"]:
            return response == "y"
        else:
            print("Invalid response. Please answer with 'yes' or 'no'.")
