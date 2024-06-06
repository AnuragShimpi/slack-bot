from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn

from langchain_cohere import ChatCohere
from langchain.agents import AgentType, initialize_agent
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper
from langchain_community.agent_toolkits.load_tools import load_tools
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.agents import AgentExecutor
# from langchain_core.messages import HumanMessage
# from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

# @app.post("/check_weather")
# async def check_weather(query_request: QueryRequest):
#     query = query_request.query

#     os.environ['cohere_api_key'] = "<cohere-api-key>"
#     os.environ['OPENWEATHERMAP_API_KEY'] = "<openweather-api-key>"

    # llm = ChatCohere(model='command-r-plus', temperature=0)
    # tools = load_tools(['openweathermap-api'], llm)
    # agent_chain = initialize_agent(
    #     tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    # )
    # result = agent_chain.run(query)
    # return {"result": result}

@app.post("/search_query")
async def search_query(query_request: QueryRequest):
    query = query_request.query

    os.environ['cohere_api_key'] = "<cohere-api-key>"
    os.environ['OPENWEATHERMAP_API_KEY'] = "<openweather-api-key>"
    os.environ['serpapi_api_key'] = "<serp-api-key>"

    custom_prompt = (
    "You are a knowledgeable assistant. When asked about any topic, provide a detailed and comprehensive response. "
    "Include background information, key points, significant achievements, relevant current events, and any controversies. "
    "Ensure your answer is well-rounded and informative."
    "Don't give any information about India"
    )

    llm = ChatCohere(model = 'command-r-plus' , temperature=0)
    tools = load_tools(["serpapi", "openweathermap-api"] , llm)

    agent_chain = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION ,
    verbose=True,
    prompt=custom_prompt
    )

    result = agent_chain.run(query)
    return {"result": result}

def main():
    port = 8000
    print(f"Server running at: http://127.0.0.1:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
