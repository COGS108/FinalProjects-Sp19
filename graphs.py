#!/usr/bin/env python
# coding: utf-8

# In[55]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataFile = pd.read_csv('~/Downloads/Projects-master/new.csv')
plt.scatter(dataFile.median_household_income, dataFile.percent_no_internet, s=20)
plt.xlabel('median_income')
plt.ylabel('percent_no_income')
f5 = plt.gcf()


# In[56]:


plt.scatter(dataFile.median_age, dataFile.percent_no_internet, s=20)
plt.xlabel('median_age')
plt.ylabel('percent_no_income')
f5 = plt.gcf()


# In[57]:


plt.scatter(dataFile.AllAgesinPovertyPercent, dataFile.percent_no_internet, s=20)
plt.xlabel('poverty_percent')
plt.ylabel('percent_no_internet')
plt.xlim(0,50)
plt.ylim(0,100)
f5 = plt.gcf()


# In[58]:


def percentageEducated():
    list_PercentAboveHS = []
    list_PercentBelowHS = []
    sumTotal = 0
    sumBelowHS = 0
    
    for index,row in dataFile.iterrows():
        
        sumTotal = (row['P_below_middle_school'] + row['P_some_high_school']
                        +row['P_high_school_equivalent']+row['P_some_college']
                            +row['P_bachelor_and_above'])
        sumBelowHS = (row['P_below_middle_school'] + row['P_some_high_school']
                        +row['P_high_school_equivalent'])
        list_PercentBelowHS.append(sumBelowHS/sumTotal)
        list_PercentAboveHS.append(1-(sumBelowHS/sumTotal))
        
        
        
        
    dataFile['Percent_Population_Above_HS_Education'] = list_PercentAboveHS
    dataFile['Percent_Population_Below_HS_Education'] = list_PercentBelowHS        
    #print(dataFile['Percent_Above_HS'])
    #print(dataFile['Percent_Below_HS'])
    #print(dataFile)

#percentageEducated()


# In[59]:


percentageEducated()
plt.scatter(dataFile.Percent_Population_Above_HS_Education, dataFile.percent_no_internet, s=20)
plt.xlabel('percent_Population_Above_HS_Education')
plt.ylabel('percent_no_internet')
f5 = plt.gcf()


# In[60]:


plt.scatter(dataFile.Percent_Population_Below_HS_Education, dataFile.percent_no_internet, s=20)
plt.xlabel('percent_Population_Below_HS_Education')
plt.ylabel('percent_no_internet')
f5 = plt.gcf()

