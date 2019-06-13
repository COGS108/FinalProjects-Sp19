
# coding: utf-8

# # Introduction and background

# ## Overview

# For our final project, we performed a predictive analysis on data from Kickstarter to see which factors are more correlated with status of a Kickstarter project (successful or failed, which is defined whether they raised the goal amount of funding) and see if we can extraploate those correlations to predict which Kickstarter projects are more likely to be successful. We did so by taking a look at some of the variables associated with projects, such as duration, USD goal, categories, and start/end months for any associations between them and whether a project is successful or failed through visualization as well as statistical tests.

# ## Names
# 
# - Alan Lloyd Willey
# - Enlin Wei
# - Kanami Hannah Tanaka
# - Karen Rodriguez Pinto
# - Yumi Minami
# - Yuxiao Fan

# ## Group Members IDs
# 
# - A15746309
# - A12669124
# - A14714448
# - A15161856
# - A12938737
# - A14778609

# ## Research Question

# We are conducting this research to investigate what could be most predictive of a Kickstarter project's outcome, so the research question we wanted to ask for this project was "Among the US-based Kickstarters, which factor (within the information given in the dataset) contributes most to a Kickstarter's outcome?"
# 

# ## Background and Prior Work

# Before we introduce Kickstarter, we will take a look at crowdfunding platforms, which is what Kickstarter is. Basically, crowdfunding platforms allow those with innovative projects to pitch those projects to the public with a goal of a certain amount of money to raise; and if people like that idea and would like to support it, they can donate funds to help
# 
# A crowdfunding platforms like Kickstarter allows users to raise money and typically provide backer rewards or pre-order products. For example a filmmaker may offer a digital copy film, a live viewing of premier, signed posters, etc. A tech company could be offering pre-orders of their new phone cases or other product.
# 
# Kickstarter is a crowdfunding platform which was created by Perry Chen and Yancy Strickler in 2009, to be a place where the main focus is not Kickstarter's profit but success for those who pitch their projects. If a project raises enough money to meet its goal, it will receive those funds, and Kickstarter makes money from a 3-5% fee taken from the funds. Kickstarter does make efforts to ensure you keep your promises to backers and fraud charges could be made if you can't deliver or use funds improperly. Because funds from backers to creators cannot be charged unless the project reaches their goals, we consider this website is based on the perspectives of all-or-nothing.
# 
# References (include links):
# - 1) "Kickstarter crowdfunding site officially launches in Canada". The Canadian Press. 10 September 2013. Retrieved 8 June 2019. https://www.cbc.ca/news/business/kickstarter-crowdfunding-site-officially-launches-in-canada-1.1703774
# - 2) Isaac, Mike and David Gelles (September 21, 2015). "Kickstarter Focuses Its Mission on Altruism Over Profit". The New York Times. https://www.nytimes.com/2015/09/21/technology/kickstarters-altruistic-vision-profits-as-the-means-not-the-mission.html

# ## Hypothesis
# 

# we raised four hypothesis.
# 
# (1)We hypothesize that longer durations would likely mean a Kickstarter would fail, as that would mean backers are not as interested in the projects and thus the projects take longer to receive enough pledges to reach the goal (or may not reach the goal at all and fail). On the contrary, projects that are popular would receive pledges quickly and can hit the goal very soon.
# 
# (2)We hypothesize that the Kickstarters which fail will likely have a high USD goal, as pledgers are likely more drawn toward projects that are "cheap" (having low goals which can be reached quickly); especially when something has a goal that is relatively high, pledgers wouldn't want to have to pledge that much for something that isn't worth that much.
# 
# (3)We hypothesize that the main categories which possibly have strong influences on funding and become successful are ‘music’, ‘film and video’, and ‘publishing’ because those categories are easier to be promoted through funding promotions. Those categories are quite all rounders, which means that are quite inclusive to any age group, gender, or so on. Also, if the producer possibly have followers on their artistic work, it could make easier for them to acquire help for funding. Also, there could not any possible harms which be led from those products to backers, so psychologically speaking, it could be quite easier to be funded for them. Interestingly, we also assumed that the categories that failed easier could be the same categories which we assumed as the successful ones, because their funding is based on backers’ interests and preferences. In order to succeed in funding, the projects have to consider the backers’ popular and public trends; if one project was focused on one specific group of people, then it has a higher chance to fail.
# 
# (4)We hypothesize that projects which end later in the year (around October, November, December) have a higher chance of success because the end of the year is Thanksgiving and Christmas, where consumerism goes up because people tend buy a lot of things on holidays and might be more likely to try out the new products from Kickstarter projects. So people would likely pledge projects near the end of the year so that if it becomes successful they can buy the products for the holiday season.

