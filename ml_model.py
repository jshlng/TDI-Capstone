#Load data
import pandas as pd

df = pd.read_csv(r"C:\Users\joshu\Documents\GitHub\TDI-Capstone\Data Source\BostonListings\listings.csv")

#Set Up Pipeline
from sklearn.pipeline import Pipeline
import sklearn.linear_model

#Select Features
#8 features for Boston and SF Models
col_names = ['zipcode', 'property_type', 'room_type', 'accommodates', 
             'bathrooms', 'bedrooms', 'beds', 'bed_type']

#Remove rows that are not short term rentals
#min_nights > 3 is not considered a short term rental

    
#Calculate total price = price + cleaning fee/min_nights

#Create Pipeline
#lr is the linear regerssor
lr = LinearRegression() 
Pipeline([
        ('onehot_encoder', OneHotEncoder(handle_unknown='ignore')),
        ('regressor', lr)
    ])
