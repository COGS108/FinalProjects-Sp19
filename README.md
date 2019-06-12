# COGS108_Team174
# Haoyin Xu
# Yosuke Koike
# Chin To Chim
# Haoqi Wu
# Pratyush Khurana


Procedure:
1. read csv file into panda dataframe
2. remove the missing values using dropna() although there was no missing value
3. droped the 'Code' column since it is repetetive with 'Name' column
4. checked if there are any 0 values in 'Year' column and 'Emissions' column using the command
data.astype(bool).sum(axis=0)
to see the number of non-zero values. I noticed there is 0 values in 'Year' columns although there are 48598-48156 = 442 zeros in 'Emissions' column. Thus I looked into the rows which has 0 values using
    ind = data.index[data['Emissions'] == 0].tolist()
    for x in ind:
        print(data.loc[x])
There we realized the coutries which have zero emissions are developing countries such as Palau, Malta or the Year is around 1970, which means it makes sense that the countries have no CO2 emissions. Hence, we concluded that the zero values are valid values.
5. We extracted the dataset of USA only since we only need information of USA, which will make our project more efficiently
6. We separated one dataset into 5 different dataset by industry so that it will be easier to analyze
7. We added the line plot which shows how the co2 emissions for different industries changed in USA from 1970 to 2016.
8. We added the central tendency and variability descriptions for our data, not including mode and variance.
9. In order to make the data more readable, we changed the unit of CO2 emissions from Gg/year to Tg/year.
