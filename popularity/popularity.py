import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
def Rec_pop():
    df=pd.read_pickle('1LRecord.pkl')
    avg_rating=df.groupby('title').mean(numeric_only=True)['rating'].reset_index()
    df3=df.merge(avg_rating,on='title')
    df3.rename(columns={'rating_x':'rating','rating_y':'avg_rating'},inplace=True) 
    df3['date'] = pd.to_datetime(df3['date'])
    df3 = df3.sort_values('date',ascending=False)
    first_100_rows = df3
    a=first_100_rows[first_100_rows['avg_rating']>=4.5]
    a=a.sort_values('avg_rating',ascending=False)
    a=a.drop_duplicates(subset=["title"],keep='first')
    return a.head(100)

