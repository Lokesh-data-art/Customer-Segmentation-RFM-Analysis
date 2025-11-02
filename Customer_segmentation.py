#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[46]:


import os
os.environ["OMP_NUM_THREADS"] = "1"


# In[48]:


pip install --upgrade threadpoolctl


# In[2]:


df=pd.read_csv('C://Users//ACAL//Downloads//archive (50)//OnlineRetail.csv', encoding="latin1")

print(df)


# In[3]:


df=df.dropna(subset=['CustomerID'])


# In[4]:


df=df[~df['InvoiceNo'].str.startswith('C')]


# In[5]:


df=df[~df['Quantity']<0]


# In[6]:


df['InvoiceDate']=pd.to_datetime(df['InvoiceDate'])


# In[7]:


df['CustomerID']=df['CustomerID'].astype(int)


# In[8]:


print(df.head())


# In[9]:


df.to_csv('cleaned_Online_Retail.csv',index=False)


# In[10]:


import matplotlib.pyplot as plt
import seaborn as sb


# In[11]:


monthly_sales=df.groupby(df['InvoiceDate'].dt.to_period('M'))['Quantity'].sum()


# In[12]:


print(monthly_sales)


# In[13]:


monthly_sales.plot(kind='bar')
plt.title("monthly sales trend")
plt.show()


# In[14]:


sales_by_each_customer=df.groupby(df['CustomerID'])['Quantity'].sum()
print(sales_by_each_customer.sort_values(ascending=
                                         False).head(10))


# In[15]:


df['TotalPrice']=df['Quantity']*df['UnitPrice']


# In[16]:


# Reference date (e.g., one day after last invoice)
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',                                  # Frequency
    'TotalPrice': 'sum'                                      # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
rfm.head()




# In[17]:


from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])



# In[18]:


from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


inertia = []
K = range(1, 10)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(rfm_scaled)
    inertia.append(kmeans.inertia_)

plt.plot(K, inertia, 'bo-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()


# In[19]:


kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)


# In[20]:


rfm.groupby('Cluster').mean().sort_values('Recency')


# In[21]:


import seaborn as sns

sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Cluster', palette='viridis')
plt.title('Customer Segmentation (RFM Clusters)')
plt.show()


# In[22]:


rfm.to_csv('rfm_segmented_customers.csv', index=False)


# In[ ]:




