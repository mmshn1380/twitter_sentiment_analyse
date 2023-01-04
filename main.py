from fastapi import FastAPI, HTTPException
from colabcode import ColabCode
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
import time , uvicorn , os

from twython import Twython

APP_KEY='lqDhb6PKIRIdp0BgV2oVtw79b'
ACCESS_TOKEN ='AAAAAAAAAAAAAAAAAAAAAOqnkwEAAAAAXR%2F%2B80S0B0QESggdwu2m16RcTqs%3DAbisOav2dl7qVvJ1nvnw2Y3YrYIzKzOwIMwddU8CjZROgZi749'
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Computional setiment analyse server"}

@app.get("/sentiment_analysis/")
def predict(sentence):
    res = None
    
    if res == None:
        raise HTTPException(status_code=404, \
            detail={'status': 'failure', 'msg': 'error in prediction!', 'type': 'predict'})
    return {'status': 'success', 'value': res, 'type': 'predict'}

@app.get("/search_twitter/")
def search_twitter(query,count):
    res = None
    search_results=twitter.search(count=count, q=query ,tweet_mode="extended")
    res=[tweet['full_text'] for tweet in search_results['statuses']]
    if res == None:
        raise HTTPException(status_code=404, \
            detail={'status': 'failure'})
    return {'status': 'success', 'value': res, 'type': 'search_twitter'}

cc = ColabCode(port=8000, code=False)
cc.run_app(app=app)