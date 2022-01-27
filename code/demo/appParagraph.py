from flask import Flask,render_template,request
 
app = Flask(__name__)
 
@app.route('/form')
def form():
    return render_template('formParagraph.html')
 
@app.route('/data', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form

        for index, paragraph in form_data.items():
	        output = False 
	        matches = ['store', 'delete']
	        if all(x in paragraph for x in matches):
	        	output = True

        return render_template('output.html',output = output)