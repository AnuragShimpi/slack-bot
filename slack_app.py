import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_cohere import ChatCohere
from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentType, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env')

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

#Langchain implementation
template = """Assistant is a large language model trained by OpenAI.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

    Human: {human_input}
    Assistant:"""

prompt = PromptTemplate(
    input_variables=["human_input"], 
    template=template
)

agent_chain = LLMChain(
    llm=ChatCohere(cohere_api_key=os.environ.get("cohere_api_key"),
                model = 'command-r-plus' , 
                temperature=0),
                prompt=prompt, 
                verbose=True, 
                memory=ConversationBufferWindowMemory(k=2),
)

# llm = ChatCohere(cohere_api_key=os.environ.get("cohere_api_key"),
#                  model = 'command-r-plus' , 
#                  temperature=0,
#                  )
# tools = load_tools(["serpapi", "openweathermap-api"],
#                     llm,
#                     )

# agent_chain = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION ,
#     verbose=True,
#     prompt=prompt,
#     memory=ConversationBufferWindowMemory(k=2)
#     )

#Message handler for Slack
@app.message(".*")
def message_handler(message, say, logger):
    print(message)
    
    output = agent_chain.predict(human_input = message['text'])   
    say(output)



# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()