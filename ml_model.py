#Load data
import pandas as pd
import numpy as np

rawdf = pd.read_csv(r"C:\Users\joshu\Documents\GitHub\TDI-Capstone\Data Source\SFListings\listings.csv")

#Remove rows that are not short term rentals
#min_nights > 3 is not considered a short term rental
rawdf = rawdf[rawdf['minimum_nights'] < 4]

#Remove rows with incomplete or incorrect zipcode info
rawdf = rawdf.fillna(0)
rawdf = rawdf[rawdf.zipcode != 0]

#Calculate Total Price for Each Listing
#price + cleaning fee/min_nights + (accommodates - guests_included)*price per extra person
totalpricelist = []
for i, row in rawdf.iterrows():
    price = float(row['price'].replace(',', '')[1:])
    if (isinstance(row['cleaning_fee'], str)):
        cleaning_fee = float(row['cleaning_fee'].replace(',', '')[1:])
    else:
        cleaning_fee = 0.0
    if (isinstance(row['extra_people'], str) and (row['accommodates'] > row['guests_included'])):
        extra_ppl_fee = float(row['extra_people'].replace(',', '')[1:])*(row['accommodates'] - row['guests_included'])
    else:
        extra_ppl_fee = 0.0
    total_price = price + (cleaning_fee/row['minimum_nights']) + extra_ppl_fee
    totalpricelist.append(total_price)

    #also clean up zipcode data
    rawdf.at[i, 'zipcode'] = str(row['zipcode'])
    if (len(str(row['zipcode']))>5):
        rawdf.at[i, 'zipcode'] = str(row['zipcode'])[0:5]
    if (len(str(row['zipcode']))==4):
        rawdf.at[i, 'zipcode'] = '0' + str(row['zipcode'])
        
#Select Features
#8 features for Boston and SF Models
col_names = ['zipcode', 'property_type', 'room_type', 'accommodates', 
             'bathrooms', 'bedrooms', 'beds', 'bed_type', 'amenities']
df = rawdf[col_names]
df.insert(len(df.columns), 'total_price', totalpricelist)

#Remove rows that have unique features (not shared with at least 15 other rows)
for col in ['zipcode', 'property_type', 'room_type', 'bed_type']:
    for label, value in df[col].value_counts().iteritems():
        if (value < 15):
            df = df[df[col] != label]        

#Remove Rows that don't have the correct type (mixed type in some of columns)
#df[df.apply(lambda x: isinstance(x['zipcode'], str), axis=1)]

#Select Amenities
amenities_dict = {}
for i, row in df.iterrows():
    if (isinstance(row['amenities'], str)):
        amn_list = row['amenities'].replace('{','').replace('}','').replace('"','').split(',')
        for amn in amn_list:
            if (amn in amenities_dict):
                amenities_dict[amn] = amenities_dict[amn] + 1
            else:
                amenities_dict[amn] = 1

amn_counts = sorted(amenities_dict.items(), key=lambda kv: kv[1])

#Dict of Amenities selected by hand from the top 50
#Removed a bunch of the most common ones because >95% of listings had them
#Removed 'Internet' because 'Wifi' was the most common term used

#Dict with 40 common Amenities
amn_dict = {
        'Air conditioning': 0,
        'Hair dryer': 1,
        'Iron': 2,
        'TV': 3,
        'Laptop friendly workspace': 4,
        'Washer': 5,
        'Dryer': 6,
        'Hot water': 7,
        'Fire extinguisher': 8,
        'Refrigerator': 9,
        'Self check-in': 10,
        'Microwave': 11,
        'Bed linens': 12,
        'Stove': 13,
        'Dishes and silverware': 14,
        'Coffee maker': 15,
        'Oven': 16,
        'Cable TV': 17,
        'Cooking basics': 18,
        'Long term stays allowed': 19,
        'Family/kid friendly': 20,
        'First aid kit': 21,
        'Dishwasher': 22,
        'Lock on bedroom door': 23,
        'Free street parking': 24,
        'Elevator': 25,
        'Extra pillows and blankets': 26,
        'Luggage dropoff allowed': 27,
        'Lockbox': 28,
        'Keypad': 29,
        'Private entrance': 30,
        'Bathtub': 31,
        'Free parking on premises': 32,
        'No stairs or steps to enter': 33,
        'Private living room': 34,
        'Pets allowed': 35,
        'Gym': 36,
        'Patio or balcony': 37,
        'Paid parking off premises': 38,
        '24-hour check-in': 39}