# ## Dataset(s)

# - Dataset Name: Kickstarter Campaigns
# - Link to the dataset: https://www.kaggle.com/yashkantharia/kickstarter-campaigns
# - Number of observations: 192548
# 
# This dataset contains information about Kickstarter crowdfunding campaigns from 2014 to February 2019. The information includes the names, currency, main and subcategories, launch date and deadlines, goal amount of money to raise and actual amounts raised, whether the campaign was successful or failed, and geographical locations of the campaigns (country and state).
# 
# We found this dataset is interesting because of the following reasons:
# - Kickstarter funding have done by creators and backers, and they are not based on profits consideration for each other; backers do the funding for creators if they think their projects seemed successful or beneficial.
# - We can observe the data while considering the reasons why one projects went successful on funding but the other did not; There should be some factors having a correlation with successful ones and failed ones. 
# - This dataset has quite a lot of columns that we could make many researches, although we are not going through all of the possible research.

# # Data Analysis

# ## Data Cleaning & Pre-processing

# In[1]:


# imports
get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import patsy
import statsmodels.api as sm
import scipy.stats as stats

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)


# In[2]:


# loads Kickstarters data into dataframe
df_kickstarters = pd.read_csv("Kickstarter_projects_Feb19.csv")


# In[3]:


# viewing the first rows of the dataframe
df_kickstarters.head()


# We decided to add a column with the difference in goal_usd and usd_pledged.

# In[4]:


df_kickstarters = df_kickstarters.assign(goal_minus_pledge = df_kickstarters['goal_usd'] - df_kickstarters['usd_pledged'])


# We will first take the subset of US-based kickstarters only, since other countries may have different opinions on the kinds of projects they like and that could introduce confounding variations in our analysis. So we'll use country as a control and drop projects that are not US-based.

# In[5]:


df_kickstarters = df_kickstarters[df_kickstarters['country']=='US']


# We checked to see that the country and the currency are both US-only after the drop.

# In[6]:


df_kickstarters.country.unique()


# In[7]:


df_kickstarters.currency.unique()


# We then checked to see if any cell has null values, and if so to drop those entries.

# In[8]:


df_kickstarters[df_kickstarters.isnull().any(axis=1)]


# We checked the unique states.

# In[9]:


df_kickstarters['state'].unique()


# There are still many entries that are NOT US states, so we will clean that up so it only contains US states.

# In[10]:


def check_state(state_abbrv):
    lst_states = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UM', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']
    if state_abbrv in lst_states:
        return state_abbrv
    else:
        return 'X'


# In[11]:


df_kickstarters['state'] = df_kickstarters['state'].apply(check_state)


# In[12]:


df_kickstarters = df_kickstarters[df_kickstarters['state']!='X']


# In[13]:


# checking to see only 50 states
len(df_kickstarters['state'].unique())


# We found no null values in the dataset, and so we proceeded with data cleaning.

# We first dropped the column 'id' since it gives no useful information, just an ID associated with the project. We then dropped columns 'start_month' and 'end_month' since the information about the start and end months of the projects are already given in the dates in the 'launched_at' and 'deadline' columns and so is redundant. We checked to see that the country and currency are all US-based, so it would not be necessary to keep those columns.

# In[14]:


df_kickstarters.drop(columns=['id', 'country', 'currency'], inplace=True)


# Finally, we noticed some of the monetary amounts have more than 2 decimal places, which should be cleaned up since we don't work with monetary amounts more specific than 2 decimal places. So we decided to round the amounts to 2 decimal places.

