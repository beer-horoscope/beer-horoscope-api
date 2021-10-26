# Databricks notebook source
# Databricks notebook source

import pickle
import pandas as pd

# COMMAND ----------

#Read in data from csv
df = pd.read_csv('beer_reviews.csv', low_memory=False)
df = df.head(500000)

# COMMAND ----------

pickle_out = open('beer_data.pickle','wb')
pickle.dump(df, pickle_out)
pickle_out.close()  

# COMMAND ----------


