# TDI-Capstone

# Business Objective
The project deliverable is a pricing tool for potential airbnb hosts looking to rent their property on airbnb.com. Hosts can input basic info about their property into the pricing tool, which will return a suggested price that takes into consideration all the other listings on the market in that particular city. This will allow hosts to maximize the potential revenue from their property, and reduce uncertainty about pricing and revenue projections.

From a big picture standpoint, this project will aid in overall pricing efficiency, which benefits the market as a whole. Therefore there’s a strong incentive for Airbnb themselves to create a user-friendly tool for hosts to help price their listings. Reduced uncertainty about revenue and pricing will encourage more hosts to put short term rentals on the market.

# Data Ingestion
Data for this project was sourced from insideairbnb.com. Inside Airbnb is an independent, third-party website that provides publicly available data from airbnb listings around the world. In particular, the project focuses on building a pricing tool for listings in Boston, New York City, and San Francisco. Inside Airbnb provides snapshots of airbnb listings in each of those geographies. The data used in this project was from July 2019 snapshots of each city.

**Data Set Links:**  
Boston: http://data.insideairbnb.com/united-states/ma/boston/2019-07-14/data/listings.csv.gz  
New York City: http://data.insideairbnb.com/united-states/ny/new-york-city/2019-07-08/data/listings.csv.gz  
San Francisco: http://data.insideairbnb.com/united-states/ca/san-francisco/2019-07-08/data/listings.csv.gz

The majority of the independent data ingestion work for the project was in the feature selection and processing. Since the business objective is to inform potential hosts of pricing information, the selected features are information about the listing available before it is put on the market. This excludes information from reviews or other feedback that will have strong predictive power in determining the price.

Details of the data cleaning and feature selection process can be found in the code for the machine learning model, ml_model.py.

# Visualizations

The first plot shows the calculated average dollar value for each of 21 different amenities listed on Airbnb. This was calculated by averaging the coefficients corresponding to a particular amenitity from the linear model of each city. The amenities are listed in order of decreasing value.

![Amenities Plot](https://github.com/jshlng/TDI-Capstone/blob/master/AmenitiesPlot.png)

As shown on the plot, the most valuable amenity is a gym, which on average increases the price of an airbnb by $136 compared to an airbnb without a gym, assuming everything else is constant. It's important to note, however, that these features are not indpenedent. For example, a gym in an airbnb likely means the property is part of a larger building, also increasing the likelyhood of there being an elevator. Since these features often co-present, the model is not able to tease out how much the increase in value is from the gym or the elevator in isolation from each other. This interplay between features can also help explain why the least valuable amenities have a negative dollar value according to the linear model. In complete isolation, having dishes and silverware available in an airbnb will not reduce the price by $56. However, dishes and silverware as an amenity may be correlated with a particular zipcode, or property-type, or maybe just correlated with fewer expensive amenities so the model calculates a negative coefficient for that feature. 

Another key insight from the regression model is the regression coefficients for each zipcode. The maps below visualize this data for each city. Each marker represents a different zipcode. The darker the marker, the greater the price of airbnbs located in that particular zipcode. A snapshot of each map is provided in the readme, please see the google map links below for the full details. Each zipcode marker on the google map contains its respective linear regression coefficient.

**Google Map Links:**  
Boston: https://drive.google.com/open?id=1kt4_j-qRS3QgmAITRrr0IkxeKY-c0hii&usp=sharing  
NYC: https://drive.google.com/open?id=1DQ4r6nTX6n4p-6Z6QfQ9bJC-OksR4ZrN&usp=sharing  
SF: https://drive.google.com/open?id=1IUmKSRKL2hq5ZWpnsrDbbZaMgkBv3raF&usp=sharing  

## Boston
![Boston Zipcodes Snapshot](https://github.com/jshlng/TDI-Capstone/blob/master/BostonZipcodeCoefficientsMap.png)

## NYC
![NYC Zipcodes Snapshot](https://github.com/jshlng/TDI-Capstone/blob/master/NYCZipcodeCoefficientsMap.png)

## SF
![SF Zipcodes Snapshot](https://github.com/jshlng/TDI-Capstone/blob/master/SFZipcodeCoefficientsMap.png)


# Machine Learning Model and Metrics

### Machine Learning Model

The price prediction tool is built using three linear regression models, one for each city. The training data for Boston and San Francisco had approximately 5000 listings each, while the training data for New York City had ~45000. After data cleaning, the SF data set has 3692 listings, the Boston data set has 5182 listings, and the NYC data set has 31736 listings.

Two sets of features were used to train the models. The first set is only 8 basic features, while the second set adds 21 of the most commmon amenities listed on airbnbs on top of the basic features from the first set.

**1st Set of Features:**  
* 4 numerical features: 'accommodates', 'bathrooms', 'bedrooms', 'beds'
* 4 categorical features: 'zipcode', 'property_type', 'room_type', 'bed_type'

**2nd Set of Features:**  
* 'Self check-in', 'Microwave', 'Stove', 'Dishes and silverware', 'Coffee maker', 'Oven', 'Cable TV', 'Cooking basics', 'Family/kid friendly', 'Dishwasher', 'Free street parking', 'Elevator', 'Luggage dropoff allowed', 'Private entrance', 'Free parking on premises', 'No stairs or steps to enter', 'Private living room','Pets allowed', 'Gym', 'Patio or balcony', '24-hour check-in'

Additionally, three different regression methods were used: linear regression, ridge regression, and lasso regression. The mean standard error was used to determine the best model. The mean standard error is the average difference between the predicted price and the true price of each listing. This type of error is perfect for price prediction because it weighs a $20 error in price exactly twice as much as a $10 error, and reduces the effect of outliers on the model.

### Mean Standard Errors for Each Regression Model:

  Regression Model | Boston (-Amn) | Boston (+Amn) | NYC (-Amn) | NYC (+Amn) | SF (-Amn) | SF (+Amn) |
 ---------- | ---------- |---------- |---------- |---------- |---------- |---------- |
 Linear | 88.94 | 89.72 | 73.78 | 73.77 | 98.48 | 97.14 |
 Ridge | 88.78 | 89.41 | 72.83 | 72.45 | 97.51 | 96.52 |
 Lasso | 88.74 | 89.48 | 72.92 | 72.71 | 97.87 | 96.72 |

The ridge and lasso regression algorithms perform slightly better than the linear model across all three cities. The 2nd feature set performs slightly better than the 1st feature set in NYC and SF, but performs slightly worse in Boston. Comparing models across cities, NYC models are better than the Boston models, which are better than the SF models. This is unsurprising given the number of cleaned data points in each data set (NYC with 31736, Boston with 5182, and SF with 3692).

# Deliverable
Github repo and readme with data visualizations.
