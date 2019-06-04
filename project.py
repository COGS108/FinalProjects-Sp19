#!/usr/bin/env python
# coding: utf-8

# # COGS 108 Final Project

# <h4>Group members: Hongyu Zou Sergio Villazon*add your name here*</h4>

# # Part 1: Introduction

# ## Background 

# ## Reformulated Research Question

# ## Hypothesis

# ## Datasets

# ## Ethical Consideration

# # Part 2: Data cleaning & Wrangling

# <h4>1. import libraries</h4>

# In[1]:


# Imports
# Display plots directly in the notebook instead of in a new window
get_ipython().run_line_magic('matplotlib', 'inline')

# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import patsy 
import scipy.stats as stats
import copy
import pydotplus
import io

from IPython.display import Image  
from sklearn.model_selection import train_test_split 
from sklearn import tree 
from sklearn.tree import export_graphviz
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


# In[2]:


# Configure libraries
# The seaborn library makes plots look nicer
sns.set()
sns.set_context('talk')

# Don't display too many rows/cols of DataFrames
pd.options.display.max_rows = 7
pd.options.display.max_columns = 8

# Round decimals when displaying DataFrames
pd.set_option('precision', 2)


# <h4>2. Read dataset and clean data</h4>

# In[3]:


# read the preprocessed data into the dataframe
df_total = pd.read_csv('Relationship Data.csv')
df_total.head()


# <p>We pick following five factors that could possibly influence the effectiveness of relationship from the table</p>
# 
# <ul>
#     <li>Race</li>
#     <li>Income</li>
#     <li>Education</li>
#     <li>Internet use when dating</li>
#     <li>Sex Orientation</li>
# </ul>
# 
# <p><u>Detailed Explaination</u></p>
# <ul>
#     <p>For race: we find race of both the answerer to the questionnaire and their partner</p>
#     <p>For income: we find income of 2016 for answerer and whether their partner earns more than them</p>
#     <p>For education: we have education level for answerer and their partner<p>
#     <p>For internet use: if answer have used internet to date with their partner then both sides use internet for dating</p>
#     <p>For sex orientation: we have if they are same sex couple or not</p>
# </ul>
#     

# In[4]:


# pick the five factors that could possibly influence the quality of relationship between couples

# race of the partner
df_race_partner = df_total['int_race'].to_frame()
df_race_answerer = df_total['Q6B'].to_frame()

# 2016 income for answerer and if his/her partner earns more than him/her
df_income_answerer = df_total['ppincimp'].to_frame()
df_income_partner = df_total['Q23'].to_frame()

# education level for both sides
df_edu_answerer = df_total['Q10'].to_frame()
df_edu_partner = df_total['ppeducat'].to_frame()

# internet use when dating
df_internet = df_total['Q32'].to_frame()

# if they are same sex people or not
df_sexOrient = df_total['w6_same_sex_couple'].to_frame()


# <p><b>Drop missing values from the data</b></p>

# In[5]:


df_race_answerer.dropna(inplace=True)
df_race_partner.dropna(inplace=True)
df_income_answerer.dropna(inplace=True)
df_income_partner.dropna(inplace=True)
df_edu_answerer.dropna(inplace=True)
df_edu_partner.dropna(inplace=True)
df_internet.dropna(inplace=True)
df_sexOrient.dropna(inplace=True)


# <p>In order to measure the quality of relationship, we pick the following questions from the questionnaire as a measurement standard of quality of relationship</p>
# 
# <ul>
#     <li>In general, how would you describe the quality of your relationship with your partner</li>
#     <li>During the last 12 months, about how often did you have sex with your partner</li>
#     <li>In the past year, have you ever met someone for dating, for romance, or for sex *besides* your partner</li>
# <ul>
#         

# In[6]:


# answerer's reply to their quality of relationship
df_quality = df_total['Q34'].to_frame()

# answerer's reply to their sex frequency
df_sexFreq = df_total['w6_sex_frequency'].to_frame()

# answer's reply about if they have other dates
df_other_date = df_total['w6_otherdate'].to_frame()


# <p><b>Drop missing values from the data</b></p>

# In[7]:


df_quality.dropna(inplace=True)
df_sexFreq.dropna(inplace=True)
df_other_date.dropna(inplace=True)


