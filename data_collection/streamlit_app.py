import streamlit as st
from google.cloud import storage
import matplotlib.pyplot as plt
import pandas as pd
from scrape_functions import read_from_bucket, return_politician_handles

# read_from_bucket = st.cache(read_from_bucket)
return_politician_handles =  st.cache(return_politician_handles)


bucket_name = 'uk-gov-tweets-14289'
storage_client = storage.Client.from_service_account_json('/Users/mdunford/data_science/ticker-twitter/data_collection/creds.json')
bucket = storage_client.get_bucket(bucket_name)

data = read_from_bucket(bucket=bucket)
data.drop('id', axis=1, inplace=True)
data['user'] = data['user'].astype(str)

politicians = return_politician_handles(option='all')
print(politicians.sort_values(by='Screen name').head())

data = data.merge(politicians[['Name','Screen name']], how='left', left_on='user', right_on='Screen name')
print(data.sort_values(by='user').head())


# Title
st.title('UK Politics Twitter Dashboard')

# sidebar selections
party = st.sidebar.selectbox(
    'Choose political party:',
    politicians['Party'].unique()
)

selected_user = st.sidebar.selectbox(
    'Filter politician:',
    politicians[politicians['Party']==party]['Name'].unique()
)


# Bar chart of followers
st.header('Twitter followers by Party')
df = politicians.groupby('Party').sum()['Followers'].reset_index()
df = df.sort_values(by='Followers', ascending=True)
f, ax = plt.subplots()
ax.barh(y=df['Party'], width=df['Followers'])
st.pyplot(f)



# Selected user details
st.header('Tweets of chosen politician')
followers = int(politicians[politicians['Name']==selected_user]['Followers'])
change = int(politicians[politicians['Name']==selected_user]['New followers in last 24 hours'])
st.write("Selected politician: "+selected_user)
with st.container():
    st.metric(label="Followers 24hr change", value=followers, delta=change)
    st.table(data[data['Name']==selected_user][['text','created']])
