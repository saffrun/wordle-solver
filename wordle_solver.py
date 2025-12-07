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


def main():
    words, probs = weighted_answers(CSV)
    #tests
    print(f"Loaded {len(words)} words.")
    print(f"First 10 words: {words[:10]}")
    print(f"First 10 probabilities: {probs[:10]}")
    print(f"Sum of probabilities: {sum(probs)}")
    tests = [
        ("wagwa", "wagon"),
        ("plate", "leaps"),
        ("allar", "apple"),
        ("soare", "soare"),
    ]
    for guess, answer in tests:
        pattern = get_feedback(guess, answer)
        print(f"guess = {guess}, answer = {answer} -> {pattern}")


if __name__ == "__main__":
    main()
    