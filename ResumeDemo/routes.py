from flask import Flask, request, url_for, render_template
from app import app

@app.route('/', methods = ['GET', 'POST'])
def hello():
    """Renders a sample page."""
    if request.method == 'GET':
        return render_template('RequestPage.html')
    elif request.method == 'POST':

        return render_template('ResponsePage.html')
    else:
        return "<h2>Error in request!</h2>"