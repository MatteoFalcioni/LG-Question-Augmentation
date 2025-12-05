"""this code look will look at one question at a time from the UrbIA test questions set, using a conditional node
- the first node will split the question into three components: semantic, spatial, and temporal, using an LLM call
- It will then store these sections in a global variable, called 'question_parameters'
- then will make another LLM call to change these parameters into one or more new questions
- these new questions will then be appended to the state messages
- The questions will then be appended to a text file, ready to use for testing.
Once complete, the program will restart with a new question from the list.
"""

from typing import TypedDict, Annotated, Sequence #annotated adds additional context about the data type without affecting the type - ie describing something as an email address
from langchain_core.messages import BaseMessage #foundational class for all message types, is a parent type
from langchain_core.messages import HumanMessage, AIMessage #message from the user to the LLM
from langchain_core.messages import SystemMessage #message for providing instructions to the LLM
from langchain_openai import ChatOpenAI #importing the chat model from langchain
from langgraph.graph.message import add_messages #reducer function: tells us how to merge new data into the current state, rather than replacing the value entirely
from langgraph.graph import StateGraph, END #importing the graph classes used
from dotenv import load_dotenv #where the api key is stored secretly

load_dotenv() #loading the env file which contains the API key

temp = 0.7 #temperature setting for the llm model, chosen a high value to encourage varied outputs
model = ChatOpenAI(model="gpt-4o", temperature=temp) #setting up the llm model -  using gpt-4o

question_parameters = "" #creating a global variable to store the separated parameters

class AgentState(TypedDict): # setting up a typed dict to define the state structure of the agent
    messages: Annotated[Sequence[BaseMessage], add_messages] #the state stores a list of messages. add_messages is part of annotated and will append new messages to a list rather than replacing them
    semantic: str #the separated semantic content
    spatial: str #the separated spatial content
    temporal: str #the separated temporal content
    line_index: int #the current line being processed from the UrbIA questions file, in order to keep track of which lines have already been modified

with open("UrbIA_Questions_English.txt","r") as file: # opening the file once at the start to read lines from
    stripped_lines = [line.strip() for line in file if line.strip()] #stripping leading/trailing whitespaces and empty lines to make the file easier to read

#first node: will separate the parameters of the question into semantic, spatial, and temporal using an llm call
def separate_parameters(state: AgentState) -> AgentState:
    print ("Running separate_parameters") # used for debugging
    system_prompt = SystemMessage(content=f"""
     this node is used to analyse the composition of the input, and to highlight which parts are semantic, temporal, or spatial
    Args:
        semantic content is the part that explains what the sentence means
        spatial content refers to different locations, or different types of locations, in the city of Bologna
        temporal content refers to the time periods being discussed
        """) #instrctions for the model on how to separate the parameters
    model.invoke([system_prompt] + state["messages"]) #invoking the model with the system prompt and the current messages in the state
    global question_parameters #used to store the separated parameters in a global variable
    question_parameters = state['messages'][-1].content #assuming the last message contains the separated parameters
    return {"messages": [AIMessage(content=f"Successfully separated parameters. Current parameters are: {question_parameters}")],
            "semantic": "semantic content", #I want this to return the separated parameters inside of the state, but also store them in a global variable, question_parameters, however I'm not sure if they are actually accessed if I store them like this?
            "spatial": "spatial content",
            "temporal": "temporal content"
           } #returns the typed dict with the updated state

