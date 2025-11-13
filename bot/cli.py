from bot.commands import handle_command

def run_bot():
    try:
        while True:
            user_input = input("Enter a command: ")
            if not user_input:
                continue

            result = handle_command(user_input, {}, {})
            if result == "exit":
                # place to save all data
                print("Good bye!")
                break
            elif result is not None:
                print(result)
    except KeyboardInterrupt:
        # place to save all data
        print("\nGood bye!")