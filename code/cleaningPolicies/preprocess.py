#you will need to run pip install beautifulsoup4, pip install nltk and pip install markdown for the .md files. do this in a venv!

import nltk, markdown, os
from bs4 import BeautifulSoup, SoupStrainer
from nltk import word_tokenize
from pathlib import Path
nltk.download('punkt')



read_path = 'five_sample'
write_path = 'five_chunked'

for filename in os.listdir(read_path):
    working_file = os.path.join(read_path,filename)

    with open(working_file, 'r') as f:
        writing_file = os.path.join(write_path,str(Path(filename).stem + '.txt'))
        w_file = open(writing_file, "w")
        text = f.read()
        html = markdown.markdown(text)
        buffer = []
        index = 0
        soup = BeautifulSoup(html, 'html.parser')

        for child in soup.contents:
            if child.name != 'blockquote':
                if child.name in ['h1','h2','h3']:
                    if buffer:
                        w_file.write('EXCERPT: ' + str(index) + '\n')
                        w_file.writelines(buffer)
                        w_file.write('\n ********************************* \n')
                    buffer = []
                    index += 1
                    buffer.append(child.get_text())
                else:
                    temp_text = child.get_text()
                    buffer.append(temp_text)
                    if len(temp_text) > 700:
                        w_file.write('EXCERPT: ' + str(index) + '\n')
                        w_file.writelines(buffer)
                        w_file.write('\n ********************************* \n')
                        buffer = []
                        index += 1
        w_file.close()
