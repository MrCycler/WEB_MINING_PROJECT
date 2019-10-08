from bs4 import BeautifulSoup
import base64
import wget
import requests
import unicodecsv as csv
import datetime
import pytz
import dateutil.parser
import pandas as pd
import time

#Obtener el título del artículo
def get_title_rpp(soup_article):
    if soup_article.find("h1",{"itemprop":"headline"}) is not None:
        title = soup_article.find("h1",{"itemprop":"headline"}).text
    else:
        title = "None"
    return title

#Obtener la fecha del artículo
def get_date_rpp(soup_article):
    if soup_article.find("time",{"itemprop":"datePublished"}) is not None:
        fecha = soup_article.find("time",{"itemprop":"datePublished"})
        fecha_return = dateutil.parser.parse(fecha["datetime"])      
    else:
        fecha_return = "None"
    return fecha_return

#Obtener categoría
def get_cat_rpp(soup_article):
    if soup_article.find("span",{"itemprop":"name"}) is not None:
        categoria = soup_article.find("span",{"itemprop":"name"}).text
    else:
        categoria = "None"
    return categoria

#Obtener autor
def get_author_rpp(soup_article):
    if soup_article.find("div",{"id":"author-name"}) is not None:
        autor = soup_article.find("div",{"id":"author-name"}).text
    else:
        autor = "None"
    return autor

#Obtener resumen
def get_summary_rpp(soup_article):
    if soup_article.find("div",{"class":"sumary"}) is not None:
        resumen = soup_article.find("div",{"class":"sumary"})
        nonBreakSpace = u'\xa0'
        resumen_return = resumen.text.replace(nonBreakSpace, ' ')
    else:
        resumen_return = "None"
    return resumen_return

#Obtener contenido
def get_content_rpp(soup_article):
    if soup_article.find("div",{"id":"article-body"}) is not None:
        contenido_p = soup_article.find("div",{"id":"article-body"}).findAll(["p","h3"])
        content_line = []
        for cont_p in contenido_p:
            if cont_p.parent.has_attr('class'):
                try:
                    if cont_p.parent.name == "div" and cont_p.parent.attrs['class'][0] == "col-detail":
                        tt = cont_p.text
                        content_line.append(tt+" ")
                except IndexError:
                    pass
                continue       
        contenido = ''.join(content_line)
        nonBreakSpace = u'\xa0'
        contenido_return = contenido.replace(nonBreakSpace, ' ')        
    else:
        contenido_return = "None"
    return contenido_return

#Función principal
def scrapping_link_rpp(url_article):      
    columns = ["Fecha", "Categoria", "Autor", "Titulo", "Resumen", "Contenido"]
    d = []
    content_article = requests.get(url_article).content
    soup_article = BeautifulSoup(content_article,'lxml')
    print("URL Article===>" + str(url_article))
    date = get_date_rpp(soup_article)     
    category = get_cat_rpp(soup_article)
    author = get_author_rpp(soup_article)
    title = get_title_rpp(soup_article)
    summary = get_summary_rpp(soup_article)
    content = get_content_rpp(soup_article)
    d.append((date, category, author, title, summary, content))    
    df = pd.DataFrame(d,columns=columns)
    return df