# In[15]:


df_kickstarters['goal_usd'] = df_kickstarters['goal_usd'].round(2)
df_kickstarters['usd_pledged'] = df_kickstarters['usd_pledged'].round(2)


# ## Data visualization

# Since our project aims to analyze which factor is most important for the success of kickstarters, we will divide the dataframe into two separate ones, one with all the successful projects and one with all the failed projects.

# In[16]:


# divides df_kickstarters into successful and failed ones
df_successful = df_kickstarters[df_kickstarters['status']=='successful']
df_failed = df_kickstarters[df_kickstarters['status']=='failed']


# We next plotted the categories to see which ones are more likely to be successful.

# In[17]:


#plot histogram of the amount of projects among all the main_category
plt.figure(figsize=(20,8))
axPlt = sns.countplot(x='main_category',data=df_kickstarters)

for i in axPlt.patches:
    # get_x pulls left or right; get_height pushes up or down
    axPlt.text(i.get_x()+.18, i.get_height()+150,             str(round((i.get_height()), 2)), fontsize=11)


# Grouping by status:

# In[18]:


plt.figure(figsize=(20,10))
ax = sns.countplot(x='main_category',hue='status',data=df_kickstarters)

for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x(), i.get_height()+100,             str(round((i.get_height()), 2)), fontsize=11)


# It seems that there are unequal numbers of successful and failed projects; to confirm we'll take a look at how many successful and failed kickstarters there are.

# In[19]:


# views number of successful and failed kickstarters
print("Number of successful kickstarters: " + str(len(df_successful))); print("Number of failed kickstarters: " + str(len(df_failed)))


# It seems that there are different numbers of successful and failed kickstarters; we will account for that by comparing the ratio of each category in the successful versus failed kickstarters.

# In[20]:


df_categories = df_kickstarters.groupby(['status','main_category'])['status'].count().unstack('main_category').fillna(0)
sub_df_categories = np.transpose(df_categories.div(df_categories.sum()))
sub_df_categories.plot(kind='bar',stacked=True,rot=0, figsize=(20,5))

plt.legend(('failed','successful'), loc='center left', bbox_to_anchor=(1.0, 0.5))


# Next we tried visualizing all the numerical data to see their distributions.

# In[21]:


#distribution of duration
plt.figure(figsize=(20,8))
plt.title('Distributions of duration')
plt.ylabel('proportion')

sns.distplot(df_successful['duration'],label='Successful',color='green',hist=False)
sns.distplot(df_failed['duration'],label='Failed',color='red',hist=False)


# In[22]:


#distribution of goal_usd
plt.figure(figsize=(20,8))
plt.title('Distributions of goal_usd')
plt.ylabel('proportion')

sns.distplot(df_successful['goal_usd'],label='Successful',color='green',hist=False)
sns.distplot(df_failed['goal_usd'],label='Failed',color='red',hist=False)


# In[23]:


#distribution of usd_pledged
plt.figure(figsize=(20,8))
plt.title('Distributions of usd_pledged')
plt.ylabel('proportion')

sns.distplot(df_successful['usd_pledged'],label='Successful',color='green',hist=False)
sns.distplot(df_failed['usd_pledged'],label='Successful',color='red',hist=False)


# In[24]:


#distribution of blurb_length
plt.figure(figsize=(20,8))
plt.title('Distributions of blurb_length')
plt.ylabel('proportion')

sns.distplot(df_successful['blurb_length'],label='Successful',color='green',hist=False)
sns.distplot(df_failed['blurb_length'],label='Failed',color='red',hist=False)


# In[25]:


#distribution of name_length
plt.figure(figsize=(20,8))
plt.title('Distributions of name_length')
plt.ylabel('proportion')

sns.distplot(df_successful['name_length'],color='green',hist=False)
sns.distplot(df_failed['name_length'],color='red',hist=False)


# In[26]:


#distribution of star_month
plt.figure(figsize=(20,8))
plt.title('Distributions of start_month')
plt.ylabel('proportion')

