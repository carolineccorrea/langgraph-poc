import os
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langgraph.types import Send
from tavily import TavilyClient
import streamlit as st
from time import time
from dotenv import load_dotenv
from schemas import *
from prompts import *

load_dotenv()

print(os.getenv("TAVILY_API_KEY"))

llm = ChatOllama(model="phi3:3.8b")
reasoning_llm = ChatOllama(model="phi3:3.8b")

# NÓS


def build_first_queries(state: ReportState): 
    class QueryList(BaseModel):
        queries: List[str]
        
    user_input = state.user_input

    prompt = build_queries.format(user_input=user_input)
    query_llm = llm.with_structured_output(QueryList)
    result = query_llm.invoke(prompt)

    return {"queries": result.queries}

def spawn_researchers(state: ReportState):
    return [Send("single_search", query) 
            for query in state.queries]

def single_search(query: str):
    tavily_client = TavilyClient()

    results = tavily_client.search(query, 
                         max_results=1, 
                         include_raw_content=False)

    query_results = []
    for result in results["results"]:
        url = result["url"]
        url_extraction = tavily_client.extract(url)

        # print(url_extraction)
        if len(url_extraction["results"]) > 0:
            raw_content = url_extraction["results"][0]["raw_content"]
            prompt = resume_search.format(user_input=user_input,
                                        search_results=raw_content)

            llm_result = llm.invoke(prompt)
            query_results += [QueryResult(title=result["title"],
                                    url=url,
                                    resume=llm_result.content)]
    return {"queries_results": query_results}

def final_writer(state: ReportState):
    search_results = ""
    references = ""

    for i, result in enumerate(state.queries_results):
        search_results += f"[{i+1}]\n\nTitle: {result.title}\nURL: {result.url}\nContent: {result.resume}\n================\n\n"
        references += f"[{i+1}] - [{result.title}]({result.url})\n"

    prompt = build_final_response.format(user_input=state.user_input, search_results=search_results)
    llm_result = reasoning_llm.invoke(prompt)
    final_response = llm_result.content + "\n\nReferências:\n" + references
    return {"final_response": final_response}

# GRAFO

builder = StateGraph(ReportState)
builder.add_node("build_first_queries", build_first_queries)
builder.add_node("single_search", single_search)
builder.add_node("final_writer", final_writer)

builder.add_edge(START, "build_first_queries")
builder.add_conditional_edges("build_first_queries", spawn_researchers, ["single_search"])
builder.add_edge("single_search", "final_writer")
builder.add_edge("final_writer", END)

graph = builder.compile()

# STREAMLIT

if __name__ == "__main__":
    st.title("🌎 Local Perplexity")

    user_input = st.text_input("Qual a sua pergunta?", value="How is the process of building a LLM?")

    if st.button("Pesquisar"):
        with st.status("Gerando resposta..."):
            output = None
            for step in graph.stream({"user_input": user_input}, stream_mode="debug"):
                if step["type"] == "task_result":
                    st.write(f"🔧 Etapa: {step['payload'].get('name', 'Desconhecida')}")
                    st.write("📦 Resultado bruto:", step)
                    output = step

        if output and "payload" in output:
            payload = output["payload"]
            result = payload.get("result", [])

            if isinstance(result, list) and len(result) > 0:
                try:
                    response = result[0][1]

                    if "</think>" in response:
                        parts = response.split("</think>")
                        think_str = parts[0].strip()
                        final_response = parts[1].strip()

                        with st.expander("🧠 Reflexão", expanded=False):
                            st.write(think_str)

                        st.markdown("### 📄 Resposta final:")
                        st.write(final_response)
                    else:
                        st.warning("⚠️ A resposta não contém a tag </think>. Mostrando conteúdo completo.")
                        st.markdown("### 📄 Resposta:")
                        st.write(response)

                except Exception as e:
                    st.error("❌ Erro ao processar o conteúdo da resposta.")
                    st.exception(e)
                    st.write("Conteúdo de result[0]:", result[0])
            else:
                st.warning("⚠️ Nenhuma resposta válida retornada.")
                st.write("Conteúdo de `payload['result']`:", result)
        else:
            st.error("❌ Nenhuma saída capturada do grafo.")
