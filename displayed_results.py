import plotly.graph_objects as go
import streamlit as st
from functionalities import existing_columns


# FUNCTION FOR DISPLAYING THE STATISTICS:

def statistics(df):  
    
    list2 = existing_columns(df)
    col1, col2, col3, col4 = st.columns(4)   
    lst = [col1, col2, col3, col4]
    max_length = len(list2) 
    q, r = divmod(max_length, len(lst))
    list_cols = q * lst + lst[:r]
    
       
    container1 = st.container()
            
    with container1:
        
        for i in list2:
            with list_cols[int(list2.index(i))]:
                val = df[i].value_counts(normalize=True).mul(100).round(1).rename_axis(str(i)).reset_index(name='Values (%)').astype(str)
                st.dataframe(val, height=200, width=200)              
            
    return()


# DISPLAY GRAPHICS FUNCTION:

def graphics(df):
    
    list2 = existing_columns(df)
    col1, col2 = st.columns(2)   
    lst = [col1, col2]
    max_length = len(list2) 
    q, r = divmod(max_length, len(lst))
    list_cols = q * lst + lst[:r]
    
    config = {'displaylogo': False}
    container2 = st.container()

    
    hovertemplate = "%{label}<br>%{percent}<extra></extra>"
    
    with container2:
        
        for i in list2:
            
            with list_cols[int(list2.index(i))]:
            
                val = df[i].value_counts(normalize=True).mul(100).round(1).rename_axis(str(i)).reset_index(name='Values (%)').astype(str)
                names = val.iloc[:,0]
                values = val.iloc[:,1]               
                            
                pie_fig = go.Figure(data=[go.Pie(values=values, labels=names, textinfo='percent',
                insidetextorientation='radial', showlegend=True)])
                pie_fig.update_layout(legend=dict(yanchor="top", y=1.0, xanchor="left", x=1.0, font_size=10),
                title_text=i,title_y=0.93,title_x=0.5)
                pie_fig.update_traces(marker=dict(line=dict(color='#000000', width=1)), hovertemplate = hovertemplate)
                st.plotly_chart(pie_fig, use_container_width=True, config=config)
                    
    return()

