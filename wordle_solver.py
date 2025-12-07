import math 
import pandas as pd


CSV = 'wordle.csv'
starter_words = ["slate", "crane", "adieu", "roate", "soare"]



def weighted_answers(CSV: str):
    df = pd.read_csv(CSV, header=0, usecols= [0,1], names=["word", "occurrence"])
    #h = df.head()
    #print(h)
    # cleaning data
    df["word"] = df["word"].astype(str).str.strip().str.lower()
    #change occurence to #
    df["occurrence"] = pd.to_numeric(df["occurrence"])
    
    # Remove Nas and non-positive probabilities
    df = df.dropna(subset=["occurrence"])
    df = df[df["occurrence"] > 0]

    # Normalize into probabilities
    total = df["occurrence"].sum()
    df["prob"] = df["occurrence"] / total
    #create lists
    word_list = df["word"].tolist()
    prob_list = df["prob"].tolist()

    return word_list, prob_list





def get_feedback(guess: str, answer: str):
    #get everything to lower case 
    guess = guess.lower()
    answer = answer.lower()

    gs343 = ["w" , "w" , "w" , "w" , "w"]
    #inital string is set w(gray)
    answer_chars = list(answer)

    # check for green
    for i in range(5):
        if guess[i] == answer[i]:
            gs343[i] = "g"
            answer_chars[i] = None

    # check for yellow 
    for i in range(5):
        if gs343[i] == "w":
            if guess[i] in answer_chars:
                gs343[i] = "y"
                x = answer_chars.index(guess[i])
                answer_chars[x] = None
    #join the list to string and return it
    return "".join(gs343)


def get_feedback(guess: str, answer: str):
    #get everything to lower case
    guess = guess.lower()
    answer = answer.lower()
    gs343 = ["w" , "w" , "w" , "w" , "w"]
    #inital string is set w(gray)
    answer_chars = list(answer)
 # check for green
    for i in range(5):
        if guess[i] == answer[i]:
            gs343[i] = "g"
            answer_chars[i] = None
 # check for yellow
    for i in range(5):
        if gs343[i] == "w":
            if guess[i] in answer_chars:
                gs343[i] = "y"
                x = answer_chars.index(guess[i])
                answer_chars[x] = None
 #join the list to string and return it
    return "".join(gs343)


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


if __name__ == "__main__":
    main()
    