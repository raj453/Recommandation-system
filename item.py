from flask import Flask, request, render_template, redirect, url_for, session
from popularity.popularity import Rec_pop
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import pandas as pd
from sqlalchemy.exc import IntegrityError
import numpy as np
from endResult import result
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)

'''
engine = create_engine('sqlite:///items.db', echo=True)
Session_db = sessionmaker(bind=engine)
Base = declarative_base()


class item(Base):
    __tablename__ = 'item'
    productId = Column(String, primary_key=True)
    title = Column(String(100))
    brand = Column(String(100))
    rating = Column(String(700))
    userID = Column(String(700))
    imageURLHighRes = Column(String(700))

Base.metadata.create_all(engine)
session_main = Session_db()
'''
df =pd.read_pickle('1LRecord.pkl')
print(df.iloc[0])
'''
co=0
for index, row in df.iterrows():
            people = []
            co=co+1
            print("Processing------",co)
            data=row['imageURLHighRes']
            urls = data.split(',')
            first_url = urls[0]
            first_url=first_url.replace("'", "")
            if first_url.endswith("]"):
                first_url = first_url.rstrip("]")
            if first_url.endswith("'"):
                first_url = first_url.rstrip("'")
            if first_url.startswith("'"):
                first_url = first_url.lstrip("'") 
            if first_url.startswith("["):
                first_url = first_url.lstrip("[") 
            
            print(type(row['productId']), type(str(row['title'])), type(str(row['brand'])), type(str(row['rating'])), type(str(row['userID'])), type(str(first_url)))

            new_item = item(productId=str(row['productId']),
                             title=str(row['title']), 
                             brand=str(row['brand']), 
                             rating=str(row['rating']), 
                             userID=str(row['userID']), 
                             imageURLHighRes=str(first_url))
            
            try:
                session_main.add(new_item)
                session_main.commit()
            except IntegrityError:
                session_main.rollback()
            
app.run(port=8080)
'''
