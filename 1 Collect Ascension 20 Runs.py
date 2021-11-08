#!/usr/bin/env python
# coding: utf-8

# # Load Libraries

# In[1]:


import glob
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# display all columns
pd.options.display.max_columns = None


# # Get Multiple Json Files

# In[3]:


# get lists of multiple json files
path = ".\data_gzip" # get files in the folder
json_files = glob.glob(os.path.join(path, "*.json")) #make list of paths


# In[4]:


# see first 10 files
json_files[:10]


# # Count and Filter Multiple A20 Runs for Each Json Files

# In[5]:


# combine multiple json files into one data frame
prep_data = pd.DataFrame()
data_cnt = 0

a20_cnt = 0
a20_win =0

a0_cnt = 0
a0_win =0

a20_cnt_char = dict()
a20_win_char = dict()

a0_cnt_char = dict()
a0_win_char = dict()


cnt = 0
tot_cnt = len(json_files)


for file in json_files:
    # get counts of all attempts (all runs)
    data = pd.read_json(file)
    data_cnt = data_cnt + data.shape[0]
    cnt = cnt + 1
    
    data = pd.json_normalize(data.event)
    
    # get Ascension 0 runs atempts
    lvl = 0
    data0 = data[data.ascension_level == lvl].reset_index(drop = True)
    a0_cnt = a0_cnt + data0.shape[0]
    for i in data0['character_chosen'].tolist():
        a0_cnt_char[i] = a0_cnt_char.get(i, 0) + 1

    # get victorious on heart runs
    data0 = data0[data0.victory == True]
    data0 = data0[data0.floor_reached >= 55].reset_index(drop = True)
    a0_win = a0_win + data0.shape[0]
    for i in data0['character_chosen'].tolist():
        a0_win_char[i] = a0_win_char.get(i, 0) + 1
    
    
    # get Ascension 20 runs atempts
    lvl = 20
    data = data[data.ascension_level >= lvl].reset_index(drop = True)
    a20_cnt = a20_cnt + data.shape[0]
    for i in data['character_chosen'].tolist():
        a20_cnt_char[i] = a20_cnt_char.get(i, 0) + 1
    
    # get victorious on heart runs
    data = data[data.victory == True]
    data = data[data.floor_reached >= 55].reset_index(drop = True)
    a20_win = a20_win + data.shape[0]
    for i in data['character_chosen'].tolist():
        a20_win_char[i] = a20_win_char.get(i, 0) + 1
    
    prep_data = prep_data.append(data, ignore_index = True)
    print(str(cnt) + "/" + str(tot_cnt), sep = ' ', end = '\r', flush = True) # print dynamically
    


# # Preview of Json Files while Running

# In[6]:


prep_data.head()


# In[7]:


prep_data.columns


# # See Results

# In[8]:


print(prep_data.shape[0]) # winning a20 runs
print("total runs: {}".format(data_cnt))
print("total A20 runs: {}".format(a20_cnt))
print("total A20 runs: {}".format(a20_win))


# In[9]:


print("total A0 runs: {}".format(a0_cnt))
print("total A0 runs: {}".format(a0_win))


# **Non-Ascension Winning Percentage**
# - 1.41%

# In[10]:


(a0_win/a0_cnt)*100


# **Ascension 20 Winning Percentage**
# - 3.00% 

# In[11]:


(a20_win/a20_cnt)*100


# **3.00% Ascension 20 runs are Victorious (November 2020)** 
# 
# learn from elite players

# In[12]:


a20_cnt_char


# In[13]:


a20_win_char


# **Save Winning Runst to json and csv file**

# In[14]:


prep_data.to_json("A20runs.json")


# In[15]:


prep_data.to_csv("A20runs.csv", index = False)


# # Plot

# ## Plot Number of Winning Runs

# In[16]:


char_cnt = prep_data.groupby('character_chosen').size()
char_cnt


# In[17]:


char_cnt =char_cnt.reindex(["IRONCLAD", "THE_SILENT", "DEFECT", "WATCHER"])


# In[18]:


my_colors = ['tab:red','tab:green','tab:blue','tab:purple']  #red, green, blue, black, etc.

