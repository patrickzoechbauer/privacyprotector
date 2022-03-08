from flask import Flask,render_template,request
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np

nltk.download('punkt') # if necessary...

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def calc_bestfit(example, labels):
    bestfit = dict() 
    bestfit['similarity'] = 0
    for file in labels: 
        for para in range(len(labels[file])):
            similarity = cosine_sim(example, labels[file].loc[para,'PARAGRAPH'])        
            if bestfit['similarity'] < similarity:
                #new best fit
                bestfit['similarity'] = similarity
                bestfit['file'] = file
                bestfit['label'] = labels[file].loc[para, 'LABEL']
                bestfit['PARAGRAPH'] = labels[file].loc[para, 'PARAGRAPH']
                bestfit['AMBIGUITY'] = labels[file].loc[para, 'AMBIGUITY']
    return bestfit

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

#Load the row paragraphs
with open('DB.pickle', 'rb') as handle:
    labels = pickle.load(handle)   

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
        output_flag = False

        for index, paragraph in form_data.items():

            analysis = calc_bestfit(paragraph, labels)
            print(analysis)

            if analysis['label'] == 1:
                output_flag = True

        return render_template('output.html',output = output_flag,
                                amb = analysis['AMBIGUITY'],
                                conf = np.round(analysis['similarity'],2))


