from flask import Flask,render_template,request
 
import model

app = Flask(__name__)
 
@app.route('/form')
def form():
    return render_template('formFile.html')
 
@app.route('/data', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        filename = form_data["Input"]
        output = model.run(filename)
        return render_template('outputFile.html',output = output)