plt.style.use('default')

fig, ax = plt.subplots()
ax.bar(char_cnt.index, char_cnt, color = my_colors)
for i in range(len(char_cnt)):
    ax.annotate(str(char_cnt[i]), xy=(char_cnt.index[i], char_cnt[i]), ha='center', va='bottom')
ax.set_ylim([0,3000])
ax.set_ylabel("Count")
ax.set_title("Ascension 20 Victorious Runs")

plt.tight_layout()

plt.show()


# In[19]:


fig.savefig("img/A20runs.png")


# In[20]:


my_colors = ['tab:red','tab:green','tab:blue','tab:purple']  #red, green, blue, black, etc.

plt.style.use('dark_background')

fig, ax = plt.subplots()
ax.bar(char_cnt.index, char_cnt, color = my_colors, edgecolor = 'grey')
for i in range(len(char_cnt)):
    ax.annotate(str(char_cnt[i]), xy=(char_cnt.index[i], char_cnt[i]), ha='center', va='bottom')
ax.set_ylim([0,3000])
ax.set_ylabel("Count")
ax.set_title("Ascension 20 Victorious Runs")

plt.tight_layout()

plt.show()


# In[21]:


fig.savefig("img/A20runs_dark.png")


# ## Plot Ascension 20 Winning Percentage

# In[22]:


a20_cnt_char


# In[23]:


a20_win_char


# In[24]:


a20_cnt_char_pd = pd.Series(a20_cnt_char)
a20_win_char_pd = pd.Series(a20_win_char)


# In[25]:


#a20_runs_win = pd.concat([a20_cnt_char_pd, a20_win_char_pd], axis=1)
a20_runs_win_rate = (a20_win_char_pd/a20_cnt_char_pd)*100 


# In[26]:


a20_runs_win_rate = a20_runs_win_rate.reindex(["IRONCLAD", "THE_SILENT", "DEFECT", "WATCHER"])


# In[27]:


a20_runs_win_rate = a20_runs_win_rate.round(2)


# In[28]:


my_colors = ['tab:red','tab:green','tab:blue','tab:purple']  #red, green, blue, black, etc.

plt.style.use('default')

fig, ax = plt.subplots()
ax.bar(a20_runs_win_rate.index, a20_runs_win_rate, color = my_colors)
for i in range(len(a20_runs_win_rate)):
    ax.annotate(str(a20_runs_win_rate[i] ) + ' %', xy=(a20_runs_win_rate.index[i], a20_runs_win_rate[i]), ha='center', va='bottom')
ax.set_ylim([0,10])
ax.set_ylabel("Victory Percentage (%)")
ax.set_title("Ascension 20 Winning Percentage")

plt.tight_layout()

plt.show()


# In[29]:


fig.savefig("img/A20win_rate.png")


# ## Non- Ascension Run Winning Percentage

# In[30]:


a0_cnt_char_pd = pd.Series(a0_cnt_char)
a0_win_char_pd = pd.Series(a0_win_char)
a0_runs_win_rate = (a0_win_char_pd/a0_cnt_char_pd)*100 


# In[31]:


a0_runs_win_rate = a0_runs_win_rate.reindex(["IRONCLAD", "THE_SILENT", "DEFECT", "WATCHER"])


# In[32]:


a0_runs_win_rate = a0_runs_win_rate.round(2)


# In[33]:


my_colors = ['tab:red','seagreen','tab:blue','tab:purple']  #red, green, blue, black, etc.

plt.style.use('default')

fig, ax = plt.subplots()
ax.bar(a0_runs_win_rate.index, a0_runs_win_rate, color = my_colors)
for i in range(len(a0_runs_win_rate)):
    ax.annotate(str(a0_runs_win_rate[i] ) + ' %', xy=(a0_runs_win_rate.index[i], a0_runs_win_rate[i]), ha='center', va='bottom')
ax.set_ylim([0,5])
ax.set_ylabel("Win Percentage (%)")
ax.set_title("Non-Ascension Winning Percentage")

plt.tight_layout()

plt.show()


# In[34]:


fig.savefig("img/A0win_rate.png")


# In[ ]:




