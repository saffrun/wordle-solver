import math 
import pandas as pd


CSV = 'wordle.csv'
starter_words = ["slate", "crane", "adieu", "roate", "soare"]


def weighted_answers(CSV: str):
    df = pd.read_csv(CSV, header=0, usecols=[0, 1], names=["word", "occurrence"])

    # cleaning data
    df["word"] = df["word"].astype(str).str.strip().str.lower()

    # change occurrence to numeric
    df["occurrence"] = pd.to_numeric(df["occurrence"])

    # Remove NaNs and non-positive probabilities
    df = df.dropna(subset=["occurrence"])
    df = df[df["occurrence"] > 0]

    # Normalize into probabilities
    total = df["occurrence"].sum()
    df["prob"] = df["occurrence"] / total

    # create lists
    word_list = df["word"].tolist()
    prob_list = df["prob"].tolist()

    return word_list, prob_list


def get_feedback(guess: str, answer: str):
    # get everything to lower case 
    guess = guess.lower()
    answer = answer.lower()

    # initial pattern is all gray ("w")
    pattern = ["w", "w", "w", "w", "w"]
    answer_chars = list(answer)

    # check for green
    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = "g"
            answer_chars[i] = None

    # check for yellow 
    for i in range(5):
        if pattern[i] == "w" and guess[i] in answer_chars:
            pattern[i] = "y"
            x = answer_chars.index(guess[i])
            answer_chars[x] = None

    # join the list to string and return it
    return "".join(pattern)


def filter_candidates(answers, probs, guess: str, pattern: str):
    new_answers = []
    new_probs = []

    # combine lists to make easier to parse
    for word, p in zip(answers, probs):
        if get_feedback(guess, word) == pattern:
            new_answers.append(word)
            new_probs.append(p)

    total = sum(new_probs)
    if total > 0:
        new_probs = [p / total for p in new_probs]

    return new_answers, new_probs
def weighted_guess_entropy(guess: str, answers, probs)-> float:
    pattern_prob = {} 
    #key->pattern, value-> probability mass 
    #probability of each pattern occuring given the guess0
    for word, p in zip(answers, probs):
        pattern = get_feedback(guess,word)
        #add prob to that pattern bucket
        pattern_prob[pattern] = pattern_prob.get(pattern,0.0)+p

    H = 0.0
    #calculate entropy
    for p in pattern_prob.values():
        if p > 0:
            H-= p * math.log2(p)
    return H 
    #return expected infomation gain(bits)

def best_weighted_guess(answers, probs, remaining=None):
    if remaining is None:
        remaining = answers
    best_word = None
    best_ent = -1.0
    #tries every remaining guess candidate and computes its entropy with the current answers and prob
    for r in remaining:
        e = weighted_guess_entropy(r,answers,probs)
        if e > best_ent:
            best_ent = e
            best_word = r
    return best_word, best_ent
    
def main():
    answers, probs = weighted_answers(CSV)

    print("Testing filter_candidates (no entropy yet).")
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
            # if the guess is not 5 letters or not all letters
            print("Please enter a valid 5-letter word.")
            continue

        pattern = input("Enter pattern (g/y/w for each letter): ").strip().lower()
        if len(pattern) != 5 or any(c not in "gyw" for c in pattern):
            # if the pattern is not 5 characters or contains invalid characters 
            print("Pattern must be 5 characters of g/y/w (e.g., gywwy).")
            continue


        answers, probs = filter_candidates(answers, probs, guess, pattern)

        if len(answers) > 1:
            best_guess, best_ent = best_weighted_guess(answers, probs)
            print(f"Suggested next guess (max weighted entropy): "
                  f"{best_guess.upper()}  (H = {best_ent:.3f} bits)")


if __name__ == "__main__":
    main()

    
