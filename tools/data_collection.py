import os
import sys
import asyncio
import json

from dotenv import load_dotenv

#import the app.py module to gain access to the methods to construct payloads and
#call the API through the sdk

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app

#function to enable loading of the .env file into the global variables of the app.py module

def load_env_into_module(module_name, prefix=''):
***REMOVED***load_dotenv()
***REMOVED***module = __import__(module_name)
***REMOVED***for key, value in os.environ.items():
***REMOVED***if key.startswith(prefix):
***REMOVED******REMOVED***setattr(module, key[len(prefix):], value)

load_env_into_module("app")

#some settings required in app.py

app.SHOULD_STREAM = False
app.SHOULD_USE_DATA = app.should_use_data()

#format:
"""
[
  {
***REMOVED***"qa_pairs":[{"question":"...", "answer":"..."}]
  }
]
"""

generated_data_path = r"path/to/qa_input_file.json"

with open(generated_data_path, 'r') as file:
***REMOVED***data = json.load(file)


"""
Process a list of q(and a) pairs outputting to a file as we go.
"""
async def process(data: list, file):
  for qa_pairs_obj in data:
***REMOVED***  qa_pairs = qa_pairs_obj["qa_pairs"]
***REMOVED***  for qa_pair in qa_pairs:
***REMOVED***  question = qa_pair["question"]
***REMOVED***  messages = [{"role":"user", "content":question}]

***REMOVED***  print("processing question "+question)

***REMOVED***  request = {"messages":messages, "id":"1"}

***REMOVED***  response = await app.complete_chat_request(request)

***REMOVED***  #print(json.dumps(response))

***REMOVED***  messages = response["choices"][0]["messages"]

***REMOVED***  tool_message = None
***REMOVED***  assistant_message = None

***REMOVED***  for message in messages:
***REMOVED******REMOVED***if message["role"] == "tool":
***REMOVED******REMOVED***  tool_message = message["content"]
***REMOVED******REMOVED***elif message["role"] == "assistant":
***REMOVED******REMOVED***  assistant_message = message["content"]
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***  raise ValueError("unknown message role")

***REMOVED***  #construct data for ai studio evaluation

***REMOVED***  user_message = {"role":"user", "content":question}
***REMOVED***  assistant_message = {"role":"assistant", "content":assistant_message}

***REMOVED***  #prepare citations
***REMOVED***  citations = json.loads(tool_message)
***REMOVED***  assistant_message["context"] = citations

***REMOVED***  #create output
***REMOVED***  messages = []
***REMOVED***  messages.append(user_message)
***REMOVED***  messages.append(assistant_message)

***REMOVED***  evaluation_data = {"messages":messages}

***REMOVED***  #incrementally write out to the jsonl file
***REMOVED***  file.write(json.dumps(evaluation_data)+"\n")
***REMOVED***  file.flush()


evaluation_data_file_path = r"path/to/output_file.jsonl"  

with open(evaluation_data_file_path, "w") as file:
  asyncio.run(process(data, file))








