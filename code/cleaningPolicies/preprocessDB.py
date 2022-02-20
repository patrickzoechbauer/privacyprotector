#you will need to run pip install beautifulsoup4, pip install nltk and pip install markdown for the .md files. do this in a venv!

import nltk, markdown, os
from bs4 import BeautifulSoup, SoupStrainer
from nltk import word_tokenize
from pathlib import Path
import pickle
nltk.download('punkt')


#this will be folder name of files to convert
read_path = 'sample'
#this will be where the converted .txt files are kept
write_path = 'chunked'

output_dict = {}

for filename in os.listdir(read_path):
    working_file = os.path.join(read_path,filename)

    with open(working_file, 'r') as f:
        print(filename)
        if('.md' in filename):
            output_dict[filename] = []
            writing_file = os.path.join(write_path,str(Path(filename).stem + '.txt'))
            w_file = open(writing_file, "w")
            text = f.read()
            headeronly = True
            buffer = []
            index = 0
            html = markdown.markdown(text)
            #print(html)
            soup = BeautifulSoup(html, 'html.parser')

            for child in soup.contents:
                if child.name != 'blockquote':
                    if child.name in ['h1','h2','h3','h4','h5']:
                        if not(headeronly):
                            w_file.write('EXCERPT: ' + str(index) + '\n')
                            index += 1
                            #print(buffer, '\n', '\n')
                            w_file.writelines(buffer)
                            w_file.write('\n ********************************* \n')
                            output_dict[filename].append((index, buffer))
                            buffer, headeronly = [], True
                        buffer.append(child.get_text())
                    elif (child.get_text() == '\n'):
                        buffer.append(child.get_text())
                    else:
                        headeronly = False
                        temp_text = child.get_text()
                        buffer.append(temp_text)
                        if len(temp_text) > 500:
                            w_file.write('EXCERPT: ' + str(index) + '\n')
                            index += 1
                            #print(buffer, '\n', '\n')
                            w_file.writelines(buffer)
                            w_file.write('\n ********************************* \n')
                            output_dict[filename].append((index, buffer))
                            buffer, headeronly = [], True
            w_file.close()

with open('labeledData.pickle', 'wb') as handle:
    pickle.dump(output_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
