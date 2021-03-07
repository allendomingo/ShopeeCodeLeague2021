#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_json (r'input_path')


# In[3]:


df


# In[4]:


# df.loc[(df['Email'] == 'gkzAbIy@qq.com')].values


# In[5]:


total_rows = df.shape[0]
# print(total_rows)


# In[6]:


df['OrderId'].replace('', np.nan, inplace=True)
df['Email'].replace('', np.nan, inplace=True)
df['Phone'].replace('', np.nan, inplace=True)


# In[7]:


df = pd.read_json (r'input_path')
df['OrderId'].replace('', np.nan, inplace=True)
df['Email'].replace('', np.nan, inplace=True)
df['Phone'].replace('', np.nan, inplace=True)

# Cleans OrderId with null values
df_drop_orderId = df
df_drop_orderId.dropna(subset=['OrderId'], inplace=True)
# df_drop_orderId


# In[8]:


df = pd.read_json (r'input_path')
df['OrderId'].replace('', np.nan, inplace=True)
df['Email'].replace('', np.nan, inplace=True)
df['Phone'].replace('', np.nan, inplace=True)

# Cleans Email with null values
df_drop_email = df
df_drop_email.dropna(subset=['Email'], inplace=True)
# df_drop_email


# In[9]:


df = pd.read_json (r'input_path')
df['OrderId'].replace('', np.nan, inplace=True)
df['Email'].replace('', np.nan, inplace=True)
df['Phone'].replace('', np.nan, inplace=True)

# Cleans Phone with null values
df_drop_phone = df
df_drop_phone.dropna(subset=['Phone'], inplace=True)
# df_drop_phone


# In[10]:


# Get list of duplicates by OrderID
df_drop_orderId_duplicate_list = df_drop_orderId[df_drop_orderId.duplicated('OrderId', keep=False)].groupby('OrderId')['Id'].apply(list).reset_index()
df_drop_orderId_duplicate_contacts_list = df_drop_orderId[df_drop_orderId.duplicated('OrderId', keep=False)].groupby('OrderId')['Contacts'].apply(list).reset_index()
# df_drop_orderId_duplicate_contacts_list


# In[11]:


# Get list of duplicates by Email
df_drop_email_duplicate_list = df_drop_email[df_drop_email.duplicated('Email', keep=False)].groupby('Email')['Id'].apply(list).reset_index()
df_drop_email_duplicate_contacts_list = df_drop_email[df_drop_email.duplicated('Email', keep=False)].groupby('Email')['Contacts'].apply(list).reset_index()
# df_drop_email_duplicate_contacts_list
# df_drop_email_duplicate_list


# In[12]:


# Get list of duplicates by Phone
df_drop_phone_duplicate_list = df_drop_phone[df_drop_phone.duplicated('Phone', keep=False)].groupby('Phone')['Id'].apply(list).reset_index()
df_drop_phone_duplicate_contacts_list = df_drop_phone[df_drop_phone.duplicated('Phone', keep=False)].groupby('Phone')['Contacts'].apply(list).reset_index()
df_drop_phone_duplicate_contacts_list
# df_drop_phone_duplicate_list


# In[13]:


# Take note of relatives from OrderId
# print(df_drop_orderId_duplicate_list)
ID_map = []
total = []
df = pd.read_json (r'input_path')
# print(total_rows - 1)
for x in range(total_rows - 1):
    ID_map.append([str(x)])
#     print(df.iloc[x].values[3])
    total.append(df.iloc[x].values[3])
total_rows_orderId = df_drop_orderId_duplicate_list.shape[0]
# print(total_rows_orderId)
for i in range(total_rows_orderId):
    arr = df_drop_orderId_duplicate_list.iloc[i].Id
    arr_cont = df_drop_orderId_duplicate_contacts_list.iloc[i].values[1]
#     print(arr_cont)
    for j in range(len(arr) - 1):
        for k in range(j + 1, len(arr) - 1):
            ID_map[arr[j]].append(str(arr[k]))
            ID_map[arr[k]].append(str(arr[j]))
            total[arr[j]] += arr_cont[k]
            total[arr[k]] += arr_cont[j]
            
# print(ID_map)
# print(test)
        


# # Take note of relatives from Email
# 
# total_rows_email = df_drop_email_duplicate_list.shape[0]
# # print(total_rows_orderId)
# for i in range(total_rows_email):
#     arr = df_drop_email_duplicate_list.iloc[i].Id
#     for j in range(len(arr) - 1):
#         for k in range(j + 1, len(arr) - 1):
#             if (arr[k] not in ID_map[arr[j]]):
#                 ID_map[arr[j]].append(arr[k])
#             if (arr[j] not in ID_map[arr[k]]):
#                 ID_map[arr[k]].append(arr[j])
# print(ID_map)
#                 

# In[14]:


# Take note of relatives from Email
# print(total_rows - 1)
total_rows_email = df_drop_email_duplicate_list.shape[0]
# print(total_rows_orderId)
for i in range(total_rows_email):
    arr = df_drop_email_duplicate_list.iloc[i].Id
    arr_cont = arr_cont = df_drop_email_duplicate_contacts_list.iloc[i].values[1]
#     print(arr)
    for j in range(len(arr) - 1):
#         print(j)
        for k in range(j + 1, len(arr) - 1):
            if (str(arr[k]) not in ID_map[arr[j]]):
                ID_map[arr[j]].append(str(arr[k]))
                total[arr[j]] += arr_cont[k]
            if (str(arr[j]) not in ID_map[arr[k]]):
                ID_map[arr[k]].append(str(arr[j]))
                total[arr[k]] += arr_cont[j]
            
# print(ID_map)


# In[15]:


# Take note of relatives from Phone

total_rows_phone = df_drop_phone_duplicate_list.shape[0]
# print(total_rows_orderId)
for i in range(total_rows_phone):
    arr = df_drop_phone_duplicate_list.iloc[i].Id
    arr_cont = arr_cont = df_drop_phone_duplicate_contacts_list.iloc[i].values[1]
    for j in range(len(arr) - 1):
        for k in range(j + 1, len(arr) - 1):
            if (str(arr[k]) not in ID_map[arr[j]]):
                ID_map[arr[j]].append(str(arr[k]))
                total[arr[j]] += arr_cont[k]
            if (str(arr[j]) not in ID_map[arr[k]]):
                ID_map[arr[k]].append(str(arr[j]))
                total[arr[k]] += arr_cont[j]
                
# print(ID_map)
print(total)


# In[19]:


data = []
for x in range(len(total)):
    ID_string = '-'.join(ID_map[x])
    data.append([x, ID_string + ', ' + str(total[x])])

df = pd.DataFrame(data, columns = ['ticket_id','ticket_trace/contact'])    
df


# In[22]:


# df.to_csv('output_path', index=False)


# In[ ]:




