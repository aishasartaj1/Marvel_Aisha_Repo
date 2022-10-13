#Impoting Files

import requests
import json
import hashlib
import time
import datetime
import pandas as pd
from pandas import json_normalize
from pprint import pprint as pp
import string
from keys import PUBLIC_KEY, PRIVATE_KEY
import argparse

#Creating the parser
parser = argparse.ArgumentParser(description='Please provide the Public key, priavte key and initial letter of marvel character')
parser.add_argument('--public_key', type=str,required = True,
                    help='provide the Public key')
parser.add_argument('--private', type=str,required = True,
                    help='provide the Private key')
#Parsing the arguments
ts = 1
args = parser.parse_args()




#Getting the URL, defining the public and private key, timestamp and limit

request_url = "http://gateway.marvel.com/v1/public/characters"
public_key = PUBLIC_KEY
private_key = PRIVATE_KEY
timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
limit = 100

#Defining the function for hash

def hash_params():
    """ Marvel API requires server side API calls to include
    md5 hash of timestamp + public key + private key """

    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{private_key}{public_key}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()

    return hashed_params

#Activity 2

#Making API calls

character_start = list(string.ascii_lowercase + string.digits)
character_start.remove('0')

final_data = []
for i in character_start:
    nameStartsWith = i
    params = {'ts': timestamp, 'apikey': public_key, 'hash': hash_params(), 'nameStartsWith': nameStartsWith, 'limit': limit}
    response = requests.get(request_url,params=params)
    data = response.json()
    df = pd.json_normalize(data, record_path=['data', 'results'])
    final_data.append(df)

df = pd.concat(final_data)

#Dataframe of the API calls

characters_sum=df.loc[:,['id','name','comics.available','series.available','stories.available','events.available']]
characters_sum

characters_sum.rename(columns = {'id': 'Id', 'name':'Name', 'comics.available':'Comics', 'series.available': 'Series', 
                                'stories.available': 'Stories', 'events.available': 'Events'}, inplace = True)

#Activity 3

timestamp1 = datetime.datetime.now()
hash_md5 = hashlib.md5()
hash_md5.update(f'{timestamp1}{private_key}{public_key}'.encode('utf-8'))
hashed_params = hash_md5.hexdigest()

# raising an exception
def func_except(nameStartsWith, apikey=None, hash=None):
    global df1
    try:   
        request_url = "http://gateway.marvel.com/v1/public/characters"
        params = {'ts': timestamp1, 'apikey': apikey, 'hash': hash, 'nameStartsWith': nameStartsWith, 'limit': 100}
        response = requests.get(request_url,params=params)
        data = response.json()
        df1 = pd.json_normalize(data, record_path=['data', 'results'])
        df_required = df1[['id','name', 'comics.available', 'stories.available', 'events.available', 'series.available']]

    except:
        print("Missing apikey or hash")

    else:
        print("Yay the marvel chracters you asked for")
        return df_required

    finally:
        print("If error, provide api key or hash value")


#Dataframe with all the arguments, hence gives no exception
df_act3 = func_except(nameStartsWith='c', apikey= public_key, hash=hashed_params) 


#Dataframe with API key missing, gives exception
df_act31 = func_except(nameStartsWith='a', hash=hashed_params) 

#Activity 4
def filter_char(dataframe, column, condition):
    if condition[0] == '>':
        filter_df = dataframe[dataframe[column]>filter[1]]
    if condition[0] == '<':
        filter_df = dataframe[dataframe[column]<filter[1]]
    if condition[0] == '=':
        filter_df = dataframe[dataframe[column]==filter[1]]
    return filter_df

filter = []
filter = ['>', 100]

df_act4 = filter_char(df_act3, "comics.available", condition = filter)
