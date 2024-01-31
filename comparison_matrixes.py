import pandas as pd
import streamlit as st
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

# ECU COMPARISON MATRIX FUNCTION
def comparison_ECU_matrix(df,ID):
    
    compatible_models=[]
    incompatible_models=[]
    
    df2 = pd.read_csv('Configuration/ECU_Vergleichsmatrizen.csv')
       
    if ID in df['ID'].unique():    

        ticket = df[df['ID']==ID]        
        ECU = ticket.iloc[0]['Assigned ECU']
        models = ticket.iloc[0]['Model series'].replace(" ", "").split(",") 
        # Is this column "lead model" or "Model series"? Ask Ralf
        
        df3 = df2[df2['Mögliche assigned ECU']==ECU].drop('Mögliche assigned ECU',axis=1)
        df4 = df3[df3.columns[~df3.isnull().all()]]
        possible_models = df4.columns.values.tolist()
      
        for i in models:
            if i in possible_models:
                compatible_models.append(i)
            else:
                incompatible_models.append(i)
                
    else:
        
        print('the ID is not in the database') 
        
    return(compatible_models,incompatible_models)



# ISTEP COMPARISON MATRIX FUNCTION
def comparison_Istep_matrix(df,ID):
    
    compatible_models=[]
    incompatible_models=[]
        
    df2 = pd.read_csv('Configuration/IStep_Vergleichsmatrizen.csv')
    
    ticket = df[df['ID']==ID]
    Istep = ticket.iloc[0]['Involved I-Step']
    models = ticket.iloc[0]['Model series'].replace(" ", "").split(",") 
    
    # We discard the last part of the Istep:
    
    def Istep_reducer(Istep):
    
        sub_str = "-"
        occurrence = 3 
        # Finding 3rd occurrence of substring "-"
        val = -1
        for i in range(0, occurrence):
          val = Istep.find(sub_str, val + 1)
        Istep = Istep[:val]    
        return(Istep)
    
    
    try:
        Istep = Istep_reducer(Istep)
    except:
        st.write('Wrong format or empty cell in the column Involved I-Step for the following ID:', ID)
        
        
    df3 = df2[df2['Mögliche assigned IStep']==Istep].drop('Mögliche assigned IStep',axis=1)
    df4 = df3[df3.columns[~df3.isnull().all()]]
    possible_models = df4.columns.values.tolist()
    
    for i in models:
        if i in possible_models:
            compatible_models.append(i)
        else:
            incompatible_models.append(i)
    
    return(compatible_models,incompatible_models)


# FUNCTION FOR THE ECU COMPARISON MATRIX MODIFICATION.
def edit_ECU_comparison_matrix(cm):
    
    col1, col2 = st.columns([3,15])
       
    def update2():
        st.session_state.num.to_csv(r'Configuration/ECU_Vergleichsmatrizen.csv', index = False) 
        return()
                       
    def update3():
        st.session_state.num = pd.read_csv('Configuration/ECU_Vergleichsmatrizen_default.csv')
        st.session_state.num.to_csv(r'Configuration/ECU_Vergleichsmatrizen.csv', index = False)
        return()
                    
    def update4(column_name):
        st.session_state.num = st.session_state.num.replace(np.nan, 'novalue')
        st.session_state.num[str(column_name)] = st.session_state.num['Mögliche assigned ECU'].apply(lambda x: '' if x == 'novalue' else 'x')
        st.session_state.num = st.session_state.num.replace('novalue', '')   
        st.session_state.num.to_csv(r'Configuration/ECU_Vergleichsmatrizen.csv', index = False)
        st.session_state.num = pd.read_csv('Configuration/ECU_Vergleichsmatrizen.csv')
        return()
        
    def update5(column_name2):
        st.session_state.num.drop(str(column_name2), axis=1, inplace=True)         
        st.session_state.num.to_csv(r'Configuration/ECU_Vergleichsmatrizen.csv', index = False)
        return()
        
                               
    with col1:   
              
        st.button("📥 Save current database", on_click=update2, key='key_1')
        st.button("📥 Restore default values", on_click=update3, key='key_2')
        
        with st.form('Form1', clear_on_submit = True):
            column_name = st.text_input(label='Create new model:')                                                    
            add_column = st.form_submit_button('📥 Add new model') 
               
            if add_column:
                update4(column_name)
             
                
        with st.form('Form2', clear_on_submit = True): 
            columns3 = st.session_state.num.drop('Mögliche assigned ECU', axis=1)
            column_name2 = st.selectbox('Delete model:', columns3.columns.tolist())         
            delete_column = st.form_submit_button('📥 Delete this model')            
            
            if delete_column:                                        
                update5(column_name2)
                
           
  
    with col2:        
        gb = GridOptionsBuilder.from_dataframe(st.session_state.num)  
        gb.configure_default_column(editable=True)
        gridOptions = gb.build() 
        st.session_state.num = AgGrid(st.session_state.num, gridOptions=gridOptions, data_return_mode = DataReturnMode.AS_INPUT).data
        st.session_state.num.replace(['None'],'', inplace=True)  
    
    return()


# FUNCTION FOR THE ISTEP COMPARISON MATRIX MODIFICATION.
def edit_IStep_comparison_matrix(cm):

    col1, col2 = st.columns([3,15])
    
    def update2():
        st.session_state.num.to_csv(r'Configuration/IStep_Vergleichsmatrizen.csv', index = False) 
        return()
                       
    def update3():
        st.session_state.num = pd.read_csv('Configuration/IStep_Vergleichsmatrizen_default.csv')
        st.session_state.num.to_csv(r'Configuration/IStep_Vergleichsmatrizen.csv', index = False)
        return()
                    
    def update4(column_name):
        st.session_state.num = st.session_state.num.replace(np.nan, 'novalue')
        st.session_state.num[str(column_name)] = st.session_state.num['Mögliche assigned IStep'].apply(lambda x: '' if x == 'novalue' else 'x')
        st.session_state.num = st.session_state.num.replace('novalue', '')   
        st.session_state.num.to_csv(r'Configuration/IStep_Vergleichsmatrizen.csv', index = False)
        st.session_state.num = pd.read_csv('Configuration/IStep_Vergleichsmatrizen.csv')
        return()
        
    def update5(column_name2):
        st.session_state.num.drop(str(column_name2), axis=1, inplace=True)     
        st.session_state.num.to_csv(r'Configuration/IStep_Vergleichsmatrizen.csv', index = False)
        return()
                         
    with col1:   
              
        st.button("📥 Save current database", on_click=update2, key='key_3')
        st.button("📥 Restore default values", on_click=update3, key='key_4')
        
        with st.form('Form3', clear_on_submit = True):
            column_name = st.text_input(label='Create new model:')                                                    
            add_column = st.form_submit_button('📥 Add new model') 
               
            if add_column:
                update4(column_name)
                 
        with st.form('Form4', clear_on_submit = True): 
            columns3 = st.session_state.num.drop('Mögliche assigned IStep', axis=1)
            column_name2 = st.selectbox('Delete model:', columns3.columns.tolist())         
            delete_column = st.form_submit_button('📥 Delete this model')            
            
            if delete_column:                                        
                update5(column_name2)
           
    with col2:        
        gb = GridOptionsBuilder.from_dataframe(st.session_state.num)  
        gb.configure_default_column(editable=True)
        gridOptions = gb.build() 
        st.session_state.num = AgGrid(st.session_state.num, gridOptions=gridOptions, data_return_mode = DataReturnMode.AS_INPUT).data
        st.session_state.num.replace(['None'],'', inplace=True)  
        
    return()