#change node will change the semantic, spatial, and temporal parts of the question, stored in the global variable, question_parameters, with new, similar ones to generate new questions
def change_parameters(state: AgentState) -> AgentState: #this node will change the parameters stored in the global variable, question_parameters
    print("Running change_parameters")
    system_prompt = SystemMessage(content=f"""
    You are an AI assistant helping to generate new, similar questions based on an original set. Use the parameters analysed in the separate_parameters node to generate new questions of the same type.
    These questions should be about the city of Bologna, Italy, and relevant to one or more of the stakeholders identified: researchers, local government, and residents.
    
    this node will use the identified spatial, temporal, and semantic content from the separate_parameters node and {question_parameters}, then change the semantic, spatial, and temporal meanings with similar ones to generate new questions about the city of Bologna, and save them in the 'new_questions' variable.
    Args:
        semantic content is the part that explains what the sentence means
        spatial content refers to different locations, or different types of locations, in the city of Bologna
        temporal content refers to the time periods being discussed
    
    The response should only be a list of 5-10 new questions per input question, each on a new line.
    """)
    response = model.invoke([system_prompt]) #invokes the model with the system prompt above, and returns a response #try invoking the whole state
    return {"messages": [response]} #returns a typed dict with the new questions, 'response',  stored in messages

# setting up the third node that appends the generated questions to a text file
def append_node(state: AgentState) -> AgentState:
    print("Running append_node")
    last_message = state["messages"][-1] #looking at the last message (the new questions generated)
    #for debugging:
    #print("Input message:", last_message)
    #print("Type of last_message:", type(last_message))
    with open("generated_UrbIA_questions.txt", "a") as file: #opens file in append mode
        file.write (last_message.content + "\n") #extract content from the last message and write to file
    print("Content written to file.") #debugging statement
    return {"messages": [AIMessage(content="New questions appended to generated_UrbIA_questions.txt")]} #returns a valid typed dict

#setting up the fourth node: a loop that will use the index to read one line at a time from the UrbIA questions file
def loop_questions(state: AgentState) -> AgentState: #using state to keep track of progress
    """this function will loop through each line in the UrbIA questions file, returning 'continue' until the end of the file is reached, when it will return 'end' to stop the process"""
    index = state.get("line_index")  # updating the variable 'index' with the current line index from the state
    if index >= len(stripped_lines): #checking if the index is greater than or equal to the number of lines in the file
        print("End of file")
        return {"messages": [AIMessage(content="End of questions.")], "line_index": index} #returns the state and updates the line index
    
    next_question = stripped_lines[index] #the next question is the next line in the file
    print(f"Question n.{index}: {next_question}") # print the question being looked at from the UrbIA questions file
    
    return {
        "messages": [HumanMessage(content=next_question)],
        "semantic": "",
        "spatial": "",
        "temporal": "",
        "line_index": index + 1
    } #returns the state with the new question and increments the line index by 1

# setting up a function that will be used as a conditional edge to decide if there are more questions in the txt file or if it is at the end
def should_continue(state: AgentState) -> str: #using the line index from the state to determine the last line parsed, then returning a string that will be used to decide which edge to use
    if state["line_index"] >= len(stripped_lines): #if the line index is greater than or equal to the number of lines in the file then it will return 'end'
        return "end"
    else: #else it will return 'continue', which is an edge that loops back to the first node
        return "continue"



#Setting up the graph:
graph = StateGraph(AgentState)
graph.add_node("separate_parameters", separate_parameters)
graph.add_node("change_parameters", change_parameters)
graph.add_node("append_node", append_node)
graph.add_node("loop_questions", loop_questions)

graph.add_edge("separate_parameters", "change_parameters")
graph.add_edge("change_parameters", "append_node")
graph.add_edge("append_node", "loop_questions")
graph.add_conditional_edges(
    "loop_questions",  #node that runs the condition
    should_continue,  #function that tests the condition
    {
        "continue": "separate_parameters",
        "end": END
    }
)

graph.set_entry_point("separate_parameters") #starting point of the graph
app = graph.compile() #compiling the graph as app

with open("restructured_questions_graph.png", "wb") as file: #saving a .png of the graph as restructured_questions_graph.png
    file.write(app.get_graph().draw_mermaid_png())

# setting up the initial state with empty parameters
inputs = {
    "messages":"",
    "semantic": "",
    "spatial": "",
    "temporal": "",
    "line_index": 0
    }

#simplified version without intermediate outputs:
final = app.invoke(inputs)