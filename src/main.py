from make_graph import create_graph
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import datetime
import os
#import csv


if __name__ == '__main__':

    load_dotenv()
    date = datetime.datetime.now().strftime("%d%m%Y_%H%M")
# issue with taking longer than 1 minute for the code to run - suggested to move to the graph file but since that runs each question separately I think it could create more than file per run
#is now working as long as the minute doesn't change during the run
folder_path = "./logs"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


os.makedirs(f"./logs/logs_{date}")
file_path = os.path.join(f'./logs/logs_{date}', f'logs_{date}.txt')

with open(file_path, 'w') as f:
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
        print("="*80)
        
        print(f"\nProcessing question: {line}\n")

        msg = "Process the following question: \"" + line + "\""
        input_state = {"messages": [HumanMessage(content=msg)]} 
        
        result = graph.invoke(input_state, config=config)
        print("="*80)
        print(result)