from connectAPI import *
from helper import *

# This valiateQuery function is use to Validate the payload data["prompt"] is not empty and string format.
def valiateQuery(data):
    try:
        if "Question" in data:
            if data["Question"] != "":
                return ConnectChatBot(data)
            else:
                return {
                    "message":"Invaild data !",
                    "statusCode":400
                }
        else:
            return {
                "message":"All fields (Question) are required.",
                "statusCode":400
            }
    except Exception as e:
        return {
                "message":str(e),
                "statusCode":400,
                "status":True
            }