#Dict with 31 common Amenities
amn_dict = {
        'Washer': 0,
        'Dryer': 1,
        'Refrigerator': 2,
        'Self check-in': 3,
        'Microwave': 4,
        'Stove': 5,
        'Dishes and silverware': 6,
        'Coffee maker': 7,
        'Oven': 8,
        'Cable TV': 9,
        'Cooking basics': 10,
        'Family/kid friendly': 11,
        'First aid kit': 12,
        'Dishwasher': 13,
        'Lock on bedroom door': 14,
        'Free street parking': 15,
        'Elevator': 16,
        'Extra pillows and blankets': 17,
        'Luggage dropoff allowed': 18,
        'Lockbox': 19,
        'Keypad': 20,
        'Private entrance': 21,
        'Bathtub': 22,
        'Free parking on premises': 23,
        'No stairs or steps to enter': 24,
        'Private living room': 25,
        'Pets allowed': 26,
        'Gym': 27,
        'Patio or balcony': 28,
        'Paid parking off premises': 29,
        '24-hour check-in': 30}

#Dict with 21 common Amenities
amn_dict = {
        'Self check-in': 0,
        'Microwave': 1,
        'Stove': 2,
        'Dishes and silverware': 3,
        'Coffee maker': 4,
        'Oven': 5,
        'Cable TV': 6,
        'Cooking basics': 7,
        'Family/kid friendly': 8,
        'Dishwasher': 9,
        'Free street parking': 10,
        'Elevator': 11,
        'Luggage dropoff allowed': 12,
        'Private entrance': 13,
        'Free parking on premises': 14,
        'No stairs or steps to enter': 15,
        'Private living room': 16,
        'Pets allowed': 17,
        'Gym': 18,
        'Patio or balcony': 19,
        '24-hour check-in': 20}

#Create Machine Learning Pipeline
from sklearn import base
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import OneHotEncoder

#Column Select Transformer Helper Function
class ColumnSelectTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, col_names):
        self.col_names = col_names
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.col_names]

#Transformer for Numerical Features: accommodates, bathrooms, bedrooms, beds
num_features = ['accommodates', 'bathrooms', 'bedrooms', 'beds']
numerical_transformer = ColumnSelectTransformer(num_features)

#Transformer for Categorial Features: zipcode, property_type, room_type, bed_type
cat_features = ['zipcode', 'property_type', 'room_type', 'bed_type']
categorial_transformer = Pipeline([
        ('cst', ColumnSelectTransformer(cat_features)),
        ('one_hot', OneHotEncoder(handle_unknown='ignore'))
    ])
    

#Encoder for Amenities, limited to 21 of the top Amenities
class AmenitiesEncoder(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, amn_dict):
        self.amn_dict = amn_dict
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        amn_matrix = np.zeros((X.shape[0],len(self.amn_dict)))
        df = X.reset_index()
        for i, row in df.iterrows():
            if (isinstance(row['amenities'], str)):
                amn_list = row['amenities'].replace('{','').replace('}','').replace('"','').split(',')
                #print(i-1)
                for amn in amn_list:
                    if (amn in self.amn_dict):
                        amn_matrix[i,self.amn_dict[amn]] = 1
        return amn_matrix

#Transformer for amenities
amn_transformer = Pipeline([
        ('cst', ColumnSelectTransformer(['amenities'])),
        ('amn_encoder', AmenitiesEncoder(amn_dict))
    ])
    
#Feature Union to combine Categorial and Numerical Features 
union = FeatureUnion([
        ('cat_tfm', numerical_transformer),
        ('num_tfm', categorial_transformer),
        ('amn_tfm', amn_transformer)
    ])
    
#Test Transformers to Make Sure They Work    
#testnumdata = numerical_transformer.fit_transform(df)
#testcatdata = categorial_transformer.fit_transform(df)
#testamndata = amn_transformer.fit_transform(df)
#testuniondata = union.fit_transform(df)

#Create Pipelines
#Create one pipeline for each type of linear regression
from sklearn.linear_model import LinearRegression, Ridge, Lasso
lin_reg = LinearRegression()
rid_reg = Ridge()
las_reg = Lasso()

pipe_lin = Pipeline([
            ('feat_union', union),
            ('lin_reg', lin_reg)
        ])

pipe_rid = Pipeline([
            ('feat_union', union),
            ('rid_reg', rid_reg)
        ])
    
pipe_las = Pipeline([
            ('feat_union', union),
            ('las_reg', las_reg)
        ])

