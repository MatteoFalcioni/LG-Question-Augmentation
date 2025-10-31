from make_graph import create_graph
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage


if __name__ == '__main__':

    load_dotenv()
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