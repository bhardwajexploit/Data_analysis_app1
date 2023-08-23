import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns

@st.cache_data()
def load_data():
    return pd.read_csv('dataset/Salary.csv')

with st.spinner("loading dataset"):
    df=load_data()

st.title("MY data-science app")
st.dataframe(df)
st.header('Data visulization')
st.subheader('Top 10 jobs of the employees')
job_count=df['job_title'].value_counts().head(10)
fig1=px.bar(job_count,
            job_count.index,
            job_count.values,
            title='job title of employees')
st.plotly_chart(fig1,use_container_width=True)
st.subheader("these are the popular jobs")
st.info(';'.join(job_count.index.tolist()))
# main question from the data set
st.markdown('''
## What can we find out?
- basic categorical analysis
- salary trend on the basis of
    - year
    - experience
    - employement type
    - job title
    - location
    - company size
    - currency
- statistical analysis of diffrent category vs salary          
''')

categories = df.select_dtypes(exclude=np.number).columns.tolist()
st.success(f'There are following categories: {", ".join(categories)}')
for col in categories:
    counts = df[col].value_counts()
    if df[col].nunique() > 10:
        fig = px.bar(x=counts.index, y=counts.values, log_y=True, title=f'Distribution of {col}', text=counts.values)
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    else:
        fig = px.pie(names=counts.index, values=counts.values, title=f'Distribution of {col}')
    st.plotly_chart(fig, use_container_width=True)
st.subheader("salary trend over years ")
year_wiser_sum=df.groupby('work_year')[['salary','salary_in_usd']].sum().reset_index()
year_wiser_avg=df.groupby('work_year')[['salary','salary_in_usd']].mean().reset_index()
st.dataframe(year_wiser_sum,use_container_width=True)

fig1=px.bar(year_wiser_sum,'work_year','salary_in_usd',title='Work_year vs Salary in usd')
fig2=px.pie(year_wiser_avg,'work_year','salary_in_usd',title='Avg salaries acc to work year ')
c1,c2=st.columns(2)
st.plotly_chart(fig1,use_container_width=True)
st.plotly_chart(fig2,use_container_width=True)
c1, c2 = st.columns(2)
cats = c1.multiselect('Select categories', categories)
graphs = ['box', 'violin', 'bar polar', 'sunburst', 'treemap','line']
graph = c2.selectbox('Select graph', graphs) 

for col in cats:
    if graph == graphs[0]:
        fig = px.box(df, x=col, y='salary_in_usd', title=f'Salary distribution of {col}')
    elif graph == graphs[1]:
        fig = px.violin(df, x=col, y='salary_in_usd', title=f'Salary distribution of {col}')
    elif graph == graphs[2]:
        fig = px.line(df, x=col, y='salary_in_usd', title=f'Salary distribution of {col}')
    elif graph == graphs[3]:
        fig = px.bar_polar(df, r='salary_in_usd', theta=col, title=f'Salary distribution of {col}')
    st.plotly_chart(fig, use_container_width=True)
if graph == graphs[4]:    
    fig = px.sunburst(df, path=cats, values='salary_in_usd', title=f'Salary distribution of {col}')
if graph == graphs[5]:
    fig = px.treemap(df, path=cats, values='salary_in_usd', title=f'Salary distribution of {col}')
st.plotly_chart(fig, use_container_width=True)

            