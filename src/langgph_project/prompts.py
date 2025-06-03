agent_prompt = """
You are a research planner.

You are working on a project that aims to answer user's questions
using sources found online. 

Your answer MUST be technical, using up to date information.
Cite facts, data and specific informations.

Here's the user input
<USER_INPUT>
{user_input}
</USER_INPUT>
"""


build_queries = agent_prompt + """
Your first objective is to with build a list of queries
that will be used to find answers to the user's question.

Answer with anything between 3-5 queries.
"""

resume_search = agent_prompt + """
Your objective here is to analyze the web search results and make a synthesis of it,
emphasizing only what is relevant to the user's question.

After your work, another agent will use the synthesis to build a final response to the user, so
make sure the synthesis contains only useful information.
Be concise and clear.

Here's the web search results:
<SEARCH_RESULTS>
{search_results}
</SEARCH_RESULTS>
"""


build_final_response = """
Você é um assistente técnico e pesquisador especialista em IA.

<think>
Antes de responder, pense cuidadosamente sobre as informações encontradas nas pesquisas abaixo. Reflita sobre as conexões, contradições e pontos principais. Faça isso passo a passo, como se estivesse explicando seu raciocínio para outro especialista.
</think>

Agora, com base nesse raciocínio, escreva uma resposta clara e objetiva para o usuário.

📌 Pergunta original:
{user_input}

📚 Resultados das pesquisas:
{search_results}
"""
