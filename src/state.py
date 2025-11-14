from langchain.agents import AgentState
from typing_extensions import Annotated
from typing import Literal


def replace_str(left : str, right : str)-> str:
    """Replaces str"""
    if left is None:
        left= ""
    if right is None:
        right= ""
    
    return right

class QuestionState(AgentState):
    """
    Define other fields other than messages
    """
    semantic : Annotated[str, replace_str]
    temporal : Annotated[str, replace_str]
    spatial : Annotated[str, replace_str]
    stakeholder : Annotated[str, replace_str] # should this be a string literal/list 

from pydantic import BaseModel, Field
class ComponentOutput(BaseModel):
    semantic : str = Field(description="The semantic question") 
    temporal : str = Field(description="The temporal question")
    spatial : str = Field(description="The spatial question")
    stakeholder : Literal["residents (including students)", "local government", "tourist", "researcher"] = Field(description="The stakeholder(s) interested in the question")

class QuestionOutput(BaseModel):
    final_question : str = Field(description="The final question combining all parameters") 


'''    questions = {
        0 : {
        "semantic" : "...",
        "temporal" : "...",
        "spatial" : "...",
        "stakeholder" : "..."
        },
        1 : {
        "semantic" : "...",
        "temporal" : "...",
        "spatial" : "...",
        "stakeholder" : "..."
        }
        }'''