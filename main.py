# Install and Import important libraries
from cgitb import text
from urllib import response
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
#from convert_born_to_date import convert_to_date
from data_imputaion import *
from datetime import datetime


def convert_to_date(text):
    def clean(text):
        text = text.replace(",","")
        return text.replace(" ","/")

    months_names = ['January', 'February', 'March', 
    'April', 'May', 'June', 'July', 
    'August', 'September', 'October',
    'November', 'December']

    def make_dictionary(months_names):
        number_months = {} 
        for i in range(0,12):   
            #print(months_names[i].upper())
            number_months[months_names[i].upper()]= str(i+1)

        return number_months
    
    text = clean(text=text)
    word_month = make_dictionary(months_names)
    res = '/'.join([word_month.get(i, i) for i in text.upper().split('/')])

    datetime_object = datetime.strptime(str(res),'%m/%d/%Y').date()

    return datetime_object


def tacgiaLink(authors,authors_link,borns,quotes) -> list:
    """ return (ten tac gia, link, ngaythangnamsinh, quotes )"""
    result = list()
    for i in range(len(quotes)):
        result.append({'Tacgia': authors[i],
            'Link': authors_link[i],
             'NamSinh': borns[i],
             'quote': quotes[i]})

    return result
    #return [{'tacgia': authors[i], 'Link': authors_link[i], 'NamSinh': borns[i], 'Quote':quotes[i]}
     #for i in range(len(quotes))] # using the list comprehension



def merge(list1, list2):
      
    merged_list = [(p1, p2) for idx1, p1 in enumerate(list1) 
    for idx2, p2 in enumerate(list2) if idx1 == idx2]
    return merged_list


def crawling_born(url):
    response=requests.get(url)
    doc_quotes =BeautifulSoup(response.text,'html.parser')
    #print(response.text)
    text = doc_quotes.find('div', class_='author-details').find('span',class_='author-born-date').text
    return text


def number_quotes(quote):
    length_quotes = 0
    authors = []
    authors_link = []
    bornofauthor = []
    quotes = []
    page = 1
    result = []
    bornofauthor = list()
    i = 0

    # length web 
    while int(i) < int(quote):
        
        url = 'http://quotes.toscrape.com/page/'+str(page)+'/' 
        #print(url)
        
        response=requests.get(url)  
        
        
        doc_quotes =BeautifulSoup(response.text,'html.parser')
        #print('quote', len(doc_quotes))


        if int(quote) <= 10 or (int(quote)-i < 10):
            temp = doc_quotes.find_all('div',class_='quote')[:int(quote)-i]
            result += temp
            i += int(quote)-i
        else:
            temp = doc_quotes.find_all('div',class_='quote')
            result += temp
            i += len(result)

        print(result)
    
        quotes += [tag.find('span',class_='text').text for tag in result]


        # find author 
        author = [tag.find('small',class_='author').text for tag in result]

        authors += [tag.find('span',class_=None).\
        find('small',class_='author').text for tag in result]
        
        url = 'http://quotes.toscrape.com/'
        authors_link += [str(url+tag.find('span', class_=None).\
        find('a')['href']) for tag in result]
        
        result = [] 
        page += 1
        
    print("--------------------------------------")
   
    for i in tqdm(range(len(authors_link))):
        bornofauthor.append(convert_to_date(crawling_born(authors_link[i])))
       
    print("--------------------------------------")
    return authors, authors_link, bornofauthor, quotes
   
    

    

if __name__ == "__main__":
    response = None
    file = open("kq.txt", "w")  
    for i in range(10):
        print(i+1)
        url = 'http://quotes.toscrape.com/page/'+str(i+1)+'/'
        response =requests.get(url) 
        file.write(str(response.content))  
        print(response.content)
    file.close() 

    # quote = input("The number of quotes you want:")
    # #number_quotes(quote)
    # authors, authors_link, bornofauthor, quotes = number_quotes(quote)
    # items = tacgiaLink(authors, authors_link, bornofauthor, quotes)

    # path = "Quote.csv"
    # print(items)
    # df=pd.DataFrame(items)
    # df.to_csv(w,index=None)

    # some ways
    # read file Quote.csv
    #df = get_dataFrame()
    #print(df)

    # random value df  
    #data_value_nan = make_random(df)
    #print(data_value_nan)

    # list value nan 
    #data_values = list_nan_value(data_value_nan, df)
    #print(data_values)

    #data_wiki_search = data_values['tacgia'].values.tolist()
    #print(data_wiki_search)

    #list_bday_authors = fill_missing_value(data_values, data_wiki_search)
    #print(list_bday_authors)

    #df = merge_to_value_missing(data_value_nan, list_bday_authors)
    #print(df)

    # add more column name 'age' to df
    res = add_age_to_dataFrame(df)
    df['Tuoi'] = res
    print(df)
    path = "Quote.csv"
    df.to_csv(path,index=None)

    