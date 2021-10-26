# Databricks notebook source
# MAGIC %md
# MAGIC In this model we will use a [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) metric, which we can use for content-based filtering by comparing the beers directly to each other.
# MAGIC 
# MAGIC We'll collect the attributes of all the beers into a [bag-of-words](https://en.wikipedia.org/wiki/Bag-of-words_model) and calculate the similarity between those attributes.

# COMMAND ----------

import pandas as pd
import pickle 

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# COMMAND ----------

# MAGIC %md
# MAGIC First, we modify our data to be two columns, the beer name and the attributes that describe the beer in string format. 

# COMMAND ----------

#Read in data from pickle

df = pd.read_pickle("beer_data.pickle")

df = df.drop_duplicates(subset=['beer_name'])

cols = ['brewery_name', 'beer_style']
df['key_words'] = df[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

dfbag = df[['beer_name', 'key_words']].copy()

dfbag["key_words"] = dfbag["key_words"].str.lower()
dfbag["key_words"] = dfbag["key_words"].replace('/', '')

dfbag = dfbag.reset_index(drop=True)

# COMMAND ----------

# MAGIC %md
# MAGIC We will create a matrix using the sk-learn's CountVectorizer. This module allows use to use textual data for predictive modeling. For this to happen, the text needs to be parsed to remove certain words, also known as tokenization. Those words then need to be encoded as integers for use as inputs in ML algorithms. This entire process is cqalled feature extraction.

# COMMAND ----------

count = CountVectorizer()
count_matrix = count.fit_transform(dfbag['key_words'])
count_matrix.shape

# COMMAND ----------

#Generate the cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# COMMAND ----------

# Create a Series for the beers so they are associated to an ordered numerical list
indices = pd.Series(dfbag['beer_name'])
indices[indices == 'Coors']

# COMMAND ----------

#Takes in the name of the beer and returns the top n nunber of recommended beers

def beer_recs(string, n, cosine_sim = cosine_sim):
    
    recommended_beers = []
    
    #Get the index of the beer that matches the beer name
    idx = indices[indices == string].index[0]
    
    #Creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    #Get the indices of the n most similar unique beers
    n = n + 1
    top_n_indexes = list(score_series.iloc[1:n].index)
    
    #Populating the list with the names of the n most similar beers
    for i in top_n_indexes:
        recommended_beers.append(dfbag.iloc[i]['beer_name'])
        
    return recommended_beers

# COMMAND ----------

beer_recs('Cauldron DIPA', 5)

# COMMAND ----------

beer_recs('Sausa Weizen', 5)

# COMMAND ----------

beer_recs('Coors', 5)

# COMMAND ----------


