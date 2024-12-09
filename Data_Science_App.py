import streamlit as st 
import numpy as np 
import pandas as pd
import seaborn as sns
import plotly.express as px
st.set_page_config("Data Science App")
st.title(':rainbow[Data Science App]')
with st.sidebar:
    uploaded_file = st.file_uploader(":blue[Upload Your file here:]",type = ['csv','xls'])
    # file_name = uploaded_file.name
    process =  st.button("Process")
# if process:
if uploaded_file:
    if (uploaded_file.name.endswith('csv')):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # st.dataframe(df)
    df.info()
    st.subheader(":blue[Basic Information about your data]",divider='blue')
    with st.expander('Open'):
        # st.subheader()
        tab1,tab2,tab3,tab4 = st.tabs(['Summary','Top and Bottom Rows', 'Data Types','Columns'])
        with tab1:
            st.write(f'There are :red[{df.shape[0]}] rows and  :red[{df.shape[1]} ] columns in your data set')
            st.subheader(':gray[Statistical summary of the dataset]')
            st.dataframe(df.describe())
        with tab2:
            st.subheader(":gray[Top Rows]")
            top_rows = st.slider('Number of top rows.',1,df.shape[0])
            st.dataframe(df.head(top_rows))

            st.subheader(':gray[Bottom Rows]')
            bottom_rows = st.slider("Number of Bottom rows.",1,df.shape[0])
            st.dataframe(df.tail(bottom_rows))


        with tab3:
            st.subheader(":gray[Data types of columns]")
            st.write(list[df.dtypes])


        with tab4:
            st.subheader(":gray[Column names of the data set]")
            st.write(list[df.columns])

    st.subheader(":blue[Column valus to count]",divider='blue')
    with st.expander('Value Count'):
        col1,col2 = st.columns(2)
        with col1:
            column = st.selectbox("Choose Column name",options=list(df.columns))
        with col2:
            toprows = st.number_input("Top rows",min_value=10,step=1)

        count_button = st.button(":blue[Count]")
        
        if count_button:
            result = df[column].value_counts().reset_index(name='Counts').head(toprows)
            st.dataframe(result)
    
            st.subheader('Visualiztion',divider = 'blue')
            if not result.empty:
                fig = px.bar(data_frame = result ,x = column,y = 'Counts',text= 'Counts',template='plotly_white')
                st.plotly_chart(fig)
            
            fig = px.area(data_frame=result,x = column,y = 'Counts')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names = column,values='Counts',template='plotly_dark')
            st.plotly_chart(fig)
    
    st.subheader(':blue[Groupby: Simplify your data analysis]')
    st.write("The groupby lets you summarize data by specific categoris and groups.")
    with st.expander("Group by your columns"):
        col_one,col_two,col_three = st.columns(3)
        with col_one:
            groupby_cols = st.multiselect("Choose your column to groupby",options=list(df.columns))
        
        with col_two:
            operation_col = st.selectbox("Choose column for opretion",options=list(df.columns))
        
        with col_three:
            operation = st.selectbox("Choose operation",options=['sum','max','min','mean','median','value_counts'])
        
        if groupby_cols:
            result = df.groupby(groupby_cols).agg(
                counts = (operation_col,operation)
            ).reset_index()
            st.dataframe(result)
            # st.write(result)
            # st.write(result.columns)
            # st.write(result.counts)

            st.subheader(':blue[Data Visualization]')
            graphs = st.selectbox('Choose your graphs',options=['line','bar','scatter','pie','sunburst'])
            if graphs == 'line':
                x_axis = st.selectbox('Choose x-axis',options=list(result.columns))
                y_axis = st.selectbox('Choose y-axis',options=list(result.columns))
                color = st.selectbox("Color information",options=[None] + list(result.columns))
                fig = px.line(data_frame=result,x = x_axis,y = y_axis,color=color , markers='o',template='plotly_dark',text = 'counts')
                st.plotly_chart(fig)
            elif graphs == 'bar':
                x_axis = st.selectbox('Choose x-axis',options=list(result.columns))
                y_axis = st.selectbox('Choose y-axis',options=list(result.columns))
                color = st.selectbox("Color information",options=[None] + list(result.columns))
                facet_col = st.selectbox('Column Information',options= [None] + list(result.columns))
                fig = px.bar(data_frame=result,x = x_axis,y = y_axis,color=color , facet_col=facet_col,barmode='group',template='plotly_dark',text = 'counts')
                st.plotly_chart(fig)
            elif graphs == 'scatter':
                x_axis = st.selectbox('Choose x-axis',options=list(result.columns))
                y_axis = st.selectbox('Choose y-axis',options=list(result.columns))
                color = st.selectbox("Color information",options=[None] + list(result.columns))
                size = st.selectbox('Column size',options= [None] + list(result.columns))
                fig = px.scatter(data_frame=result,x = x_axis,y = y_axis,color=color ,size = size,template='plotly_dark')
                st.plotly_chart(fig)
            elif graphs == 'pie':
                values = st.selectbox('Select values',options= list(result.columns))
                names = st.selectbox('Select label',options=list(result.columns))
                fig = px.pie(data_frame=result,values=values,names=names,template='plotly_dark')
                st.plotly_chart(fig)
            elif graphs == 'sunburst':
                path = st.multiselect('Select your path',options=list(result.columns))
                fig = px.sunburst(data_frame=result,path = path,values='counts',template='plotly_dark')
                st.plotly_chart(fig)

