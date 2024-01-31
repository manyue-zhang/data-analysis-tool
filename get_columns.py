import pandas as pd
import streamlit as st
import numpy as np
import collections  #neue bei Ralf und Petra. It is a built-in module from Python though
from datetime import date # neue bei Ralf un Petra
from errors import error_description
from comparison_matrixes import comparison_ECU_matrix,comparison_Istep_matrix
from functionalities import empty_cells,missing_columns

# FUNCTION FOR DISPLAYING A WARNING MESSAGE, IN CASE TWO COLUMNS HAVE THE SAME HEADER
def search_duplicated_columns(df):

    headers1 = df.columns.tolist()
    headers2 = pd.read_csv('Configuration/headernames.csv').iloc[:,2:6].stack().loc[lambda s: s.str.strip().ne('')].tolist()
    total_headers = headers1 + headers2
    repeated_columns = [item for item, count in collections.Counter(total_headers).items() if count > 2]

    if repeated_columns:        
        st.warning('Could not be evaluated. The following variables are duplicated in the database:', icon="⚠️")
        for i in repeated_columns:
            st.write(i)
    
    return()

# FUNCTION TO APPLY THE FUNCTIONS AND CREATE THE NEW COLUMNS IN THE DATAFRAME:
#@st.cache(allow_output_mutation=True, show_spinner=False)
def columns(df,template):
    
    missing_columns(df)      
    
    first_column = df.pop('ID')
    df.insert(0, 'ID', first_column)
    
    
    df['Ticket Passes'] = df['ID'].apply(lambda x: empty_cells(df,x)[0])
    df['Status'] = df['ID'].apply(lambda x: empty_cells(df,x)[1]).apply(lambda x: (', '.join(x))) 
    df['ECU-Matrix Compatible models']=df['ID'].apply(lambda x: comparison_ECU_matrix(df,x)[0]).apply(lambda x: (', '.join(x)))  
    df['ECU-Matrix Incompatible models']=df['ID'].apply(lambda x: comparison_ECU_matrix(df,x)[1]).apply(lambda x: (', '.join(x))) 
    
    ###############
    
    df['IStep-Matrix Compatible models']=df['ID'].apply(lambda x: comparison_Istep_matrix(df,x)[0]).apply(lambda x: (', '.join(x)))  
    df['IStep-Matrix Incompatible models']=df['ID'].apply(lambda x: comparison_Istep_matrix(df,x)[1]).apply(lambda x: (', '.join(x))) 
    
    #############
    
    df['Supplierinfo1']=df['ID'].apply(lambda x: error_description(df,x)[4])  
    df['Supplierinfo2']=df['ID'].apply(lambda x: error_description(df,x)[3]) 
    df['Verifikationsinfo']=df['ID'].apply(lambda x: error_description(df,x)[2])  
    df['Rückmeldung PbM']=df['ID'].apply(lambda x: error_description(df,x)[1])   
    df['Next Feedback']=df['ID'].apply(lambda x: error_description(df,x)[0])  
    df['Comments'] = np.nan    
    df['ID'] = df['ID'].apply(str)
    df['Creation time'] = df['Creation time'].apply(lambda x: x.strftime('%Y-%m-%d'))  
 
    df['Comments'] = str(date.today()) + ': ' + str(template) 
    
    return(df)

def email_columns(df):

    missing_columns(df)      
    
    first_column = df.pop('ID')
    df.insert(0, 'ID', first_column)
    df['Ticket Passes'] = df['ID'].apply(lambda x: empty_cells(df,x)[0])
    df['Status'] = df['ID'].apply(lambda x: empty_cells(df,x)[1]).apply(lambda x: (', '.join(x))) 
    df['ID'] = df['ID'].apply(str)

    
    return(df)
    