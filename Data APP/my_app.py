# IMPORTING REQUIRED LIBRARIES
import pandas as pd
import plotly.express as px
import streamlit as st 

st.set_page_config(page_title="1403 Analytics Portal",
                   page_icon="📈")
st.title(':rainbow[Data Analytics Portal]',)
st.subheader(":gray[Find Your Data Insights]",divider="rainbow")

file = st.file_uploader("Drop CSV or Excel File",type=["csv","xlsx"])
if file is not None:
    if (file.name.endswith("csv")):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.dataframe(data)
    st.info("Uploaded Successfully",icon="🚨")

    st.subheader(":rainbow[Basic Information of Dataset]",divider="rainbow")
    tab1,tab2,tab3,tab4 = st.tabs(["Summary","Top and Bottom Rows","Data Types","Columns"])

    with tab1:
        st.write(f"There are {data.shape[0]} rows in data set and {data.shape[1]} columns in dataset.")
        st.subheader(":gray[Statstical Summary of Dataset]")
        st.dataframe(data.describe())

    with tab2:
        st.subheader(":gray[Top Rows]")
        toprows = st.slider("Number of rows you want",1,data.shape[0],key="Top slider")
        st.dataframe(data.head(toprows))
        st.subheader(":gray[Bottom Rows]")
        bottomrows = st.slider("Number of rows you want",1,data.shape[0],key="Bottom Slider")
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(":gray[Data Types of Columns]")
        st.dataframe(data.dtypes)
    with tab4:
        st.subheader(":gray[Columns Information]")
        st.write(list(data.columns))

    st.subheader(":rainbow[Columns Values To Count]",divider="rainbow")
    with st.expander("Value Count"):
        col1,col2 = st.columns(2)
        with col1:
            col = st.selectbox("Choose Column Name",options=list(data.columns))
        with col2:
            top_row= st.number_input("Choose Number of Top rows",min_value=1,step=1)

        count = st.button("Count")
        if (count==True):
            result = data[col].value_counts().reset_index().head(top_row)
            st.dataframe(result)
            st.subheader("Visualization",divider="rainbow")
            fig = px.bar(data_frame=result,x=col,y="count",text="count")
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=col,y="count",text="count")
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names=col,values="count")
            st.plotly_chart(fig)
            
    st.subheader(':rainbow[Get Insights Through Groupby]',divider='red')
    with st.expander("Groupby Insights"):
        col1,col2,col3 = st.columns(3)
        with col1:
            group_by_cols =st.multiselect("Choose Desired Columns",options=list(data.columns))
        with col2:
            op_col =st.selectbox("Choose Operations Column",options=list(data.columns))
        with col3:
            op =st.selectbox("Choose Operation",options=["max","sum","min","mean","median","count"])
        if (group_by_cols):
            result = data.groupby(group_by_cols).agg(
                new_col = (op_col,op)
            ).reset_index()

            st.dataframe(result)

            st.subheader(':rainbow[Data Visualisation]',divider='red')
            graphs = st.selectbox("Choose Your Graphs",options=["line","bar","sunburst","scatter","pie"])
            if (graphs=='line'):
                x_axis = st.selectbox(" Define X-axis",options=list(result.columns))
                y_axis = st.selectbox(" Define Y-axis",options=list(result.columns))
                color = st.selectbox("Choose Color info",options=[None]+list(result.columns))
                fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)
            elif(graphs=="bar"):
                x_axis = st.selectbox(" Define X-axis",options=list(result.columns))
                y_axis = st.selectbox(" Define Y-axis",options=list(result.columns))
                color = st.selectbox("Choose Color info",options=[None]+list(result.columns))
                facet_col = st.selectbox("Column Information",options=[None]+list(result.columns))
                fig = px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode="group")
                st.plotly_chart(fig)
            elif(graphs=="scatter"):
                x_axis = st.selectbox(" Define X-axis",options=list(result.columns))
                y_axis = st.selectbox(" Define Y-axis",options=list(result.columns))
                color = st.selectbox("Choose Color info",options=[None]+list(result.columns))
                size = st.selectbox("Choose Size info",options=[None]+list(result.columns))
                fig = px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size)
                st.plotly_chart(fig)
            elif(graphs=="pie"):
                values = st.selectbox("Choose the Value",options=list(result.columns))
                names = st.selectbox("Choose Label Names",options=list(result.columns))
                fig = px.pie(data_frame=result,names=names,values=values)
                st.plotly_chart(fig)
            elif(graphs=="sunburst"):
                path = st.multiselect("Choose Your Path",options=list(result.columns))
                fig = px.sunburst(data_frame=result,path=path)
                st.plotly_chart(fig)
                