sns.distplot(df_successful['start_month'],color='green',hist=False)
sns.distplot(df_failed['start_month'],color='red',hist=False)


# In[27]:


#distribution of end_month
plt.figure(figsize=(20,8))
plt.title('Distributions of end_month')
plt.ylabel('proportion')

sns.distplot(df_successful['end_month'],color='green',hist=False)
sns.distplot(df_failed['end_month'],color='red',hist=False)


# ## Data Analysis

# Upon these initial visualization of data, we can see that comics, dance, and music seem to have the highest success rates while food, journalism, and technology seem to not do that well. When we compare the overall number of kickstarters in each category, we can see that dance is the least and music is the most popular category, both being the most successful categories. However, it seems that the amount of kickstarters did not effect the rate of successes and failures in each category. 

# For the next part of our analysis, we will try to search for differences between successful/failed kickstarters to help distinguish what attributes the successful starters had that the failed didn't.

# check how many unique main categories and sub categories there are：

# In[28]:


len(df_kickstarters['sub_category'].unique())


# In[29]:


len(df_kickstarters['main_category'].unique())


# We will drop some more columns:
# - For data on start/end dates of projects, we agreed that observing trends at the month level is best, so we will drop the more specific dates in "launched_at" and "deadline" columns. In addition, some of the columns have redundancy with regards to project funding start and end date. Start and end month is the most balanced.
# - The names of the Kickstarters are difficult to quantify and analyze sentiment with nltk as they often contain catchy phrases or made-up words to try to catch consumers' attention, so we will drop the "name" column as well.
# - Finally, as shown above, there are 159 sub categories which is a bit excessive to analyze; but there are only 15 main categories which is good for analysis（And also our hypothesis is on main_category）. So we will drop the sub categories.

# In[30]:


df_kickstarters.drop(columns=['launched_at', 'deadline', 'name', 'sub_category'], inplace=True)


# Next, we will create a function that will change our status (successful, failed) column into binary variables, with 1.0 being successful and 0.0 being failed. We believe that doing this will make data analysis a little faster.

# In[31]:


def convert_status(label):
    if label == "successful":
        return float(1.0)
    else:
        return float(0.0)


# In[32]:


df_kickstarters['status'] = df_kickstarters['status'].apply(convert_status)


# In[33]:


df_kickstarters.head()


# Next, we will analyze the means of failed and successful kickstarts for the quantitative variables (duration, goal, blurb length, name length, start and end months, and money pledged) using the groupby function.

# In[34]:


df_grouped = df_kickstarters.groupby('status').mean()
df_grouped


# From this we get some key observations:
# - We see clearly that the goals of failed kickstarters were set exponentially higher than their successful counterparts.
# 
# - There isn't any discerinble difference between start and end times, and blurb length.
# 
# - Successful kickstarters had shorter durations
# 
# - Obviously the successful kickstarters had a much higher pledge
# 
calculate standard deviation of each factor's data(both failure and success):
# In[35]:


df_std = df_kickstarters.groupby('status').std()
df_std


# Let's take a further look into the differences in goal_usd between successful and failed

# In[36]:


my_colors = list(['r', 'b'])
df_grouped.goal_usd.plot.bar(stacked=True, color=my_colors, figsize=(10,5))
plt.title('Mean of goal_usd for Successful/Failed', fontsize=30)
plt.ylabel('goal_usd', fontsize=18)
plt.xlabel('Status', fontsize=18)


# In[37]:


fail = df_grouped.loc[0, 'goal_usd']
success = df_grouped.loc[1, 'goal_usd']
percent = ((fail - success) / success) * 100

print("Compared to the successful kickstarters, the failed kickstarters had an increase of " 
      "{0:.2f}".format(percent) + "%\nin there USD goal amount")


# As we can see, a 736.38% increase in goal_usd for the failed kickstarters is a huge difference compared to the successful kickstarters.
# 
# This clearly shows that part of what makes a successful kickstarter is likely setting a realistic goal for funding.  If people who are looking into kickstarters notice that you've set your goal for funding unreasonably high especially with respect to the details of your project, why would they waste time and effort into funding your kickstarter if they know your funding goal likely won't be met?  Perhaps it can also be an indicator that shows that you are naive to the business side of things, which can be seen as a red flag.

