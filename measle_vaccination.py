#!/usr/bin/env python
# coding: utf-8

# ## Motivation for this project
# 
# **There have been a recent rise in the antivaxers in most countries but especially in the developed world, this has led to a drastic reduction in the vaccination rate in these countries.
# This therefore puts these countries at risk of outbreaks from vaccine preventable disease, one such is measles. The measles vaccine was one of the earliest vaccine to have been developed. Though it is relatively safe, there are alot of antivaxers who are against its used.**
# 
# **I find this dataset personal, as I believe that in the 21st century nobody should die of a vaccine preventable disease.**

# # Measles
# 
# This data contains the overall and measles, mumps, and rubella immunization rates for schools across the United States. Each row corresponds to one school and includes a number of variables including the latitude, longitude, name, and vaccination rates.
# 

# ## Data Dictionary
# 
# |Column    |Explanation                                                              |
# | -------- | ----------------------------------------------------------------------- |
# |index     | Index ID                                                                |
# |state     | School's state                                                          |
# |year      | School academic year                                                    |
# |name      | School name                                                             |
# |type      | Whether a school is public, private, charter                            |
# |city      | City                                                                    |
# |county    | County                                                                  |
# |district  | School district                                                         |
# |enroll    | Enrollment                                                              |
# |mmr       | School's Measles, Mumps, and Rubella (MMR) vaccination rate             |
# |overall   | School's overall vaccination rate                                       |
# |xrel      | Percentage of students exempted from vaccination for religious reasons  |
# |xmed      | Percentage of students exempted from vaccination for medical reasons    |
# |xper      | Percentage of students exempted from vaccination for personal reasons   |

# # Importing packages

# In[1]:


##Importing the needed libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import plotly.express as px
import scipy.stats as stats


# # Loading data

# In[2]:


# loading the dataset into a pandas dataFrame

df=pd.read_csv("data/measles.csv")
df


# # Data inspection

# In[3]:


df.info()


# In[4]:


df.describe()


# # Data cleaning 

# In[5]:


##Some data cleaning
df.drop(columns=['district'], inplace =True)


# In[6]:


df


# In[7]:


## Percentage of students exempted from vaccination o/a religious reasons (xrel) is made an object data type. 
df.xrel= df.xrel.astype(float)


# In[8]:


### There are some NA values in the year field. So we will drop those rows.
# df.year.isna().value_counts() ### about 4681 NA
df= df.dropna(subset=['year'])
df


# # UNIVARIATE Analysis and further cleaning and normalization of data

# In[9]:


###Univariate analysis of the various variables of interest
df.groupby('type')['overall'].count()


# In[10]:


## Visualization of the various types of schools
sns.set_theme()
df.type.value_counts().plot(kind='bar')
plt.title('Distribution of the various types of schools');


# ##  The most common type of school in the dataset is the public school as seen in the above bar chart
# 

# In[11]:


## Visualization of the cities with the most schools
df.city.value_counts().head(10).plot(kind='bar')
plt.title('Top 10 cities with the highest number schools');


# In[12]:


##Visualizing the counties with highest number of schools
df.county.value_counts().head(10).plot(kind='bar')
plt.title('Top 10 counties with the highest number schools');


# In[13]:


## Analysis the total number of students enrolled for the vaccination
df.enroll.describe()


# In[42]:


## Visualizing the distribution of the enroll column
sns.kdeplot(data=df.enroll, fill=True);


# **As shown on the above kde plot, the data is not normally distributed, skewed to the right**

# In[15]:


## Boxplot of the enroll
sns.boxplot(df.enroll);


# ### The boxplot above shows there are alot of extreme values
# 

# # Removal of outliers from the enroll column

# In[16]:


low_quantile, high_quantile=df.enroll.quantile([0.25,0.75])


# In[17]:


### Any school that enrolled students (low_quantile - 1.5 * IQR) or (high_quantile + 1.5* IQR)
IQR= high_quantile - low_quantile
lower_bound = low_quantile -1.5* IQR
upper_bound = high_quantile + 1.5*IQR
lower_bound
upper_bound


# In[18]:


## Removal the schools from the datasets ( from a copy of the dataset)
df1= df.copy()


# In[19]:


df1 = df1.drop(df1[df1['enroll'] < lower_bound].index)


# In[20]:


df1=df1.drop(df1[df1['enroll'] >upper_bound].index)
# df1


# In[41]:


## kde of the transformed data
sns.kdeplot(data=df1.enroll, fill=True);


# **The above kdeplot is a little normalized compared to previous before the removal of the extreme values**

# In[22]:


## Boxplot of the transformed values 
sns.boxplot(df1.enroll);


# **The boxplot still shows some extreme values, but this is better the previous data**

# In[40]:


## Visualizing the distribution of the mmr data
sns.kdeplot(df1.mmr, fill=True); 


