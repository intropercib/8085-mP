from bardapi import BardCookies
import json
import os

with open("API_KEY.json","r") as api_dict:
    api = json.load(api_dict)

#Set the REPLICATE_API_TOKEN environment variable
os.environ["REPLICATE_API_TOKEN"] = api["key"]

with open("API_KEY.json","r") as api_dict:
    api = json.load(api_dict)

def generate(prompt:str):
    token = api["key"]
    cookie_dict = {
        "__Secure-1PSID":api["key"],
        "__Secure-1PSIDTS":api["TSID"],
        "__Secure-1PSIDCC":api["CCID"],
    }
    bard = BardCookies(cookie_dict=cookie_dict)
    return bard.get_answer(f"{api['pre-prompt']} {prompt}")['content']
