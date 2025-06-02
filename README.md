# 🤖 Projeto IA com LangGraph, LangChain e LLMs

Este projeto utiliza **LangChain**, **LangGraph** e **modelos LLM locais com Ollama** para gerar respostas inteligentes a partir de entradas do usuário, estruturando o fluxo com grafos de estados. A aplicação possui uma interface via **Streamlit**.

## 🧩 Tecnologias utilizadas

- [LangChain](https://www.langchain.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Ollama](https://ollama.com/) — Modelos LLM locais (ex: Phi-3, Mistral, LLaMA)
- [Python 3.12+](https://www.python.org/)
- [Poetry](https://python-poetry.org/) — Gerenciador de dependências
- [Streamlit](https://streamlit.io/) — Interface web leve
- [Pydantic](https://docs.pydantic.dev/) — Validação de dados

---

## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Instale as dependências

```bash
poetry install
```

### 3. Ative o ambiente virtual do Poetry (opcional)

```bash
poetry shell
```

### 4. Certifique-se de que o modelo está rodando no Ollama

```bash
ollama run phi3
```

Você pode trocar `"phi3"` por outro modelo como `"mistral"`, `"llama3"` etc.

### 5. Rode a aplicação

```bash
poetry run streamlit run src/langgph_project/main.py
```

---

## 📁 Estrutura do projeto

```bash
src/
├── langgph_project/
│   ├── main.py              # Ponto de entrada Streamlit + LangGraph
│   ├── prompts.py           # Prompts utilizados na IA
│   ├── schemas.py           # Estrutura dos estados (Pydantic)
│   └── ...
```

---

## 📌 O que é LangGraph?

**LangGraph** é uma biblioteca que permite criar **fluxos de decisão com LLMs usando grafos de estados**, ideais para tarefas mais complexas do que simples prompts únicos.  
Permite loops, ramificações, múltiplas etapas e controle total do fluxo.

---

## ✨ Exemplo de uso

> O usuário envia um comando (ex: "explique o que é LangChain"), e o sistema:
1. Gera perguntas auxiliares com LLM,
2. Busca dados (em breve: RAG),
3. Gera uma resposta final estruturada.

---

## 📄 Licença

Este projeto está sob a licença MIT.  
Sinta-se à vontade para usar, contribuir e adaptar conforme necessário.

---

## 🙋‍♀️ Autora

Desenvolvido por [Caroline Castro](https://github.com/seu-usuario)
