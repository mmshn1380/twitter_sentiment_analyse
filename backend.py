from flask import render_template, redirect, url_for, flash, jsonify, request ,Flask
from pyngrok import ngrok
import uvicorn
import time , uvicorn , os , threading , pickle
import onnxruntime as ort
import numpy as np
from twython import Twython

APP_KEY='****'
ACCESS_TOKEN ='***'
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

os.environ["FLASK_ENV"] = "development"
app = Flask(__name__)
port = 5000
ngrok.set_auth_token("****")
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
app.config["BASE_URL"] = public_url

ort.set_default_logger_severity(3)
sequence_length = 200
vocab_size = 10000
with open('model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

model_path = "model/model_class.onnx"
ort_sess = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])

@app.route("/")
@app.route("/home")
@app.route("/home.html")
def root():
    return render_template('home.html')

@app.route("/manual")
@app.route("/manual.html")
def manual():
    return render_template('manual.html')

@app.route("/predict")
def predict():
    res = None
    sequences = tokenizer.texts_to_sequences([request.args.get('str', None)])
    padded = np.array(sequences)
    padded.resize((1, 200), refcheck=False)
    outputs = ort_sess.run(None, {'embedding_1_input': padded.astype(np.float32)})
    res = str(np.argmax(outputs[0]))
    return {'status': 'success', 'value': res, 'type': 'predict'}

@app.route("/search_twitter")
def search_twitter():
    res = None
    search_results=twitter.search(count=request.args.get('count', None), q=request.args.get('query', None) ,result_type='popular',lang='en',tweet_mode="extended")
    res=[tweet['full_text'] for tweet in search_results['statuses']]
    sense=[]
    for s in res:
      sequences = tokenizer.texts_to_sequences([s])
      padded = np.array(sequences)
      padded.resize((1, 200), refcheck=False)
      outputs = ort_sess.run(None, {'embedding_1_input': padded.astype(np.float32)})
      arg = np.argmax(outputs[0])
      sense.append(str(arg))
    
    return {'status': 'success', 'value': res, 'result':sense , 'type': 'search_twitter'}

threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
time.sleep(100000)