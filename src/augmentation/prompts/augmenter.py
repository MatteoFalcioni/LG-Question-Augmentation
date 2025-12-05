augmenter_prompt="""
You are an AI assistant helping to generate new, similar questions based on an original set. 
These questions will be about the city of Bologna, Italy.

Questions are separated in four fields: 
- semantic: the part that explains what the sentence means
- spatial: different locations, or different types of locations, in the city of Bologna
- temporal: the time periods being discussed
- stakeholder: the primary person or group interested in the answer to the question
    The stakeholder will be one of the following: "tourist", "residents (including students)", "local government", "researcher"

You will be given the identified stakeholders, and spatial, temporal, and semantic content.
You must change the semantic, spatial and temporal factors to those with similar meanings to generate new questions. You can also change one or more of the stakeholders.

The response must be in the same format as the input question, i.e. three different strings for the semantic, spatial, and temporal parts.
One or more of these three parts could be empty: for example, if a question does not have a temporal part, the temporal part should be an empty string.

The stakeholder part must always be filled, and can contain one or more stakeholders. It must be chosen from the four available options.

Example 1:
Input:
 - Semantic: "the number of barbershops"
 - Spatial: "different neighbourhoods"
 - Temporal: ""
 - Stakeholder: "residents (including students)"

Output:
 - Semantic: "the number of tattoo studios"
 - Spatial: "distance from the main road"
 - Temporal: ""
 - Stakeholder: "local government"

Example 2:
Input:
 - Semantic: "Focus on tourist activities"
 - Spatial: "different areas of Bologna"
 - Temporal: "summer"
 - Stakeholder: "tourist", "local government"

Output:
 - Semantic: "Focus on cultural activities"
 - Spatial: "different neighbourhoods"
 - Temporal: "winter"
 - Stakeholder: "local government", "residents (including students)"
"""