#!/usr/bin/env python
# coding: utf-8

import os,sys
import re
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


from jupyterthemes import jtplot
jtplot.style()


## Importing Data
df=pd.read_csv('data/dummy_data.csv')
df


## Extracting Year from Dates
df['year']=df['start_date'].apply(lambda x: int(x.split('-')[0]))

## Project Count Every Year
df['year'].value_counts().sort_index()

## Project Count for each Service
df['service'].value_counts()

## Project Count for every year for each Service
df[['year','service']].groupby(['year','service']).size().reset_index(name='counts')

## Average Price for each project each year
df[['year','price']].groupby('year').mean()

## Avg Price Vs Year
f=plt.figure(figsize=(15,8))
sns.barplot(data=df,x='year',y='price')
plt.xlabel('Year')
plt.ylabel('Avg price of service offered')

## Avg Price Vs Year for each Service
f=plt.figure(figsize=(15,12))
sns.barplot(data=df,x='year',y='price', hue='service')
plt.xlabel('Year')
plt.ylabel('Average Price')
plt.legend(title='Services')

## Avg Price Vs Year for each Team
f=plt.figure(figsize=(15,12))
sns.barplot(data=df,x='year',y='price', hue='team')
handles, labels = plt.gca().get_legend_handles_labels()
legend_dict=dict(zip(labels,handles))
labels= sorted(labels)
handles=[legend_dict[label] for label in labels]
plt.xlabel('Year')
plt.ylabel('Avg price of a project')
plt.legend(handles,labels,title='Teams');

## Avg Price Vs Year for each Service
f=plt.figure(figsize=(15,12))
sns.lineplot(data=df,x='year',y='price', hue='service')
plt.xlabel('Year')
plt.ylabel('Average Price')
plt.legend(title='Services')

## Avg Price Vs Year for each Team
f=plt.figure(figsize=(15,12))
sns.lineplot(data=df,x='year',y='price', hue='team')
handles, labels = plt.gca().get_legend_handles_labels()
legend_dict=dict(zip(labels,handles))
labels= sorted(labels)
handles=[legend_dict[label] for label in labels]
plt.xlabel('Year')
plt.ylabel('Average Price')
plt.legend(handles,labels,title='Teams');

## Count of Projects for each Service
f=plt.figure(figsize=(15,8))
sns.countplot(data=df,x='service')
plt.xticks(rotation=30);
plt.xlabel('Service')
plt.ylabel('No. of Projects')

## Count of Projects for each team every year
f=plt.figure(figsize=(15,8))
sns.countplot(data=df,x='year',hue='team')
plt.xticks(rotation=30);
handles, labels = plt.gca().get_legend_handles_labels()
legend_dict=dict(zip(labels,handles))
labels= sorted(labels)
handles=[legend_dict[label] for label in labels]
plt.xlabel('Year')
plt.ylabel('No. of Projcets')
plt.legend(handles,labels,title='Teams');


## Count of Projects for each Service every year
f=plt.figure(figsize=(15,8))
sns.lineplot(data=df[['year','service']].groupby(['year','service']).size().reset_index(name='counts'),x='year',y='counts',hue='service')
plt.xlabel('Year')
plt.ylabel('No. of Projcets')
plt.legend(title='Services');

## Count of projects for each year for each service for each team
df.groupby(['year','service','team']).size().reset_index(name='counts')

## Count of project for each year for each location for each Service
pd.DataFrame(df.groupby(['year','location','service'])['proj_no'].count())

## Count of project for each location for each Service
pd.DataFrame(df.groupby(['location','service'])['proj_no'].count())

## Count of project for each year for each Service
pd.DataFrame(df.groupby(['year','service'])['proj_no'].count())

