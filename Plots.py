#Charts for Capstone Project

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import operator

#Boston Data
bos_amn_coef = [('Self check-in', -19.248273181480712),
 ('Microwave', 6.58305865369477),
 ('Stove', -0.5340856456191677),
 ('Dishes and silverware', -24.684298009221745),
 ('Coffee maker', 21.064401367537396),
 ('Oven', -32.74049797994334),
 ('Cable TV', 10.27762790740533),
 ('Cooking basics', 33.90412262197459),
 ('Family/kid friendly', -0.017047763524058224),
 ('Dishwasher', 21.231414884881467),
 ('Free street parking', 1.6899680687020666),
 ('Elevator', 53.44557916799452),
 ('Luggage dropoff allowed', -2.9213130316117475),
 ('Private entrance', 4.334934589808325),
 ('Free parking on premises', -8.44876207181063),
 ('No stairs or steps to enter', -42.54142654302729),
 ('Private living room', 21.844673539175567),
 ('Pets allowed', -19.290614646686578),
 ('Gym', 49.286519153700816),
 ('Patio or balcony', -7.727733971805114),
 ('24-hour check-in', 34.476682955069464)]

#NYC Data
nyc_amn_coef = [('Self check-in', -8.672856632460217),
 ('Microwave', -4.9621118686690435),
 ('Stove', -30.163594459131218),
 ('Dishes and silverware', -9.402922114549858),
 ('Coffee maker', 7.368663119460597),
 ('Oven', 40.57564677407602),
 ('Cable TV', 13.035877381830305),
 ('Cooking basics', -16.512103147069716),
 ('Family/kid friendly', -4.465516231484704),
 ('Dishwasher', 23.51455950617538),
 ('Free street parking', -4.270187024431402),
 ('Elevator', 16.900322402357396),
 ('Luggage dropoff allowed', 4.610516498622159),
 ('Private entrance', 1.8158823724309698),
 ('Free parking on premises', 1.2457543072323602),
 ('No stairs or steps to enter', -0.770983723976742),
 ('Private living room', 1.6139192483042202),
 ('Pets allowed', -9.0485056625368),
 ('Gym', 28.364313313743942),
 ('Patio or balcony', -0.25480210044840523),
 ('24-hour check-in', -3.981648068539019)]

#SF Data
sf_amn_coef = [('Self check-in', -23.634126212039927),
 ('Microwave', -11.095045116164199),
 ('Stove', -24.082352943450015),
 ('Dishes and silverware', -22.520889704890077),
 ('Coffee maker', 27.346747927018576),
 ('Oven', 18.882981866644045),
 ('Cable TV', 13.211921427210836),
 ('Cooking basics', -33.06115107008044),
 ('Family/kid friendly', -26.525648010186764),
 ('Dishwasher', 42.51907660750575),
 ('Free street parking', 19.98468461737906),
 ('Elevator', 32.64976880521727),
 ('Luggage dropoff allowed', 0.43074486346097346),
 ('Private entrance', -1.5290681305498874),
 ('Free parking on premises', 14.923292091661272),
 ('No stairs or steps to enter', -3.0240003893642546),
 ('Private living room', -10.955592216005176),
 ('Pets allowed', -21.89821143072365),
 ('Gym', 59.29426459774423),
 ('Patio or balcony', 23.41848944902945),
 ('24-hour check-in', -8.04449032193547)]

total_coef = []
for i in range (0,len(bos_amn_coef)):
    total_coef.append((bos_amn_coef[i][0], bos_amn_coef[i][1], nyc_amn_coef[i][1], sf_amn_coef[i][1],
                       bos_amn_coef[i][1]+nyc_amn_coef[i][1]+sf_amn_coef[i][1]))
total_coef.sort(key=operator.itemgetter(4), reverse=True)

labels = [x[0] for x in total_coef]
avg_values = [x[4] for x in total_coef]
bos_values = [x[1] for x in total_coef]
nyc_values = [x[2] for x in total_coef]
sf_values = [x[3] for x in total_coef]

plt.rcParams["figure.figsize"] = (14,8)
plt.rc('ytick',labelsize=14)
x = np.arange(len(labels))  # the label locations
width = 0.4  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x, avg_values, width, label='Avg $')
#rects2 = ax.bar(x - width*.5, nyc_values, width, label='NYC')
#rects3 = ax.bar(x + width*.5, sf_values, width, label='SF')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Dollar Value', fontsize = 18)
ax.set_title('Linear Model Coefficients for 21 Common Amenities', fontsize = 24)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize = 14)
plt.xticks(rotation=90)
#ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = int (rect.get_height())
        if (height >= 0):
            offset = 3
        else:
            offset = -17
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, offset),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize = 12)


autolabel(rects1)
#autolabel(rects2)
#autolabel(rects3)

plt.show()