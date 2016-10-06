from flask import Flask, request, url_for, render_template
from app import app
from getLinkedInData import getData
from callPredictor import resume_predict
import json

@app.route('/', methods = ['GET', 'POST'])
def hello():
    """Renders a sample page."""
    if request.method == 'GET':
        return render_template('RequestPage.html')
    elif request.method == 'POST':
        handle = request.form['name']
        try:
            profile_data = getData(handle)
        except:
             return render_template('Invalid.html')
        profile_data["unit_id"] = "1"
        profile_data["decision"] = ""
        prediction = resume_predict(profile_data)
        if prediction == "":
            return render_template('Invalid.html')
        prediction = json.loads(prediction)
        label = prediction['Results']['output1'][0]['PredictedLabel']
        predictedLabel = "Accept" if label == "False" else "Reject"   
        score = float(prediction['Results']['output1'][0]['Probability'])
        if score < 0.5:
            score = 1 - score
        return render_template('ResponsePage.html', label = predictedLabel, score = int(score * 100))
    else:
        return "<h2>Error in request!</h2>"