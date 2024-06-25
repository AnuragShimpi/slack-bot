import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv('.env')

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN2"))


# base_url = "https://webapp-be-nlq.azurewebsites.net"

base_url = "http://0.0.0.0:8000"

def call_search_api(query: str):
    payload = {"input": query}
    response = requests.post(f"{base_url}/search_query", json=payload)
    if response.status_code == 200:
        return response.json().get("result")
    else:
        return f"Failed to call search API: {response.status_code}, {response.text}"


#Message handler for Slack
@app.message(".*")
def message_handler(message, say, logger):
    print(message)
    
    output = call_search_api(message['text'])
    say(output)
    
    print(output)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN2"]).start()