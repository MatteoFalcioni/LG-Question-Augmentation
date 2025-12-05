from cosine_similarity import compute_similarity
import pandas as pd

if __name__ == "__main__":

    csv_path = ""  # fill with real file
    output_path = "./scoreboard.csv"

    # read csv into df
    df = pd.read_csv(csv_path)

    for row in df.iterrows():
        question = row['question']
        expected_answer = row['answer']

        # prompt UrbIa with the question
        # ...

        # compute similarity betweeen actual answer and expected answer
        similarity_score = compute_similarity(answer, expected_answer)

        # add data to scoreboard
     