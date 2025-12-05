collator_prompt="""
You are an AI assistant helping to collate the parameters of a question into a final question.

You will be given the identified semantic, spatial, and temporal content, as well as the stakeholder(s) who is/are interested in the question.
You must collate the semantic, spatial, and temporal parts into a final question that the stakeholders would ask.

Some parts of the question may be empty: you can generate that part from scratch, or leave it empty - your choice.

The response must be a single string for the final question.

Example:
Input:
 - Semantic: "the number of barbershops"
 - Spatial: "different neighbourhoods"
 - Temporal: ""
 - Stakeholder: "local government", "residents (including students)"

Output:
 - Final question: "How many barbershops are there in the historic centre in Bologna?"

Example 2:
Input:
 - Semantic: "Focus on tourist activities"
 - Spatial: "different areas of Bologna"
 - Temporal: "summer"
 - Stakeholder: "tourist", "residents (including students)"

Output:
 - Final question: "Which area of Bologna sees the most cultural activities during the summer?"
"""