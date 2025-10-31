from state import QuestionState, ComponentOutput, QuestionOutput
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from prompts.augmenter import augmenter_prompt 
from prompts.separator import separator_prompt 
from prompts.collator import collator_prompt
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

separator_agent = create_agent(
    model=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    tools=[],
    system_prompt=separator_prompt,
    state_schema=QuestionState,
    response_format=ComponentOutput
)

augmenter_agent = create_agent(
    model=ChatOpenAI(model="gpt-4.1", temperature=0.7),  # probably higher T in order to have several different augmentations
    tools=[],
    system_prompt=augmenter_prompt,
    state_schema=QuestionState,
    response_format=ComponentOutput
)

collator_agent = create_agent(
    model=ChatOpenAI(model="gpt-4.1", temperature=0),
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

    def collate_parameters(state : QuestionState) -> QuestionState:
        """Collates the parameters using the collator agent"""
        file_path = "./output.txt"

        print(f"***State: {state}***")

        messages = [HumanMessage("Combine the parameters into a final question")]

        result = collator_agent.invoke({"temporal": state['temporal'], "spatial": state['spatial'], "semantic": state['semantic'], "messages": messages})
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

 


