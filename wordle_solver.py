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



def main():
    words, probs = weighted_answers(CSV)

    #tests
    print(f"Loaded {len(words)} words.")
    print(f"First 10 words: {words[:10]}")
    print(f"First 10 probabilities: {probs[:10]}")
    print(f"Sum of probabilities: {sum(probs)}")




if __name__ == "__main__":
    main()
