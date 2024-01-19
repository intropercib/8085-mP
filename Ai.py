import replicate
import json
import os

with open("API_KEY.json","r") as api_dict:
    api = json.load(api_dict)

#Set the REPLICATE_API_TOKEN environment variable
os.environ["REPLICATE_API_TOKEN"] = api["key"]

def generate(prompt:str):
    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt": api["pre-prompt"] + prompt.capitalize(),
            "temperature":0.1,"top_p":0.9,"max_length":512,
        }
    )

    response = ''

    for i in output:
        response += i
    print(prompt,response)    
    return response
