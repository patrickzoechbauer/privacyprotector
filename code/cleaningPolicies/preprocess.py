#you will need to run pip install beautifulsoup4, pip install nltk and pip install markdown for the .md files. do this in a venv!

import nltk, markdown
from bs4 import BeautifulSoup, SoupStrainer
from nltk import word_tokenize
nltk.download('punkt')

with open('practice.md', 'r') as f:
    text = f.read()
    html = markdown.markdown(text)



buffer = []

soup = BeautifulSoup(html, 'html.parser')

for child in soup.contents:
    if child.name != 'blockquote':
        if child.name in ['h1','h2','h3']:
            buffer.append(child.get_text())
        else:
            temp_text = child.get_text()
            buffer.append(temp_text)
            if len(temp_text) > 500:
                print(buffer)
                print('*********************************')
                buffer = []



#raw = BeautifulSoup(html, 'html.parser').get_text()
#tokens = word_tokenize(raw)
#print(tokens)
