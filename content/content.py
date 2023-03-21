import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data=pd.read_pickle('summary.pkl').head(1000)

'''
co=0
def preprocess_text(text):
    global co
    co=co+1
    if co%10==0:
        print("processing",co)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    return ' '.join(tokens)

data['summary'] = data['summary'].apply(preprocess_text)

data.to_pickle('summary.pkl')
'''


tfidf_vectorizer = TfidfVectorizer()
tfidf_features = tfidf_vectorizer.fit_transform(data['summary'])

cosine_sim = cosine_similarity(tfidf_features)

def recommend_products(brand='Buxton', num_recommendations=10):
    print("start")
    indices = [i for i, row in data.iterrows() if row['brand'] == brand]
    avg_cosine_sim = cosine_sim[indices, :].mean(axis=0)
    print("highf a way")
    top_indices = avg_cosine_sim.argsort()[::-1][:num_recommendations]
    print("almost complet")
    return data.iloc[top_indices]
