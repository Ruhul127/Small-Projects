import random

def calculate_points(attempts, max_attempts):
    """
    Calculate points based on the number of attempts.
    """
    if attempts == 1:
        return 100
    elif attempts <= max_attempts // 2:
        return 50
    else:
        return 10

def is_prime(n):
    """
    Check if a number is prime.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def give_hint(number_to_guess, guess):
    """
    Provide a hint based on whether the number is odd/even and prime.
    """
    if number_to_guess % 2 == 0:
        hint = "The number is even."
    else:
        hint = "The number is odd."
    
    if is_prime(number_to_guess):
        hint += " It is also a prime number."
    else:
        hint += " It is not a prime number."

    if number_to_guess > guess:
        hint += " The number is greater than your guess."
    else:
        hint += " The number is less than your guess."
    
    return hint

def number_guessing_game():
    """
    Main function to run the number guessing game.
    """
    max_attempts = 10
    total_points = 0

    # Get the player's name once at the start
    print("Welcome to the Number Guessing Game!")
    player_name = input("Please enter your name: ")

    while True:
        print(f"\nHello, {player_name}! I have selected a number between 1 and 100. Try to guess it!")

        number_to_guess = random.randint(1, 100)
        guess = None
        attempts = 0

        while guess != number_to_guess:
            try:
                guess = int(input("Enter your guess: "))
                attempts += 1

                if guess < number_to_guess:
                    print("Too low! Try again.")
                elif guess > number_to_guess:
                    print("Too high! Try again.")
                else:
                    print(f"Congratulations, {player_name}! You guessed the correct number {number_to_guess} in {attempts} attempts.")
                    points = calculate_points(attempts, max_attempts)
                    total_points += points
                    print(f"You earned {points} points. Total points: {total_points}")
                    break

                # Provide a hint every third attempt
                if attempts % 3 == 0:
                    hint = give_hint(number_to_guess, guess)
                    print(f"Hint: {hint}")

                if attempts >= max_attempts:
                    print(f"Sorry, {player_name}. You've reached the maximum number of attempts. The number was {number_to_guess}.")
                    break

            except ValueError:
                print("Please enter a valid integer.")

        # Ask if the player wants to play again
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print(f"Thank you for playing, {player_name}! Your final score is {total_points} points.")
            break

# Run the game
number_guessing_game()
