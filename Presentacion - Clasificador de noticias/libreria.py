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

def scrap_news(file_name):
	df_articulos = pd.read_csv(file_name)
	print('------------------------------------------------------------------------------------------------------------')
	print('Noticias obtenidas despues del scrapping:')
	print_news(df_articulos)
		
def getFV(document, model1): #promedio del vector caracteristico
	words=document.split()
	s=np.zeros(100)
	k=1
	for w in words:
		if w in model1.wv.vocab:
			s=s+ model1[w]
			k=k+1
	return s/k

def obtener_vector_doc(file_name,model_name):
	model1 = gensim.models.keyedvectors.KeyedVectors.load_word2vec_format(model_name, binary=True)
	df_articulos = pd.read_csv(file_name)
	df_2 = df_articulos.dropna()
	df_2['Vector'] = df_2['Contenido'].apply(lambda x: getFV(x,model1)) 
	return df_2['Vector']
	
	
	
  
