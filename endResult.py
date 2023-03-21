import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collabrative.collabrative import collaborative_filtering
from content.content import recommend_products
def result():
    df=pd.read_pickle('1LRecord.pkl').head(5000)
    arr=collaborative_filtering()
    arr=np.array(arr)
    arr=arr.T
    similar_rows = df[np.isin(df.iloc[:, 2], arr)] #collbrative result
    df2=recommend_products()  #content based
    merged_df = pd.merge(similar_rows, df2, on=['productId', 'productId'])
    merged_df.rename(columns = {'imageURLHighRes_y':'imageURLHighRes','title_y':'title','reviewText_y':'reviewText','productId_y':'productId'}, inplace = True)
    merged_df.drop_duplicates()
    return merged_df




'''

rating_x                                                           3.0
date_x                                                     10 16, 2011
userID_x                                                A11GC8EI5HGD5H
productId                                                   B0002Z1JNK
reviewerName_x                                                  Nicole
reviewText_x         I'm normally a 6.5 shoe size, so I ordered a 7...
summary_x                                          Small circumference
title_x                             Pleaser Women's Electra-2000Z Boot
brand_x                                                        Pleaser
feature_x            ['100% Synthetic', 'Synthetic sole', 'Shaft me...
rank_x                             261,979inClothing,Shoesamp;Jewelry(
imageURLHighRes_x    ['https://images-na.ssl-images-amazon.com/imag...
rating_y                                                           5.0
date_y                                                     09 26, 2014
userID_y                                                 A7LETLDCZIFLH
reviewerName_y                                                     avw
reviewText_y         order one size larger there amazing and great ...
summary_y                                                         star
title_y                             Pleaser Women's Electra-2000Z Boot
brand_y                                                        Pleaser
feature_y            ['100% Synthetic', 'Synthetic sole', 'Shaft me...
rank_y                             261,979inClothing,Shoesamp;Jewelry(
imageURLHighRes_y    ['https://images-na.ssl-images-amazon.com/imag...
Name: 0, dtype: object
(venv) (base) Admins-Mac-mini-2:Recommandation project admin$ 



productId                                                 B00007GDFV
title                           Buxton Heiress Pik-Me-Up Framed Case
imageURLHighRes    ['https://images-na.ssl-images-amazon.com/imag...
brand                                                         Buxton

rating                                                           3.0
date                                                     09 22, 2013
userID                                                A1BB77SEBQT8VX
productId                                                 B00007GDFV
reviewerName                                      Darrow H Ankrum II
reviewText         mother - in - law wanted it as a present for h...
summary                                          bought as a present
title                           Buxton Heiress Pik-Me-Up Framed Case
brand                                                         Buxton
feature            ['Leather', 'Imported', 'synthetic lining', 'F...
rank                              43,930inClothing,Shoesamp;Jewelry(
imageURLHighRes    ['https://images-na.ssl-images-amazon.com/imag...
'''