# In[38]:


df_success = df_kickstarters[df_kickstarters['status'] == 1 ]
df_fail = df_kickstarters[df_kickstarters['status'] == 0 ]

                  #len(df.goal_usd.unique())


# In[39]:


df_kickstarters.boxplot(column=['goal_usd'],by='status',showfliers=False)


# It seems that the distributions are too nonnormal for statistical tests to work effectively. So instead, we decided to group the data by state and take the mean of the data by state to be analyzed.

# In[40]:


## Get statistical data from each state
state_describe = df_kickstarters.groupby('state').describe()
state_describe


# In[41]:


state_describe_succ = df_successful.groupby('state').describe()
state_describe_succ


# In[42]:


state_describe_fail = df_failed.groupby('state').describe()
state_describe_fail


# We will now create plots of the mean durations, grouped by state.

# In[43]:


plt.figure(figsize=(20,8))
plt.title('Distributions of average duration grouped by state')
plt.ylabel('proportion')

sns.distplot(state_describe_succ['duration']['mean'],color='green')
sns.distplot(state_describe_fail['duration']['mean'],color='red')


# Visually, there appears to be a significant difference in distributions; we will use a t-test to confirm.

# In[44]:


stats.ttest_ind(state_describe_succ['duration']['mean'],state_describe_fail['duration']['mean'])


# The p-value is much less than alpha value of 0.05; we can thus see that durations of Kickstarters is an important determinant, with failed kickstarters usually taking longer.

# Next we will compare the distributions of the average start and end months grouped by state.

# In[45]:


plt.figure(figsize=(20,8))
plt.title('Distributions of average start_month grouped by state')
plt.ylabel('proportion')

sns.distplot(state_describe_succ['start_month']['mean'],color='green')
sns.distplot(state_describe_fail['start_month']['mean'],color='red')


# In[46]:


plt.figure(figsize=(20,8))
plt.title('Distributions of average end month grouped by state')
plt.ylabel('proportion')

sns.distplot(state_describe_succ['end_month']['mean'],color='green')
sns.distplot(state_describe_fail['end_month']['mean'],color='red')


# There doesn't seem to be much visual difference in these distributions; we ran t-tests to corroborate our visual conclusions.

# In[47]:


stats.ttest_ind(state_describe_succ['start_month']['mean'],state_describe_fail['start_month']['mean'])


# In[48]:


stats.ttest_ind(state_describe_succ['end_month']['mean'],state_describe_fail['end_month']['mean'])


# Indeed, the t-test of distributions of average start and end months grouped by state did not output p-values less than 0.05 and thus the start and end months of Kickstarters don't seem to affect status significantly.

# Lastly, we will test which states Kickstarters are most likely to achieve success in.

# In[49]:


plt.figure(figsize=(20,8))
plt.title('Count of numbers of Kickstarters per state')
plt.ylabel('proportion')

ax_state = sns.countplot(x='state',hue='status',data=df_kickstarters)


# And a plot of proportions:

# In[50]:


df_state = df_kickstarters.groupby(['status','state'])['status'].count().unstack('state').fillna(0)
sub_df_state = np.transpose(df_state.div(df_state.sum()))
sub_df_state.plot(kind='bar',stacked=True,rot=0, figsize=(25,10))

plt.legend(('failed','successful'), loc='center left', bbox_to_anchor=(1.0, 0.5))


# # Data Analysis Summary

