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

As shown on the plot, the most valuable amenity is a gym, which on average increases the price of an airbnb by $136 compared to an airbnb without a gym, assuming everything else stays constant. It's important to note, however, that these features are not indpenedent. For example, having a gym in an airbnb likely means the property is in a larger building, also increasing the likelyhood of there being an elevator. Since these features often co-present, the model is not able to tease out how much the increase in value is from the gym or the elevator in isolation from each other. This interplay between features can also help explain why the least valuable amenities have a negative dollar value according to the linear model. In complete isolation, having dishes and silverware available in an airbnb will not reduce the price by $56. However, dishes and silverware as an amenity may be correlated with a particular zipcode, or property-type, or maybe just correlated with fewer expensive amenities so the model calculates a negative coefficient for that feature. 

Another key insight from the regression model is the regression coefficients for each zipcode. The maps below visualize this data for each city. Each marker represents a different zipcode. The darker the marker, the greater the price of airbnbs located in that particular zipcode. A snapshot of each map is provided in the readme, please see the google map links below for the full details. Each zipcode marker on the google map contains its respective linear regression coefficient.

**Google Map Links:**  
Boston: https://drive.google.com/open?id=1kt4_j-qRS3QgmAITRrr0IkxeKY-c0hii&usp=sharing  
NYC: https://drive.google.com/open?id=1DQ4r6nTX6n4p-6Z6QfQ9bJC-OksR4ZrN&usp=sharing  
SF: https://drive.google.com/open?id=1IUmKSRKL2hq5ZWpnsrDbbZaMgkBv3raF&usp=sharing  

## Boston
![Amenities Plot](https://github.com/jshlng/TDI-Capstone/blob/master/BostonZipcodeCoefficientsMap.png)

## NYC
![Amenities Plot](https://github.com/jshlng/TDI-Capstone/blob/master/NYCZipcodeCoefficientsMap.png)

## SF
![Amenities Plot](https://github.com/jshlng/TDI-Capstone/blob/master/SFZipcodeCoefficientsMap.png)


# Machine Learning and Interactive Website

### Machine Learning Model

The price prediction tool is built using three linear regression models, one for each city. To train each regression model, I used the data sets from insideairbnb.com, (see links above in the Data Ingestion section). For Boston and San Francisco, there are approximately 5000 listings, while in New York City there are ~45000. 

I compared two different sets of features to train the models. The initial set is only 8 basic features, and the second set includes 21 of the most commmon amenities listed on airbnbs.

The 8 basic features are as follows: 
* 4 numerical features: 'accommodates', 'bathrooms', 'bedrooms', 'beds'
* 4 categorical features: 'zipcode', 'property_type', 'room_type', 'bed_type'

The 21 common amenities are:
* 'Self check-in', 'Microwave', 'Stove', 'Dishes and silverware', 'Coffee maker', 'Oven', 'Cable TV', 'Cooking basics', 'Family/kid friendly', 'Dishwasher', 'Free street parking', 'Elevator', 'Luggage dropoff allowed', 'Private entrance', 'Free parking on premises', 'No stairs or steps to enter', 'Private living room','Pets allowed', 'Gym', 'Patio or balcony', '24-hour check-in'

Additionally, I used three different regression methods to fit the training data sets. To determine the best model, I compared the mean absolute error from each. The mean standard error is the average difference between the predicted price and the true price of each listing. I used this error because 



Website via heroku/flask.

# Deliverable
Github repo and heroku/flask website.
