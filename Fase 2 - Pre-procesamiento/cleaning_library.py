import pandas as pd
import nltk
import string
import numpy as np

import gensim
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import word2vec , Phrases

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize 
import nltk

from multiprocessing import cpu_count

def limpiar_parrafo(contenido):
  if not(isinstance(contenido, float)):
    parrafo_punt = contenido.translate(str.maketrans('', '', string.punctuation+'‘’¡¿“”')) #Elimina signos de puntuación
    parrafo_clean = parrafo_punt.lower() #Cambia todo a minuscula
  else:
    parrafo_clean = np.NaN
 
  return parrafo_clean

def eliminar_stopwords(cadena, stopwords):
  if not(isinstance(cadena, float)):
    text = ' '.join([word for word in cadena.split() if word not in stopwords])
    text = text.replace('xa0',' ')
  else:
    text = np.NaN
  return text

def limpiar_dataframe(df_art, stopwords):
  size = df_art.shape
  for i in range(size[0]):
    df_art.at[i, 'Contenido'] = eliminar_stopwords(limpiar_parrafo(df_art['Contenido'][i]),stopwords)
    df_art.at[i, 'Categoria'] = eliminar_stopwords(limpiar_parrafo(df_art['Categoria'][i]),stopwords)
    df_art.at[i, 'Autor'] = eliminar_stopwords(limpiar_parrafo(df_art['Autor'][i]),stopwords)
    df_art.at[i, 'Titulo'] = eliminar_stopwords(limpiar_parrafo(df_art['Titulo'][i]),stopwords)
    df_art.at[i, 'Resumen'] = eliminar_stopwords(limpiar_parrafo(df_art['Resumen'][i]),stopwords)
  return df_art

def print_news(array_news):
    for row,f in array_news.iterrows():
        print('------------------------------------------------------------------------------------------------------------')
        print('*Noticia Nº',row)
        print('------------------------------------------------------------------------------------------------------------')
        print('*Titulo:',f[0])
        print('*Autor:',f[1])
        print('*Contenido:',f[3])
        print('*Categoría:',f[4])
        print('*Fecha:',f[5])

def limpiar_csv(file_name,out_name):
  nltk.download('stopwords')
  df_articulos = pd.read_csv(file_name)
  df_articulos.drop(df_articulos.columns[0],axis=1,inplace=True)
  StopWords = stopwords.words("spanish")
  columns = ['palabras']
  df2 = pd.read_csv('spanish_stopwords.csv', encoding = "ISO-8859-1",names=columns)
  stopwords_added = df2['palabras'].values.tolist()
  stopwords_castellano = StopWords + stopwords_added
  df_articulos_clean = limpiar_dataframe(df_articulos, stopwords_castellano)
  df_articulos_clean.to_csv(out_name,encoding='utf_8')
  #print('------------------------------------------------------------------------------------------------------------')
  #print('Noticias obtenidas despues de la limpieza:')
  #print_news(df_articulos_clean)