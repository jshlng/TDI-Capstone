# TDI-Capstone

# Business Objective
The project deliverable is a pricing tool for potential airbnb hosts looking to rent their property on airbnb.com. Hosts can input basic info about their property into the pricing tool, which will return a suggested price that takes into consideration all the other listings on the market in that particular city. This will allow hosts to maximize the potential revenue from their property, and reduce uncertainty about pricing and revenue projections.

From a big picture standpoint, this project will aid in overall pricing efficiency, which benefits the market as a whole. Therefore there’s a strong incentive for Airbnb themselves to create a user-friendly tool for hosts to help price their listings. Reduced uncertainty about revenue and pricing will encourage more hosts to put short term rentals on the market.

# Data Ingestion
Data for this project was sourced from insideairbnb.com. Inside Airbnb is an independent, third-party website that provides publicly available data from airbnb listings around the world. In particular, the project focuses on building a pricing tool for listings in Boston, New York City, and San Francisco. Inside Airbnb provides snapshots of airbnb listings in each of those geographies. The data used in this project was from July 2019 snapshots of each city.

Boston data: http://data.insideairbnb.com/united-states/ma/boston/2019-07-14/data/listings.csv.gz  
New York City data: http://data.insideairbnb.com/united-states/ny/new-york-city/2019-07-08/data/listings.csv.gz  
San Francisco data: http://data.insideairbnb.com/united-states/ca/san-francisco/2019-07-08/data/listings.csv.gz

The majority of the independent data ingestion work for the project was in the feature selection and processing. Since the business objective is to inform potential hosts of pricing information, the selected features are information about the listing available before it is put on the market. This excludes information from reviews or other feedback that will have strong predictive power in determining the price. Additionally, the number of features was carefully selected because of the size of that data sets in each city. For Boston and San Francisco, there are approximately 5000 listings, while in New York City there are 45000. To build a linear regression model from this amount of data, 8 features were selected for the cities with 5000 data points, while 20 features were selected for NYC since the amount of data could support a model of that complexity.

# Visualizations

The first plot shows the calculated average dollar value for each of 21 different amenities listed on Airbnb. This was calculated by averaging the coefficients corresponding to a particular amenitity from the linear model of each city. The amenities are listed in order of decreasing value.

![Amenities Plot](https://github.com/jshlng/TDI-Capstone/blob/master/AmenitiesPlot.png)

As you can see on the plot, the most valuable amenity is a gym, which on average increases the price of an airbnb by $136 compared to an airbnb without a gym, assuming everything else stays constant. It's important to note, however, that these features are not indpenedent. For example, having a gym in an airbnb likely means the property is in a larger building, also increasing the likelyhood of there being an elevator. Since these features often co-present, the model is not able to tease out how much the increase in value is from the gym or the elevator in isolation from each other. This interplay between features can also help explain why the least valuable amenities have a negative dollar value according to the linear model. In complete isolation, having dishes and silverware available in an airbnb will not reduce the price by $56. However, dishes and silverware as an amenity may be correlated with a particular zipcode, or property-type, or maybe just correlated with fewer expensive amenities so the model calculates a negative coefficient for that feature. 

2: Machine learning metrics comparing various linear regression methods


# Machine Learning and Interactive Website
Machine Learning Model

The price prediction tool is build upon three linear regression models, one for each city. The features used in the Boston model and the San Francisco model are below:

'zipcode', 'property_type', 'room_type', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'bed_type'

In addition to these 8 features, the 12 most common amenities are included in the features for the New York City model, for a total of 20 features.

Comparison between linear, ridge, and lasso linear regression model metrics.

Website via heroku/flask.

# Deliverable
Github repo and heroku/flask website.