# #### 1.) Duration
# - It appears that if your project goes beyond 32 days you have a very high likelihood of having a failed     kickstarter
# - For successful kickstarters success is determined before the 32 day mark
# - The average duration for successful kickstarters is ~30, while the average duration for the failed kickstarters is ~34.  The std deviation for successful and failed kickstarters is 10, and 12
#   
# #### 2.) USD_Goal
# - The difference in the total USD goal for failed/kickstarters is massive.  There is an 736.38% increase in goal_usd for the failed kickstarters compared to successful
# - Failed kickstarters have a average goal of about \\$81,020
# - Successful kickstarters have an average goal of about \\$9380
# - Why the stark difference?  Possibly due to reasonable goals/expectations, a certain level of preparedness and experience.  It probably also matters when someone is deciding whether or not they will pledge to the cause
# 
# #### 3.) Categories -- Listed below are the top 4 successful categories
# - Dance has a much lower number of kickstarters at 3,092 (lowest of the top 4).  However, they also have the highest success rate at 86%
# - Comics has a total of 5,921 kickstarters (3rd in terms of total kickstarters) with a success rate of 84%
# - Publishing has the second greatest number of kickstarters with a total of 13,590 with a success rate of 74% (which is the 3rd highest success rate)
# - Music has the greatest number kickstarters at 20,491, and alternatively it has the 4th highest success rate of 70% which is nothing to scoff at
# 
# #### 4.) Start/end month
# - Based on the observations we noticed that you're in trouble if your project starts later than October, such as November or December. You're lowering your chances of success by a large margin.  At the same time when we compared start time to end time, the end time of January and early February also has a lowered chance of success which is consistent with our obvservation for start time.  Since on average duration is about a month, the detrimental effects of starting in November/Decmeber are observed in the end time success of January the next year.

# # Ethics & Privacy

# We must decide if Kickstarter and crowdfunding should only be used to fund a project’s minimum requirements or whether these “above and beyond” moments of success should be allowed and celebrated, and we must also decide if Kickstarter’s essential nature is to allow unestablished artists and creators to find success or if people like Braff should be allowed  to use the service despite their previous success.
# 
# Unique from other creators, Kickstarter creators have a preexisting obligation to their consumers to deliver a certain amount of quality, because many of their consumers will have already paid money and will have a certain expectation for what will be delivered. Does the artist’s vision suffer when they are encouraged to meet a certain expectation? If so, is it okay if their vision is changed to please  their backers, who funded the actual creation? Crowdsourcing offers an interesting dilemma, and begs the question: is the essential nature of creation to please consumers even if some artistic vision is lost, or is it to allow the artist absolute freedom in their creation?
# 
# Considering using this dataset which is showing the results from each kickstarter projects, then it could be another ethical problem that we are using their information. Although this dataset does not consist of any information regarding to neither personal nor confidential, there is a way to track which project was successful by looking and analyzing all the information here; it could be a risk of revealing personal information as well.

# # Conclusion & Discussion

# Through our analysis, we found that “music”,”film & video”, and “publishing” have the most common for kickstarter projects’ main categories. Although these main categories are quite common, it did not mean that they have the highest rates of getting better successful rates. From our data visualization, we have found that the category with the most successful kickstarters were dance, publishing, and comics in that order. Although dance had the least amount of kickstarter projects, it still had the highest success rate, compared to technology, which was one of the larger numbers kickstarter projects but was still one of the lower success rate category. 
# 
# In addition, we have also found that duration and USD goals does indeed have an effect on the success and failure of the kickstarter projects, which supports our hypothesis. We have found that projects within 32 days have a higher success rate and failed projects usually had a longer duration. We have also found that projects with smaller amount of USD goals tend to be more sucessful. Failed projects had an average of USD goal of 81020 dollars while successful projects had an average USD goal of 9380 dollars. 
# 
# On the other hand, we have also found that the start and end month of a project does not have an effect on the success and failure of a project. However, we did find that there are more projects that failed around the end of the year, such as starting in November and December and ending in January and February when looking at the data visualization of success and fail rates of each month but this was ratio was not significant enough for us to find that there is indeed an effect to the overall success and failure of projects. Some plausible explanation to these findings could be because backers might be more comfortable in pledging only a small amount of money and in something that they can get quickly, hence the smaller USD goal and duration of successful projects. This is only our speculation and is something that we will have to do further research to prove. 
# 
# We would like to keep in mind that our data consists of datas within the United States from 2014 to 2019. This limits our findings. For someone that wants to start a kickstarter, our findings could be useful to have a higher chance of a successful kickstarter campaign. 
# 
