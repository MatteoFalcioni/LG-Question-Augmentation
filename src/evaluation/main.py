from langchain_openai import OpenAIEmbeddings
import uuid
import pandas as pd
import os
from urbia.context import set_thread_id
from evaluation.cosine_similarity import compute_similarity
from dotenv import load_dotenv
from urbia.graph import make_graph

if __name__ == "__main__":

    load_dotenv()

    # Initialize UrbIA graph
    keys_dict = {
        "openai_key" : os.getenv("OPENAI_API_KEY"),
        "anthropic_key" : os.getenv("ANTHROPIC_API_KEY")
    }
    urbia = make_graph(
        plot_graph=True, 
        user_api_keys=keys_dict,
        checkpointer=None  # no memory!
    )

    # Initialize OpenAI embeddings
    EMBEDDING_MODEL = (os.getenv("EMBEDDING_MODEL")).lower()  
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    # Define input and output csv paths
    input_csv_path = ""  # fill with real file
    output_path = "./scoreboard.csv"

    # list to store scoreboard
    scoreboard = []
    # read csv into df
    df = pd.read_csv(input_csv_path)

    # each row is a question and answer pair
    for row in df.iterrows():

        try:
            # Fresh sandbox per question
            set_thread_id(uuid.uuid4())
            question = row['question']
            expected_answer = row['answer']

            # prompt UrbIa with the question
            # ...
            # answer = UrbIA(question)

            # compute similarity betweeen actual answer and expected answer
            similarity_score = compute_similarity(answer, expected_answer, embeddings)

            # add data to scoreboard
            scoreboard.append({
                "question": question,
                "answer": answer,
                "expected_answer": expected_answer,
                "similarity_score": similarity_score
            })
        except Exception as e:
            print(f"Error processing question {question}: {e}")
            continue

    # save scoreboard to csv
    pd.DataFrame(scoreboard).to_csv(output_path, index=False)