#!/usr/bin/env python
# coding: utf-8

# In[1]:


# imports
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#setting up the data and dataframes
nba_injuries_data = pd.read_csv('injuries_2010-2020.csv - Sheet1.csv')
nba_uptaded_injuries=pd.DataFrame(nba_injuries_data,columns=['Date','Team','Relinquished','Notes']).rename(columns={'Relinquished':'name'})

nba_data = pd.read_csv('player_data - Sheet1.csv')

nba_injury_data_merge = pd.merge(nba_data,nba_uptaded_injuries)
nba_injury_data_merge_no_duplicates = nba_injury_data_merge.drop_duplicates('name')


# In[3]:


#cleaning up the data
notes = []
injury_notes = []
recover_or_not = []
injury_types = []

for note in nba_injury_data_merge['Notes']:
    notes.append(note)

for injury in range(len(notes)):
    injury_note = notes[injury].split('(')
    injury_notes.append(injury_note)
    
    if len(injury_note)>1:
        recover_or_not.append(injury_note[1][:-1:])
    else:
        recover_or_not.append(injury_note[0][:-1:])
    
    injury_types.append(injury_note[0])
        
nba_injury_data_merge['Recover or Not'] = recover_or_not
nba_injury_data_merge['Injury'] = injury_types
nba_injury_data_merge
nba_updated_injury_data_merge = pd.DataFrame(nba_injury_data_merge,columns=['name','year_start','year_end','position','height','weight','birth_date','college','Date','Team','Notes','recover or not','Injury']).rename(columns={'name':'Name','year_start':'Year Start','year_end':'Year End','position':'Position','height':'height','weight':'Weight','college':'College'})
nba_updated_injury_data_merge.head(50)


# In[4]:


# Which team gets injured the most?
teams = []
teams_injury_counter = {}

for team in nba_injury_data_merge_no_duplicates['Team']:
    teams.append(team)
teams = sorted(list(set(teams)))


for team in teams:
    teams_injury_counter[team] = 0


for team in nba_injury_data_merge_no_duplicates['Team']:
       for key in teams_injury_counter:
        if team == key:
            teams_injury_counter[key]+=1
            
teams_injury_counter_values = list(teams_injury_counter.values())
teams_injury_counter_keys = list(teams_injury_counter.keys())

team_color_pallete = ['#006bb6','#e03a3e','#00788c','#00471b','#ce1141','#68122d','#008348','#1d428a','#5d76a9','#e03a3e','#98002e','#00788c','#f9a01b','#5a2b81','#f58426','#fdb927','#0077c0','#00285e','black','#e9b625','#002d62','#e31837','#1d428a','Black','#ce1141','#c4ced4','#e56020','#007ac1','#78be20','#fdb927','#002b5c']

website = 'https://encycolorpedia.com/'

sns.set(rc={'figure.figsize':(175,175)})
plt.rc('xtick',labelsize=75)
plt.rc('ytick',labelsize=150)

sns.barplot(x=teams_injury_counter_keys,y=teams_injury_counter_values,palette = team_color_pallete)
plt.yticks(np.arange(42,step=2))
plt.title("Amount of players injured per team",fontdict={'Size':200})


# In[5]:


#Which confrence gets injured the most?

east_coast_nba_teams = ['Bucks','Raptors','Celtics','Heat','Pacers','76ers','Nets','Magic','Wizards','Hornets','Bulls','Knicks','Pistons','Hawks','Cavaliers','Bobcats']
west_coast_nba_teams = ['Lakers','Clippers','Nuggets','Jazz','Thunder','Rockets','Mavericks','Grizzlies','Blazers','Pelicans','Kings','Spurs','Suns','Timberwolves','Warriors']
confrences = [east_coast_nba_teams,west_coast_nba_teams]
confrence_injury_counter_dict = {'east_coast_nba_teams_injuries':0,'west_coast_nba_teams_injuries':0}

for injury in nba_injury_data_merge_no_duplicates['Team']:
    for team in teams:
        if team in east_coast_nba_teams:
            confrence_injury_counter_dict['east_coast_nba_teams_injuries'] +=1
        else:
            confrence_injury_counter_dict['west_coast_nba_teams_injuries'] +=1

confrence_injury_counter_dict_keys = list(confrence_injury_counter_dict.keys())
confrence_injury_counter_dict_values = list(confrence_injury_counter_dict.values())

confrence_color_pallete = ['darkgreen','blue']

sns.set(rc={'figure.figsize':(10,10)})
sns.barplot(x=confrence_injury_counter_dict_keys,y=confrence_injury_counter_dict_values,palette=confrence_color_pallete)
plt.title("Which confrence gets injured more?")


# In[6]:


#Which position gets injured most?

position_injury_counter = {}
position_injury_counter_keys = position_injury_counter.keys()
position_injury_counter_values = position_injury_counter.values()

for position in nba_injury_data_merge_no_duplicates['position']:
    position_injury_counter[position] = 0
    
for injury in nba_injury_data_merge_no_duplicates['position']:
    for position in position_injury_counter:
        if injury == position:
            position_injury_counter[position] +=1

plt.pie(position_injury_counter_values,labels=position_injury_counter_keys,colors = ['green','Blue','pink','darkorange','Purple','Black','red'],shadow=True,explode=(0,0,0.05,0,0,0,0))
plt.title("Which position gets injured the most?")


# In[7]:


#Which colleges have the most injuries?

colleges = {}
for college in nba_injury_data_merge_no_duplicates['college']:
    colleges[college] = 0

for injury in nba_injury_data_merge_no_duplicates['college']:
    for college in colleges:
        if injury == college:
             colleges[college] +=1

colleges_counter = dict(Counter(colleges).most_common(15))

plt.pie(colleges_counter.values(),colors=['blue','darkblue','gold','crimson','#99badd','#000080','gray','#CC5500','orange','purple','gold','indianred','white','darkgreen','#CFB53B'])
plt.legend(colleges_counter.keys(),prop = {'size':12})
plt.title("Top 15 colleges that NBA players have gotten injured at")

