from state import QuestionState, ComponentOutput, QuestionOutput
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from prompts.augmenter import augmenter_prompt 
from prompts.separator import separator_prompt 
from prompts.collator import collator_prompt
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

separator_agent = create_agent(
    model=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    tools=[],
    system_prompt=separator_prompt,
    state_schema=QuestionState,
    response_format=ComponentOutput
)

augmenter_agent = create_agent(
    model=ChatOpenAI(model="gpt-4.1", temperature=0.7),  # probabòy higher T in order to have several different augmentations
    tools=[],
    system_prompt=augmenter_prompt,
    state_schema=QuestionState,
    response_format=ComponentOutput
)

final_agent = create_agent(
    model=ChatOpenAI(model="gpt-4o-mini", temperature=0),
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
            "spatial" : structured_result.spatial
        }

    def augment_parameters(state : QuestionState) -> QuestionState:
        """Augments the parameters using the augmenter agent"""
        result = augmenter_agent.invoke(state)
        structured_result = result["structured_response"]  # this is an OutputTemplate object

        return {
            "semantic" : structured_result.semantic,
            "temporal" : structured_result.temporal,
            "spatial" : structured_result.spatial
        }

    def generate_final_question(state : QuestionState) -> QuestionState:
        """Generates the final question using the final agent"""
        file_path = "./output.txt"

        result = final_agent.invoke(state)
        structured_result = result["structured_response"]  # this is an QuestionOutput object

        final_question = structured_result.final_question
        with open(file_path, "a") as f:
            f.write(final_question + "\n")


    builder = StateGraph(QuestionState)

    builder.add_node("separate_parameters", separate_parameters)
    builder.add_node("augment_parameters", augment_parameters)
    builder.add_node("generate_final_question", generate_final_question)

    builder.add_edge(START, "separate_parameters")
    builder.add_edge("separate_parameters", "augment_parameters")
    builder.add_edge("augment_parameters", "generate_final_question")
    builder.add_edge("generate_final_question", END)

    graph = builder.compile()

    if plot_graph:
        print("Plotting graph to graph.png")
        with open("./graph.png", "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())

    return graph

 