#Model Selection using Nested Cross-Validation
#neg_mean_absolute_error is used to improve explainability of the model
#also, outliers are not disproportionatlely important for price prediction
from sklearn.model_selection import GridSearchCV, cross_val_score, KFold

# Choose cross-validation techniques for the inner and outer loops,
# independently of the dataset.
inner_cv = KFold(n_splits=5, shuffle=True, random_state=i)
outer_cv = KFold(n_splits=5, shuffle=True, random_state=i)

pipe_lin.fit(df, df['total_price'])
nested_score_lin = cross_val_score(pipe_lin, df, y=df['total_price'], scoring='neg_mean_absolute_error', cv=outer_cv)
lin_reg_coefficients = pipe_lin.steps[1][1].coef_

print ("Linear Regression:")
print (nested_score_lin.mean())

label, cat_one_hot_encoder = categorial_transformer.steps[1]

#Create lists of (feature, coefficient) pairs for every column in the linear model
num_coef_list = [('accommodates', pipe_lin.steps[1][1].coef_[0]),
                  ('bathrooms', pipe_lin.steps[1][1].coef_[1]),
                  ('bedrooms', pipe_lin.steps[1][1].coef_[2]),
                  ('beds', pipe_lin.steps[1][1].coef_[3])]

cat_coef_list = []
counter = 4
for feat_list in cat_one_hot_encoder.categories_:
    for feat in feat_list:
        cat_coef_list.append((feat, pipe_lin.steps[1][1].coef_[counter]))
        counter += 1

amn_coef_list = [('Self check-in', pipe_lin.steps[1][1].coef_[counter]),
        ('Microwave', pipe_lin.steps[1][1].coef_[counter+1]),
        ('Stove', pipe_lin.steps[1][1].coef_[counter+2]),
        ('Dishes and silverware', pipe_lin.steps[1][1].coef_[counter+3]),
        ('Coffee maker', pipe_lin.steps[1][1].coef_[counter+4]),
        ('Oven', pipe_lin.steps[1][1].coef_[counter+5]),
        ('Cable TV', pipe_lin.steps[1][1].coef_[counter+6]),
        ('Cooking basics', pipe_lin.steps[1][1].coef_[counter+7]),
        ('Family/kid friendly', pipe_lin.steps[1][1].coef_[counter+8]),
        ('Dishwasher', pipe_lin.steps[1][1].coef_[counter+9]),
        ('Free street parking', pipe_lin.steps[1][1].coef_[counter+10]),
        ('Elevator', pipe_lin.steps[1][1].coef_[counter+11]),
        ('Luggage dropoff allowed', pipe_lin.steps[1][1].coef_[counter+12]),
        ('Private entrance', pipe_lin.steps[1][1].coef_[counter+13]),
        ('Free parking on premises', pipe_lin.steps[1][1].coef_[counter+14]),
        ('No stairs or steps to enter', pipe_lin.steps[1][1].coef_[counter+15]),
        ('Private living room', pipe_lin.steps[1][1].coef_[counter+16]),
        ('Pets allowed', pipe_lin.steps[1][1].coef_[counter+17]),
        ('Gym', pipe_lin.steps[1][1].coef_[counter+18]),
        ('Patio or balcony', pipe_lin.steps[1][1].coef_[counter+19]),
        ('24-hour check-in', pipe_lin.steps[1][1].coef_[counter+20])]

intercept = pipe_lin.steps[1][1].intercept_

#Grid Search for Ridge and Lasso Models
gs_rid = GridSearchCV(
    pipe_rid,
    {"rid_reg__alpha": [10,20,40]},
    cv = inner_cv,
    n_jobs = -1,
    scoring='neg_mean_absolute_error'
)
gs_rid.fit(df, df['total_price'])

nested_score_rid = cross_val_score(gs_rid, df, y=df['total_price'], scoring='neg_mean_absolute_error', cv=outer_cv)

print (gs_rid.best_params_)
print (nested_score_rid.mean())

gs_las = GridSearchCV(
    pipe_las,
    {"las_reg__alpha": [0.01,0.05,0.1]},
    cv = inner_cv,
    n_jobs = -1,
    scoring='neg_mean_absolute_error'
)
gs_las.fit(df, df['total_price'])

nested_score_las = cross_val_score(gs_las, df, y=df['total_price'], scoring='neg_mean_absolute_error', cv=outer_cv)

print (gs_las.best_params_)
print (nested_score_las.mean())


