from flask import Flask, request, url_for, render_template
from app import app
from getLinkedInData import getData, getHTML
from callPredictor import resume_predict
import json
from bs4 import BeautifulSoup

@app.route('/', methods = ['GET', 'POST'])
def hello():
    """Renders a sample page."""
    if request.method == 'GET':
        return render_template('RequestPage.html')
    elif request.method == 'POST':
        handle = request.form['name']
        try:
            html_body = getHTML(handle)
            profile_data = getData(html_body, handle)
        except:
             return render_template('Invalid.html')
      
        prediction = resume_predict(profile_data)
        if prediction == "":
            return render_template('Invalid.html')
        prediction = json.loads(prediction)
        label = prediction['Results']['output1'][0]['PredictedLabel']
        predictedLabel = "Accept" if label == "False" else "Reject"   
        score = float(prediction['Results']['output1'][0]['Probability'])
        page = 'ResponsePageReject.html'
        if score < 0.5:
            score = 1 - score
            page = 'ResponsePageAccept.html'
        data = {
"0 (accepted)": {
"undefined": None
},
"roles": {
"data": -1,
"engineer": -0.3771569,
"analyst": -0.2214854,
"analytics": -0.2155646,
"scientist": -0.1922189,
"-": 0.0640342,
"president": 0.05838439,
"director": 0.09142493
},
"headline": {
"data": -0.6861926,
",": 0.07813177
},
"skills": {
"data": -0.2632319,
"_": 0.5742549
},
"companies": {
"_": -0.7256273
},
"schools": {
"_": -0.4342133
},
"summary": {
"data": -0.2409923,
"": 0.1275924,
",": 0.2316926
},
"connections": {
"500+": 0.3418371
}
}
        jsfile = open("static/js/html-feature-importance.js", "r")
        js_contents = jsfile.read()
        #print(js_contents)
        script_html = BeautifulSoup("<script>var featureImportance=" + json.dumps(data) + ";" + str(js_contents) + "</script>", "html.parser") 
        #print(script_html)
        html_body.body.append(script_html)
        #print(html_body.body.script)
        return render_template(page, label = predictedLabel, score = int(score * 100), html_body = str(html_body))
    else:
        return "<h2>Error in request!</h2>"