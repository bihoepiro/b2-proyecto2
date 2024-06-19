# -*- coding: utf-8 -*-
"""Spimi-prepro.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MY08p1RkM_5fJnp8og9KNjg8wn-3pL4M
"""

import pandas as pd
import os
import nltk
nltk.download('punkt')
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('english')

def determinar_bloque(i, limite):
  for j in range(limite + 1):
    # seleccionar bloque
    if i <= j*limite and i > (j-1)*limite:
      return j

csv_file = '/data.csv'
df = pd.read_csv(csv_file)
#DICCIONARIO DOCS
diccionario_docs = {}



def obtener_tf(index, word):
  frecuencia = 0
  words = diccionario_docs[index]
  for w in words:
    if w == word:
      frecuencia += 1
  return frecuencia


# Crear una carpeta para almacenar los archivos de texto
output_folder = '/content/text_files'
os.makedirs(output_folder, exist_ok=True)

stoplist = ["a", "an", "and", "are", "as", "at", "be", "but", "by",
            "for", "if", "in", "into", "is", "it", "no", "not", "of",
            "on", "or", "such", "that", "the", "their", "then", "there",
            "these", "they", "this", "to", "was", "will", "with", "...", "/", "-", "&", ")", "(", ".", "..", "?", "'s"]
diccionario_palabras = {}
for index, row in df.iterrows():
    # Concatenar todos los atributos en una sola cadena
    row_text = ' '.join(row.astype(str).tolist())
    text_file_path = os.path.join(output_folder, f'fila_{index + 1}.txt')

    with open(text_file_path, 'w') as text_file:
        text_file.write(row_text)
   #TOKENIZAR (DIVIDIR EL TEXTO EN PALABRAS)
    with open( f'/content/text_files/fila_{index + 1}.txt', encoding = "utf-8") as textfile:
       words = textfile.read()
    words = nltk.word_tokenize(words.lower())
    words_ = []
    for word in words:
       if  word not in stoplist:
        words_.append(word)
        #para garantizar el diccionario correcto
        #diccionario_palabras.setdefault(word, {})[index+1] = obtener_tf(index +1, word)
    words_ = [stemmer.stem(words_[i]) for i in range(len(words_))]
    #como doc id le asignamos su index + 1
    diccionario_docs[index+1] = words_
    for word in words_:
      diccionario_palabras.setdefault(word, {})[index+1] = obtener_tf(index +1, word)



print(f'Archivos de texto creados en la carpeta: {output_folder}')

print(diccionario_palabras)

print(diccionario_docs)

cant_bloques = 3
cant_docs = 30
bloques = {}
limite = int(cant_docs/cant_bloques)


for i in range(cant_bloques):
  bloques[i] = {}

bloque_temp = 1
for i in range(cant_docs):
  #obtener datos necesarios es decir TF de cada word en cada doc, bueno en los necesarios por bloque
  bloque_temp = determinar_bloque(i+1, limite)
  for word in diccionario_palabras:
    docs_presentes = diccionario_palabras[word]
    docs_limite = []
    for index in docs_presentes:
      if determinar_bloque(index, limite) == bloque_temp:
        docs_limite.append(index)
    if len(docs_limite) > 0: #solo si esas palabras estan presentes en los docs pertenecientes al bloque
      bloques.setdefault(bloque_temp, {})[word] = docs_limite

"""**Notar que en el bloque 1, la palabra boy aparece en el 2,4,6**"""

import pprint
pprint.pprint(bloques[1])

"""**Notar que boy aparece en el bloque 2 con página 14**"""

import pprint
pprint.pprint(bloques[2])

"""**Okay ahora merge Blocks para no tener los mismos terminos (words) en todos los bloques que antes eran locales.**"""

merged_blocks = {}
for i in range(cant_bloques):
  for word, docs in bloques[i].items():
    if word in merged_blocks:
      merged_blocks[word].extend(docs)
    else:
      merged_blocks[word] = docs

pages = {}
page_num = 0
words_in_page = 0
total_words = len(merged_blocks)
limite = int(total_words/ cant_bloques)
sorted_words = sorted(merged_blocks.keys())

total_words = len(sorted_words)
limite = int(total_words / cant_bloques)

pages = {}
page_num = 0
words_in_page = 0

for word in sorted_words:
    if page_num not in pages:
        pages[page_num] = {} #su page se inicia

    pages[page_num][word] = merged_blocks[word] # añado el word a la page
    words_in_page += 1 #voy aumentando el numero de palabras

    if words_in_page >= limite: #compruebo si ya pase el limite
        page_num += 1
        words_in_page = 0

pprint.pprint(pages)



"""**Búsqueda por similitud de coseno TOP K**

"""

#Forma de la query, palabras naturales, tipo oraciones
def simcosK(query, K ):
  #preprocesamiento de la query.
  query = nltk.word_tokenize(query.lower())
  final_query = []
  for word in query:
    if word not in stoplist:
      final_query.append(word)
  final_query = [stemmer.stem(final_query[i]) for i in range(len(final_query))]

  #similitud por coseno






  #probamos la correcta reduccion de la query
  return final_query

simcosK("wondering about the lovers and the amazing things of life")
