#Load data
import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\joshu\Documents\GitHub\TDI-Capstone\Data Source\BostonListings\listings.csv")

#Remove rows that are not short term rentals
#min_nights > 3 is not considered a short term rental
df = df[df['minimum_nights'] < 4]

#Calculate total price = price + cleaning fee/min_nights
totalpricelist = []
for i, row in df.iterrows():
    price = float(row['price'].replace(',', '')[1:])
    if (isinstance(row['cleaning_fee'], str)):
        cleaning_fee = float(row['cleaning_fee'].replace(',', '')[1:])
    else:
        cleaning_fee = 0.0
    total_price = price + (cleaning_fee/row['minimum_nights'])
    totalpricelist.append(total_price)

    #also clean up zipcode data
    if (isinstance(row['zipcode'], str) and (len(row['zipcode'])>5)):
        df.at[i, 'zipcode'] = row['zipcode'][0:5]

totalpricelist = np.array(totalpricelist)

#Data cleaning
#Select Features
#8 features for Boston and SF Models
col_names = ['zipcode', 'property_type', 'room_type', 'accommodates', 
             'bathrooms', 'bedrooms', 'beds', 'bed_type']

#Remove unnecessary columns, remove rows with incomplete information
df = df[col_names]
df = df.fillna(0)
df = df[df.zipcode != 0]


#Create Machine Learning Pipeline
from sklearn import base
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import OneHotEncoder

#Column Select Transformer Helper Function
class ColumnSelectTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, col_names):
        self.col_names = col_names
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.col_names]

#Transformer for Categorial Features: zipcode, property_type, room_type, bed_type
cat_features = ['zipcode', 'property_type', 'room_type', 'bed_type']
categorial_transformer = Pipeline([
        ('cst', ColumnSelectTransformer(cat_features)),
        ('one_hot', OneHotEncoder(handle_unknown='ignore'))
    ])

#Transformer for Numerical Features: accommodates, bathrooms, bedrooms, beds
num_features = ['accommodates', 'bathrooms', 'bedrooms', 'beds']
numerical_transformer = ColumnSelectTransformer(num_features)

testcatdata = categorial_transformer.fit_transform(df)
testnumdata = numerical_transformer.fit_transform(df)

#Full Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
lin_reg = LinearRegression()
rid_reg = Ridge()
las_reg = Lasso()