# <p>We merge those columns together based on the index to have a better format of data. Because in the original dataset each index corresponds to each individual, so we can safely directly merge them based on the index</p>

# In[8]:


# merge all the columns we have above together based on index
lst = [df_income_answerer, df_income_partner, df_edu_answerer, df_edu_partner, df_internet, df_sexOrient, df_race_answerer, df_race_partner,
                         df_quality, df_sexFreq, df_other_date]

df_individual = df_race_answerer

for ele in lst:
    df_individual = pd.merge(df_individual, ele, right_index = True, left_index = True)


# In[9]:


df_individual.head()


# <p>Rename the columns to be name of the factors/ name of the quality measurement</p>

# In[10]:


df_individual.drop("Q6B_x", axis = 1, inplace=True)
df_individual = df_individual.rename(columns={"Q6B_y": "race_partner", "int_race" : "race_answerer", "ppincimp": "income", "Q23":"income_comp", "Q10":"partner_degree", 
                               "ppeducat" : "degree", "Q32":"internet", 'w6_same_sex_couple': "sax_orient",
                               "Q34":"quality", "w6_sex_frequency":"sex_freq", "w6_otherdate":"other_date"})

df_individual.columns


# <p>Display the table after cleaning</p>

# In[11]:


df_individual


# <h1>Part 3: Descriptive & Explanatory</h1>

# <h4>Dataframe Summary</h4>
# <p>We alredy have our table of information regarding the information involving five factors 
# and quality measurement of answerers and their partners </p>

# In[12]:


desc = df_individual.describe()
desc


# We can draw some simple conclusions from our the summary of dataset.
# <ul>
#     <li>From the summary of the dataset we know that after excluding the null values we still have more than 1000 number of samples, which still meets the requirements</li>
#     <li> From the summary of income we can know:</li> 
#         <ul>
#             <li>Over 50% of the race of the answerers are white
#             <li>Over 90% of the answerers have not dated with someone else during the current relation
#             <li>Over 50% of the answerers have an excellent relationship with their partner
#             <li>Over 37% of the answerers have an Bachelor's degree
#             <li>Around 40% of the answerers' partners have higher income than them
#             <li>Over 80% of the answerers did not use internet ways to date their partner
#             <li>Over 90% of the answers are not same sex couple
#             <li>Arouhnd 30% of the answers have sex frequency one month or less
#         </ul>
# </ul>
# 
# <p>
# Because our dataset is collected based on random sampling, we expect that it contains no systemetic errors  and will reflect general case in United States</p>

# <h4>Analysis Method</h4>
# <p>We decide to use a predictive model based on regression to help the analysis of our model.</p>
# <p>Here are the steps we will follow to build our model and analyze the data</p>
# <ul>
#   <li>Transform catagorical values from the table into comparable integers</li>
#   <li>Train the regression model using the first half of the dataframe and build our model</li>
#   <li>Predict the other half the dataframe using the current regression model</li>
#   <li>Check if our model is strong enough for predicting result of relationship</li>
#   <li>Comparing the effectiveness of different factors on the quality of relationship</li>
# </ul>

# <h4>1. Transform catagorical values from table into comparable integers</h4>
# <p>We first tranform the measurement of quality of relationship from catagorical values into integers</p>

# In[13]:


# transform the quality of relationship into integer values
dic = {"Excellent": 5, "Good": 4, "Fair":3, "Poor":2, "Very Poor":1}
df_individual['quality'].replace(dic, inplace=True)
df_individual.head()


# In[14]:


# transform sex frequency from catagorical into numbers
# we assume that those who have higher sex frequency will have better relationship than those who have fewer sex
dic = {"Once a day or more": 5, "3 to 6 times a week": 4, "Once or twice a week":3, "2 to 3 times a month":2, "Once a month or less":1}
df_individual['sex_freq'].replace(dic, inplace=True)
df_individual.head()


# <p>
#     Changing income variables to easier numbers to work with, averaging lower bound and upper bounds for result 
# </p>

# In[15]:


# Helper Variables
change = False
avg_array = []

# Go through income in order to find the array 
for income in df_individual['income']:
    temp_string = income.split()
    try:
        # Get lower bounds if possible
        lower_bound = temp_string[0].replace("$","")
        lower_bound = int(lower_bound.replace(",",""))
    except ValueError:
        change = True
    try:
        # Get upper bounds if possible
        upper_bound = temp_string[2].replace("$","")
        upper_bound = int(upper_bound.replace(",",""))
        if change:
            lower_bound = upper_bound
            change = False
    except ValueError:
        upper_bound = lower_bound

    # Obtain array and get it 
    average = np.average([lower_bound,upper_bound])
    avg_array.append(average)
    
