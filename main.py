def greet_user():
    print("Welcome to your interactive Python GitHub project!")
    user_input = input("Enter your name (or type 'exit' to quit): ")

    if  user_input.strip().lower() == 'exit':
        print("Goodbye!")
    else:
        print(f"Hello, {user_input}! Glad to bring you on board!!")

if __name__ == "__main__":
    greet_user()