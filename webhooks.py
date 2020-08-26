from json import dumps
from requests import post

from settings import get_submissions_webhook

def post_submissions_embed(data):
    try:
        data = dumps({"embeds":[data]})
        request = post(get_submissions_webhook(), data=data, headers={"Content-Type":"application/json"})
        if request.status_code in [200, 204]:
            print("Succesfully messaged using webhook.")
        else:
            print("Problem messaging using webhook.")
    except:
        pass