# Assign it to a new column in the dataframe 
df_individual = df_individual.assign( int_income=avg_array )


# <p>
#     Changing partner's income into easier numbers to work with.
#     <br>
#     'I earned more' becomes 2
#     <br>
#     '[Partner Name] earned more' becomes 1
#     <br>
#      'We earned about the same amount' becomes 0
#     <br>
#     '[Partner Name] was not working for pay' becomes -1 
#     <br> 
#     'Refused' becomes becomes -2 
# </p>

# In[16]:


income_comp = []

# Go through partner's income in order to find the array 
for income in df_individual['income_comp']:
    temp_string = income
    if temp_string  == '[Partner Name] earned more':
        output = 1
    elif temp_string == 'I earned more':
        output = 2
    elif temp_string == 'We earned about the same amount':
        output = 0
    elif temp_string == '[Partner Name] was not working for pay':
        output = -1 
    elif temp_string == 'Refused':
        output = -2
    
    income_comp.append(output)
df_individual = df_individual.assign( int_income_comp=income_comp )


# <p>
#     <h5>Changing partner's degree into values that we want to work with </h5>
#     <br>
#     'Professional or Doctorate degree' = 4 
#      <br>
#     'Master's degree' = 4
#     <br>
#     'Bachelor's degree' = 3
#     <br>
#     'Associate degree' = 2
#     <br>
#     'Some college, no degree' = 1 
#     <br>
#     'HS graduate or GED' = 1 
#     <br>
#     '12th grade no diploma', '11th grade', '10th grade', '9th grade' become  0
#     <br>
#     '7th or 8th grade', '5th or 6th grade', 'Refused', and 'No formal education' and '1st-4th grade' become -1 
# </p>

# In[17]:


education = []

# Go through partner's income in order to find the array 
for income in df_individual['partner_degree']:
    temp_string = income
    if temp_string  == 'Master\x92s degree'or temp_string == 'Professional or Doctorate degree':
        output = 4
    elif temp_string == 'Bachelor\x92s degree':
        output = 3
    elif temp_string == 'Associate degree':
        output = 2
    elif temp_string == 'Some college, no degree' or temp_string == 'HS graduate or GED':
        output = 1 
    elif temp_string == '12th grade no diploma' or temp_string == '11th grade' or temp_string == '10th grade' or temp_string == '9th grade':
        output = 0
    else:
        output = -1 
    
    education.append(output)
df_individual = df_individual.assign( partner_degree=education )


# In[18]:


dic = {"Bachelor's degree or higher": 4, 'High school': 3, 'Some college':2,  'Less than high school':1}
df_individual['degree'].replace(dic, inplace=True)


# <p>
#     <h5>Transforming internet use for dating to integers</h5>
#     <br>
#     'NO meet partner through internet' = 0
#      <br>
#     'Meet partner through internet' = 1
# </p>

# In[19]:


internet_array = []

# Go through partner's income in order to find the array 
for income in df_individual['internet']:
    temp_string = income
    if temp_string  == 'No, I did NOT meet [Partner Name] through the Internet':
        output = 0
    else: 
        output = 1
    internet_array.append(output)
df_individual = df_individual.assign( internet=internet_array )    


# In[20]:


dic = {'NOT same-sex souple': 1,  'same_sex_couple': 0}
df_individual['sax_orient'].replace(dic, inplace=True)


# In[21]:


dic ={ 'No, I have not met anyone for dating, romance, or sex besides [Partner Name] in the past year.': 1,
 'Yes, I have met at least one person for dating, romance, or sex besides [Partner Name] in  the past year.': 0,
 'Refused': -1 }
df_individual['other_date'].replace(dic, inplace=True)


# In[22]:


# drop columns that are redundant resulting from transformation
df_individual.drop(['income', 'income_comp'], inplace=True, axis=1)


# In[23]:


df_individual['int_income']


# <p> Add a separate column here 'comp_degree' that determines the degree of both the partner and the interviewee

# In[24]:


