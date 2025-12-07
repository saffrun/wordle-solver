def main():
    answers, probs = weighted_answers(CSV)

    print("Welcome to the Wordle Solver!")
    print("Here are some strong starter words:")
    print("  " + ", ".join(starter_words))
    print("\nAfter each guess, enter the feedback pattern using:")
    print("  g = green  (correct letter, correct position)")
    print("  y = yellow (correct letter, wrong position)")
    print("  w = gray   (letter not in word)")
    print("Example: guess = SLATE, pattern = gywwy\n")

    while True:
        print(f"\nCurrently, {len(answers)} possible answers remain.")

        if len(answers) == 0:
            print("No candidates remain. Did you enter a pattern incorrectly?")
            break

        if len(answers) == 1:
            print(f"The only possible answer is: {answers[0].upper()}")
            break

        guess = input("Enter your guess (5 letters, or 'q' to quit): ").strip().lower()
        if guess == "q":
            break
        if len(guess) != 5 or not guess.isalpha():
            # if it the guess is not 5 letters or not all letters
            print("Please enter a valid 5-letter word.")
            continue

        pattern = input("Enter pattern (g/y/w for each letter): ").strip().lower()
        if len(pattern) != 5 or any(c not in "gyw" for c in pattern):
            # if the pattern is not 5 character or contains invalid characters 
            #checks every character(c) in pattern to be g,y or w
            print("Pattern must be 5 characters of g/y/w (e.g., gywwy).")
            continue


        print(f"Got guess {guess.upper()} with pattern {pattern}.")
        print("Filtering logic coming soon... (placeholder)")
