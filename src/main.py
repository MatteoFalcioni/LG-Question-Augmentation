from make_graph import create_graph
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import datetime
import os


if __name__ == '__main__':

    load_dotenv()
    date = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    with open(f"logs_{date}.txt", "w") as f: # log has datetime to not overwrite
        f.write("separator_model = " + os.getenv("SEPARATOR_MODEL") + "\n")
        f.write("separator_temperature = " + os.getenv("SEPARATOR_TEMPERATURE") + "\n")
        f.write("augmenter_model = " + os.getenv("AUGMENTER_MODEL") + "\n")
        f.write("augmenter_temperature = " + os.getenv("AUGMENTER_TEMPERATURE") + "\n")
        f.write("collator_model = " + os.getenv("COLLATOR_MODEL") + "\n")
        f.write("collator_temperature = " + os.getenv("COLLATOR_TEMPERATURE") + "\n")

    graph = create_graph(plot_graph=False)

    input_file = "../data/test.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        config = {"configurable": {"thread_id": "1"}}
        print("--------------------------------\n")
        
        print(f"Processing question: {line}")

        msg = "Process the following question: \"" + line + "\""
        input_state = {"messages": [HumanMessage(content=msg)]} 
        
        result = graph.invoke(input_state, config=config)
        #print(result)