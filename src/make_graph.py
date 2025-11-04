from state import QuestionState, ComponentOutput, QuestionOutput
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
#from langchain_anthropic import ChatAnthropic
from prompts.augmenter import augmenter_prompt 
from prompts.separator import separator_prompt 
from prompts.collator import collator_prompt
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import os

load_dotenv()

separator_model = os.environ.get("SEPARATOR_MODEL", "gpt-4.1")
augmenter_model = os.environ.get("AUGMENTER_MODEL", "gpt-4.1")
collator_model = os.environ.get("COLLATOR_MODEL", "gpt-4o")

separator_temperature = float(os.environ.get("SEPARATOR_TEMPERATURE", 0.7))
augmenter_temperature = float(os.environ.get("AUGMENTER_TEMPERATURE", 0.7))
collator_temperature = float(os.environ.get("COLLATOR_TEMPERATURE", 0.7))

separator_agent = create_agent(
    model=ChatOpenAI(model=separator_model, temperature=separator_temperature),
    tools=[],
    system_prompt=separator_prompt,
    state_schema=QuestionState,
    response_format=ComponentOutput
)

augmenter_agent = create_agent(
    model=ChatOpenAI(model=augmenter_model, temperature=augmenter_temperature),  # probably higher T in order to have several different augmentations
    tools=[],
    system_prompt=augmenter_prompt,
    state_schema=QuestionState,
    response_format=ComponentOutput
)

collator_agent = create_agent(
    model=ChatOpenAI(model=collator_model, temperature=collator_temperature),
    tools=[],
    system_prompt=collator_prompt,
    state_schema=QuestionState,
    response_format=QuestionOutput
)

def create_graph(plot_graph=False) -> StateGraph:
    def separate_parameters(state : QuestionState) -> QuestionState:
        """Separates the parameters using the separator agent"""
        result = separator_agent.invoke(state)
        structured_result = result["structured_response"]  # this is an OutputTemplate object

        return {
            "semantic" : structured_result.semantic,
            "temporal" : structured_result.temporal,
            "spatial" : structured_result.spatial,
            "stakeholder" : structured_result.stakeholder
        }

    def augment_parameters(state : QuestionState) -> QuestionState:
        """Augments the parameters using the augmenter agent"""
        result = augmenter_agent.invoke({"messages": [HumanMessage(f"Update the following parameters: \n\nSemantic: {state['semantic']}\nTemporal: {state['temporal']}\nSpatial: {state['spatial']}")]})
        structured_result = result["structured_response"]  # this is an OutputTemplate object

        return {
            "semantic" : structured_result.semantic,
            "temporal" : structured_result.temporal,
            "spatial" : structured_result.spatial,
            "stakeholder" : structured_result.stakeholder
        }

    def collate_parameters(state : QuestionState) -> QuestionState:
        """Collates the parameters using the collator agent"""
        file_path = "./output.txt"

        message = [HumanMessage(f"Combine the following parameters into a final question: \n\nSemantic: {state['semantic']}\nTemporal: {state['temporal']}\nSpatial: {state['spatial']}")]

        result = collator_agent.invoke({"messages": message})
        structured_result = result["structured_response"]  # this is an QuestionOutput object

        final_question = structured_result.final_question
        print(f"***Final question: {final_question}***")
        with open(file_path, "a") as f:
            f.write(final_question + "\n")


    builder = StateGraph(QuestionState)

    builder.add_node("separate_parameters", separate_parameters)
    builder.add_node("augment_parameters", augment_parameters)
    builder.add_node("collate_parameters", collate_parameters)

    builder.add_edge(START, "separate_parameters")
    builder.add_edge("separate_parameters", "augment_parameters")
    builder.add_edge("augment_parameters", "collate_parameters")
    builder.add_edge("collate_parameters", END)

    graph = builder.compile()

    if plot_graph:
        print("Plotting graph to graph.png")
        with open("./graph.png", "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())

    return graph

 


