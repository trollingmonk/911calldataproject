#!/usr/bin/env python
# coding: utf-8

# ## 911 Calls Data Project

# For this project, we will be analyzing 911 call data from https://www.kaggle.com/mchirico/montcoalert. The data contains the following fields:
# 
# * lat : String variable, Latitude
# * lng: String variable, Longitude
# * desc: String variable, Description of the Emergency Call
# * zip: String variable, Zipcode
# * title: String variable, Title
# * timeStamp: String variable, YYYY-MM-DD HH:MM:SS
# * twp: String variable, Township
# * addr: String variable, Address
# * e: String variable, Dummy variable (always 1)
# First, Please download 922.csv File
# 

# ## Data and Setup

# ____
# ** Import numpy and pandas **

# In[2]:


import numpy as np
import pandas as pd


# ** Import matplotlib.pyplot and seaborn visualization libraries and set %matplotlib inline. **

# In[3]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# ** Read in the csv file as a dataframe called df **

# In[4]:


df= pd.read_csv(r"C:\Users\R\Downloads\montcoalert\911.csv")


# ** Check the info() of the df **

# In[5]:


df.info()


# In[4]:





# ** Check the head of df **

# In[5]:





# In[6]:


df.head()


# ### Basic Questions

# ** What are the top 5 zipcodes for 911 calls? **

# In[6]:





# In[10]:


df['zip'].value_counts().head(5)


# ** What are the top 5 townships (twp) for 911 calls? **

# In[7]:





# In[11]:


df['twp'].value_counts().head(5)


# ** Take a look at the 'title' column, how many unique title codes are there? **

# In[8]:





# In[14]:


df['title'].nunique()


# ## Creating new features

# ** In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic. Use .apply() with a custom lambda expression to create a new column called "Reason" that contains this string value.** 
# 
# **For example, if the title column value is EMS: BACK PAINS/INJURY , the Reason column value would be EMS. **

# In[9]:


df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
df['Reason'].head()


# In[15]:


df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
df['Reason'].head()


# ** What is the most common Reason for a 911 call based off of this new column? **

# In[10]:





# In[16]:


df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
df['Reason'].value_counts()


# ** Now use seaborn to create a countplot of 911 calls by Reason. **

# In[11]:





# In[28]:


df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
sns.countplot(x='Reason',data=df)


# ___
# ** What is the data type of the objects in the timeStamp column? **

# In[13]:





# In[38]:


type(df.timeStamp.iloc[0])


# ** Use [pd.to_datetime](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html) to convert the column from strings to DateTime objects. **

# In[39]:


df['timeStamp'] = pd.to_datetime(df['timeStamp'])
type(df['timeStamp'].iloc[0])


# ** We can grab specific attributes from a Datetime object like -**
# 
#     time = df['timeStamp'].iloc[0]
#     time.hour
# 
# **Use .apply() Method, to create 3 new columns called Hour, Month, and Day of Week. 
# You will create these columns based off the timeStamp column.**

# In[40]:


df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)
df.head()


# ** Day of Week is an integer 0-6. Use the .map() with this dictionary to map the actual string names to the day of the week: **
# 
#     dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

# In[41]:


dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)
df.head()


# ** Use seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column. **

# In[18]:



# Relocation of the legends outside
plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0.)


# In[44]:


sns.countplot(x='Day of Week',hue='Reason',data=df)
plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0.)


# **Now do the same for Month:**

# In[19]:





# In[45]:


sns.countplot(x='Month',hue='Reason',data=df)
plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0.)


# **Create a new column called 'Date' that contains the date from the timeStamp column. You'll need to use apply along with the .date() method. ** 

# In[46]:


df['Date'] = df['timeStamp'].apply(lambda t: t.date())
df.head()


# ** Now groupby this Date column with the count() aggregate and create a plot of counts of 911 calls.**

# In[55]:


df.groupby('Date').count().plot()


# In[24]:





# In[26]:


df.groupby('Date').count()['lat'].plot()
plt.tight_layout()


# ** Now recreate this plot but create 3 separate plots with each plot representing a Reason for the 911 call**

# In[56]:


df['Reason'].unique()


# In[61]:


df[df['Reason']=='Traffic'].groupby('Date').count()['lat'].plot()
plt.title("Traffic")
plt.tight_layout()


# In[ ]:


df[df['Reason']=='Traffic'].groupby('Date').count()['lat'].plot()
plt.title("Traffic")
plt.tight_layout()


# In[62]:


df[df['Reason']=='EMS'].groupby('Date').count()['lat'].plot()
plt.title("EMS")
plt.tight_layout()


# In[63]:


df[df['Reason']=='Fire'].groupby('Date').count()['lat'].plot()
plt.title("Fire")
plt.tight_layout()


# In[30]:





# ____
# ** Let's try to create  heatmaps with seaborn and our data. But, first we will need to restructure the dataframe so that the columns become the Hours and the Index becomes the Day of the Week. 
# There are lots of ways to do this, but let's try to combine groupby with an [unstack](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.unstack.html) method. **

# In[64]:


dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack() ##Here, we can also use pivot method
dayHour


# In[77]:


df2 = df.pivot_table(index='Day of Week',columns='Hour',aggfunc='count')['Reason']
df2


# ** Now create a HeatMap using this new DataFrame. **

# In[43]:





# In[79]:


sns.heatmap(df2,cmap='coolwarm')


# ** Now create a clustermap using this DataFrame. **

# In[42]:





# In[80]:


sns.clustermap(df2,cmap='coolwarm')


# ** Now repeat these same plots and operations, for a DataFrame that shows the Month as the column. **

# In[36]:


dayMonth = df.groupby(by=['Day of Week','Month']).count()['Reason'].unstack()
dayMonth.head()


# In[84]:


df3=df.pivot_table(index='Day of Week',columns='Month',aggfunc='count')['Reason']
df3


# In[41]:





# In[86]:


sns.heatmap(df3,cmap='coolwarm')


# In[40]:





# In[87]:


sns.clustermap(df3,cmap='coolwarm')


# In[ ]:




