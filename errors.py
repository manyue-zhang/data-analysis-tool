import pandas as pd
import streamlit as st

# SHOW ERROR MESSAGE IN CASE THERE IS SOME BASIC HEADER MISSING
def error_messages(df):
    
    if 'Error description' not in df.columns.tolist() and not df.empty:
        st.write('The column with the header "Error description" is mandatory but it was not found in the input file')
    if 'ID' not in df.columns.tolist() and not df.empty:
        st.write('The column with the header "ID" is mandatory but it was not found in the input file')
    if 'Assigned ECU' not in df.columns.tolist() and not df.empty:
        st.write('The column with the header "Assigned ECU" is mandatory but it was not found in the input file')
    if 'Model series' not in df.columns.tolist() and not df.empty:
        st.write('The column with the header "Model series" is mandatory but it was not found in the input file')
    if 'Involved I-Step' not in df.columns.tolist() and not df.empty:
        st.write('The column with the header "Involved I-Step" is mandatory but it was not found in the input file')
    #here email
   

# FUNCTION FOR CREATING THE COLUMNS "Next Feedback" etc from "ERROR DESCRIPTION"
def error_description(df,ID):
    
    pd.set_option("display.max_colwidth", 100000)
      
    ticket = df[df['ID']==ID]  
    text=str(ticket['Error description'].replace(r'\n',' ', regex=True))
    position = text.rfind('Supplierinfo1')
    text2 = str(text[position:])
    
    try:        
        RM = text2.split("Nächste RM:",1)[1].replace("'-", "").lstrip().replace("Name: Error description, dtype: object", "")                  
    except: 
        RM = ""
        
    try:
        analysestatus = text2[text2.index("Analysestatus:") + 14: text2.index("Nächste RM")]
    except:
        analysestatus = ''
        
    try:
        verification = text2[text2.index("Verifikationsinfo:") + 18: text2.index("Analysestatus:")]
    except:
        verification =''
        
    try:
        supplierinfo2 = text2[text2.index("Supplierinfo2:") + 16: text2.index("Verifikationsinfo:")]
    except:
        supplierinfo2 =''
    
    try:    
        supplierinfo1 = text2[text2.index("Supplierinfo1:") + 16: text2.index("Supplierinfo2:")]
    except:
        supplierinfo1 =''      
                
    return(RM, analysestatus, verification, supplierinfo2, supplierinfo1)

