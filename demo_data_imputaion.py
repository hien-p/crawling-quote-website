
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np 
import os

authors_born_missing = []   

def make_random(data, frac=None):
    data.loc[data.sample(frac=0.2).index,'NamSinh'] = np.nan # random 20 % NaN
    return data


def get_dataFrame():
    data = None
    if os.path.exists('Quote.csv'):
        data = pd.read_csv('Quote.csv')
    else:
        print('Can not found  file quote')
    return data



def list_nan_value(data_value_nan, df):
    born = data_value_nan['NamSinh']
    count = 0
    res = []
    datatemp = pd.DataFrame()
    for row in  born.values:
    #print(row)
        if str(row) == 'nan':
            datatemp =  datatemp.append(df.iloc[[count]], ignore_index = True)
        
        count+=1
    #data_wiki_search = datatemp['tacgia'].values.tolist()
    return datatemp
    
# #print("datatemp: ", datatemp)


import re

def crawling_born(url):
    response=requests.get(url)
    doc_quotes =BeautifulSoup(response.text,'html.parser')

    return doc_quotes



def fill_missing_value(datatemp, data_wiki_search):
    result = []
    wiki_org = 'https://en.wikipedia.org/wiki/' 
    for i in data_wiki_search:  
        name = i.replace(" ","_")
        url = wiki_org+str(name)

        doc_quotes = crawling_born(url)

        # find by regex
        find_bday = '<span class="bday">(\d+-\d+-\d+)</span>'
        result += re.findall(find_bday, str(doc_quotes.findAll('table')))

    return result


# merge 
def merge_to_value_missing(dataframe, result):
    values = list(x for x in dataframe["NamSinh"])
    #print(values)
    count = 0
    datas = pd.DataFrame()
    for i in range(len(values)):
        #print(result[i])
         if str(values[i]) == 'nan' or str(values[i]) == 'NaN':
            print('============================================')
            datas = dataframe.fillna(result[count], limit=1)
            dataframe = datas
            count += 1
         #temp = datas   
    return dataframe


def add_age_to_dataFrame(df):
    data_wiki_search = df['tacgia'].values.tolist()
    find_aged = '\(aged (\d+)\)'
    find_age = '\(age (\d+)\)'
    result = []
    name_l = []
    wiki_org = 'https://en.wikipedia.org/wiki/' 
    dicts  = {}
    #print(len(data_wiki_search))
    for i in tqdm(range(len(data_wiki_search))):
        name = data_wiki_search[i]
        #print(name)
        name = find_name(name)
    
        #print(name)
        url = wiki_org+str(name)
        #print(url)
        doc_quotes = crawling_born(url)
       
        # tage age to data array            
    
        data = re.findall( find_aged, str(doc_quotes.findAll('table')))
        if len(data) == 0:
            #print(doc_quotes)
            data = re.findall( find_age, str(doc_quotes.findAll('table')))
        #print(data)
        result += data
        #name_l.append(name)            
    return result


def find_name(name):
    try:
        if '.' in list(name) or name.endswith('King Jr.'):
            hashlist = list(name)
            for i in range(len(hashlist)):
                #print(hashlist[i+2].isalpha(), hashlist[i+2])
                if str(hashlist[i]) == '.' and str(hashlist[i+1]) != ' ':
                    hashlist.insert(i+1, '_')
                    name = ''.join(hashlist)
                    
                if str(hashlist[i]) == ' ':
                    pass
                else:
                    name = name.replace(" ","_")
                
                    #print('name', name)
            name = name.replace(" ","")
        else:
            name = name.replace(" ","_")
    except:
        print("error")

    if name == "William_Nicholson":
        return 'William_Nicholson_(writer)'
    return name