df_individual['comp_degree'] = df_individual['degree'] + df_individual['partner_degree']


# In[25]:


df_individual.columns


# In[26]:


df_individual['race_answerer'].unique()


# In[27]:


df_individual['int_race_answerer'] = df_individual['race_answerer'].map({
    'White':0, 'Black':1, 'Some other race':2, 'Asian Indian ':3,
       'American Indian':4, 'Japanese ':5, 'Chinese ':6, 'Guamanian':7,
       'Other Asian':8, 'Filipino ':9, 'Korean':10, 'Refused':-1, 'Hawaiian':11,
       'Vietnamese':12, 'Samoan':13, 'Other Pacific Islander':14
})


# In[28]:


df_individual['int_race_answerer'].unique()


# <p>
#     <b>For Decision Trees</b>
#     <br/>
#     We want to take a copy of our data_frame, to clean it for decision trees
# </p>

# In[29]:


df_trees = copy.copy(df_individual)


# <p>
#    We only choose the columns of most importance to us, we drop na values and we drop those who have refused to answer quality
# <p>

# In[30]:


df_trees = df_trees[['degree','internet','sax_orient','int_income','int_income_comp','other_date','quality']]
df_trees = df_trees.dropna()
df_trees = df_trees[df_trees['quality'] != 'Refused']


# <h1>Decision Trees, part 1</h1>
#     
# <p>
#     Given that our data did not appear to be normally distributed, we decided then we should shift our focus to
#     create a decision tree model.     
#     In order to build our decision trees, we decided that our features would 
#     be comprised of the following:
#     <ul>
#         <li> Degree of the answerer</li>
#         <li> Whether the relationship began from internet use </li>
#         <li> The income of the answerer </li>
#         <li> The combined income of the answerer and their partner </li>
#         <li> Whether or not the answerer cheated on the partner </li>
#     </ul>
#     <br>
# </p>

# In[31]:


# Get valid features
df_features = df_trees[['degree','internet','sax_orient','int_income','int_income_comp','other_date']]

# Obtain the labels
df_labels = df_trees['quality']
df_labels=df_labels.astype('int')


# <p>Using sklearns train_test_split model, we create training and testing data from our features and labels</p>

# In[32]:


X_train, X_test, y_train, y_test = train_test_split(df_features, df_labels, random_state=1)


# We create a DecisionTreeClassifer using sklearn 

# In[33]:


model = tree.DecisionTreeClassifier()


# In[34]:


model


# In[35]:


# Fit the model with our training and testing data
model.fit(X_train, y_train)


# In[36]:


# Obtain predicitions from model using X_test
y_predict = model.predict(X_test)


# In[37]:


accuracy_score(y_test, y_predict)


# <h1>Decision Trees, part 2</h1>
#     
# <p>
#     Our decision tree model did not have a high accuracy (around 50%) 
#     <br>
#     We wondered if the reason for this could have been the range of our labels. 
#     Our team did some research and found that decision trees work better with a binary label, whereas our labels ranged from 5-0 
#     <br>
#     <br>
#     Therefore, we decided to change the labels of our decision tree to binary. 
#     Given that our labels 5-3 were originally values that ranged from "Excellent" to "Fair" we 
#     decided that these would be considered could be considered as "good" relationships. Therefore we made the following change:
#     <br>
#     <br>
#     <b>Labels 5-3 became label 1, and the remaining labels would be 0</b>
# </p>

# In[38]:


dic = {5:1, 4:1, 3:1, 2:0, 1:0}
df_labels.replace(dic, inplace=True)


# In[39]:


df_labels.head()


# <p>
#     We begin to build the tree again.
# </p>

# In[40]:


X_train, X_test, y_train, y_test = train_test_split(df_features, df_labels, random_state=1)


# In[41]:


model = tree.DecisionTreeClassifier()


# In[42]:


model


# In[43]:


model.fit(X_train, y_train)


# In[44]:


y_predict = model.predict(X_test)


# In[45]:


accuracy_score(y_test, y_predict)


# <p>
#     Our accuracy increased significantly, to over 95%
#     <br>
#     For this decision tree model, we also decided to create a visual representation for the tree
# </p>

# In[46]:


dot_data = io.StringIO()
export_graphviz(model, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True, feature_names=df_features.columns)


# In[47]:


graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph


# In[48]:


Image(graph.create_png())