# In[39]:


## Visualizing the distribution of the overall vaccination rate 
sns.kdeplot(df1.overall, fill=True);


# ## As shown above the both overall and MMR vaccination rate have a bimodal distribution pattern, with a peak around -1 and 100

# In[25]:


### Dataframe that contains students who were exempted from vaccinantion o/a religious reasons
df_xrel=df1[df1.xrel.notna()]
df_xrel['state'].value_counts().plot(kind='bar')
plt.title('States that exempted students from vaccination for religious reason');


# In[26]:


### Dataframe that contains students who were exempted from vaccination o/a medical reasons
df_xmed =df1[df1.xmed.notna()]
df_xmed['state'].value_counts().plot(kind='bar')
plt.title('States that exempted students from vaccination for medical reasons');


# In[27]:


### Dataframe that contains students who were exempted from vaccination o/a personal reasons
df_xper =df1[df1.xper.notna()]
df_xper['state'].value_counts().plot(kind='bar')
plt.title('States that exempted students from vaccination for personal reasons');


# # Plotly map of the distribution of the various schools in the dataset

# In[28]:


# fig= px.scatter_geo(df1, lat='lat', lon ='lng', hover_name='name', color='county', scope='usa')
# fig.show()


# # 🗺️ Explore: What types of schools have the highest overall and mmr vaccination rates?

# ## Schools with the highest overall and MMR vaccination

# In[29]:


df_highest= df1[(df1['overall'] == 100) & (df1['mmr']==100)]
# df_highest


# In[30]:


df_highest['type'].value_counts().plot(kind='bar')
plt.title('Types of schools with higest overall and MMR vaccinations');


# # 📊 Visualize: Create a plot that visualizes the overall and mmr vaccination rates for the ten states with the highest number of schools.

# In[31]:


## State with the highest number of schools 
df_state=df1.groupby('state')[['state']].value_counts().head(10).sort_values(ascending=False).reset_index(name='Number of schools')
df_state


# In[32]:


sns.barplot(x='state', y='Number of schools', data=df_state, color='blue')
plt.xticks(rotation=45)
plt.xlabel('State')
plt.title('Top 10 states with the highest number schools');


# In[33]:


## Subsetting data from the total dataset where state have some of the highest number of schools
df_stat=df[df['state'].isin(df_state.state)]


# In[34]:


fig, ax= plt.subplots(figsize=(10,10))
sns.scatterplot(data= df_stat, x='overall', y='mmr', hue='state')
plt.title('Overall and MMR vaccination rate for the top 10 states with the highest number of school')
plt.legend(loc ='best', title='States');


# # 🔎 Analyze: Does location affect the vaccination percentage of a school?

# In[35]:


## There are multiple fields which give location information (state, county,city and lat&long)


# # Performing an ANOVA test

# In[36]:


## We group the data according to various state, and we take the overall vacinnation rate to 
## represent the vaccination percentage of a school
state_overall=df.groupby('state')['overall'].apply(list)
# state_overall


# In[37]:


## We take each state and it overall vaccinate rate and put it in a group
groups=[]
for item in state_overall:
    groups.append(item)


# In[38]:


# Perform ANOVA
f_value, p_value = stats.f_oneway(*groups)

# Print the results
print("F-value:", f_value)
print("p-value:", p_value)


# **There is a statistically significant association between state and overall vaccination rate of a school,as shown by the above analysis of variance**

# # Insights from the analysis
# 1. Public owned are the commonest type of schools in the dataset
# 2. Chicago has the highest number of schools 
# 3. The county with highest number schools is the Los Angeles
# 4. The California state has the highest number of schools in all the states
# 5. North Carolina state  has the highest number of students exempted from vaccination for religious reasons 
# 6. California state  has the highest number of students exempted from vaccination for genuine medical reasons
# 7. Wisconsin states is more likely to exempt students from vaccination for personal reasons, this is concerning because there could be countless reasons for which a student can be exempted from vaccination
# 8. Kindergarten schools have the highest overall and MMR vaccination compared to other school types, this is not surprising as most Kindergarten children are within the vaccination age for most vaccines
# 9. Schools in the Colorado state have the highest overall and mmr vaccinations compared to the other state, in California; there seems to be strong positive correlation between the overall vaccination rate and the mmr vaccination rate.
# 10. The state in which a school is located affects the overall vaccination rate of the school
# 
# 

# # Call to action
# The public health unit in Wiscosin should streghten the vaccination protocols in schools, as they are noted to have a very high of number students exempted from vaccination for personal reason
# Despite the California state having the highest number of schools, they did not necessarily record the highest number of overall vaccination, vaccinations campigns should be intensified in this state,as more schools means more students and therefore high chance of outbreak in the event of an outbreak, more students should be vaccinated to achieve herd immunity.
