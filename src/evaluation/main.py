from langchain_openai import OpenAIEmbeddings
from cosine_similarity import compute_similarity
import pandas as pd

if __name__ == "__main__":

    LLM = "anthropic:claude-sonnet-4.5"
    EMBEDDING_MODEL = "text-embedding-3-large"

    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    csv_path = ""  # fill with real file
    output_path = "./scoreboard.csv"

    # read csv into df
    df = pd.read_csv(csv_path)

    for row in df.iterrows():
        question = row['question']
        expected_answer = row['answer']

        # prompt UrbIa with the question
        # ...
        # answer = UrbIA(question)

        # compute similarity betweeen actual answer and expected answer
        similarity_score = compute_similarity(answer, expected_answer)

        # add data to scoreboard
     