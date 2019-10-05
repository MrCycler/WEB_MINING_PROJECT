import pandas as pd

def print_hola(name):
	print('hola '+ name)
	
def limpiar_csv(file_name):
	df_articulos = pd.read_csv(file_name)	
	df_articulos
	print(df_articulos)