import pandas as pd
import streamlit as st
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from io import BytesIO
import urllib.parse
import webbrowser

# AG GRID FUNCTION FOR THE DATABASE:
def function_aggrid(df):
    
    gb = GridOptionsBuilder.from_dataframe(df) 
    
    if set(['Comments']).issubset(df.columns):     
        gb.configure_column('Comments',editable=True)
    
    gb.configure_side_bar() 
    
 
    if set(['Ticket Passes','ID','Assigned ECU']).issubset(df.columns):
        
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.data['Ticket Passes'] === 'yes') {
                return {
                    'color': 'black',
                    'backgroundColor': 'mediumseagreen'
                }
            } else {
                return {
                    'color': 'black',
                    'backgroundColor': 'salmon'
                }
            }
        };
        """)
        
        gb.configure_column("Ticket Passes", cellStyle=cellsytle_jscode, width=110)    
        gb.configure_column("ID", cellStyle=cellsytle_jscode, pinned='left', width=90)
        gb.configure_column("Assigned ECU", width=140)

        
             
    gridoptions = gb.build()
     
    df2=AgGrid(
        df,
        height=600, width='100%',
        gridOptions=gridoptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
        allow_unsafe_jscode=True)   
    
    return(df2)
def mail_aggrid(df1):
    
    st.session_state.mail = df1
    #st.session_state.mail = st.session_state.mail.astype(str)
    gb = GridOptionsBuilder.from_dataframe(st.session_state.mail)
    gb.configure_default_column(editable=True, cellStyle={'background': 'white'})
    st.session_state.mail.replace(['nan'],'',inplace=True) 
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    gb.configure_side_bar()
    if set(['Ticket Passes','ID']).issubset(st.session_state.mail.columns):
        
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.data['Ticket Passes'] === 'yes') {
                return {
                    'color': 'black',
                    'backgroundColor': 'mediumseagreen'
                }
            } else {
                return {
                    'color': 'black',
                    'backgroundColor': 'salmon'
                }
            }
        };
        """)
        
    gb.configure_column("Ticket Passes", cellStyle=cellsytle_jscode, width=110)    
    gb.configure_column("ID", cellStyle=cellsytle_jscode, pinned='left', width=110)

    gridOptions = gb.build()   
    response = AgGrid(
        st.session_state.mail, 
        gridOptions=gridOptions, 
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        header_checkbox_selection_filtered_only=True,
        use_checkbox=True,
        allow_unsafe_jscode=True)
    st.session_state.select_mail = response['selected_rows']
    return(st.session_state.select_mail)

def renaming_columns(df):
    
    headers = pd.read_csv('Configuration/headernames.csv', index_col = None) 
   
    # Assumption: there are 3 type of variables:
    
    # 1) Mandatory variables: the variable needs to be filled. If it is empty it would result in a ticket rejection.
    global mandatory
    #mandatory = ['Assigned ECU','Involved I-Step', 'ID','Name','Error description',
     #                'Creation time','Phase','Problem severity','Owner','Lead model','Problem finder']
     
    mandatory = ['Name','Assigned ECU','Lead model','Involved I-Step','Error description','Owner','Problem finder','ID'
                 ,'Problem Finder Team']
    
    
    # 2) Recommended variables: the variable should be filled. If it is empty, we would get a warning message in the status but would not result in a ticket rejection.
    global recommended
    #recommended = ['ECU2Modul','Found in function', 'Problem Finder', 'Reporting relevance', 'Affected Target I-Step', 'Solution Responsible', 
    #                   'Problem category', 'Days in phase', 'KIFA-comment', 'Error occurrence', 'Ticket no. supplier','Defect classification'] 
    recommended = ['Creation time','Phase','Problem severity','ECU2 Modul','Found in function', 'Reporting relevance', 
                   'Affected Target I-Step', 'Solution Responsible', 'Problem category', 'Days in phase', 'KIFA-comment', 
                   'Error occurrence', 'Ticket no. supplier','Defect classification'] 
           
    
    # 3) Free variables. They can either have a value or be empty. Basically any variable not belonging to 1 or 2
    
    total_list = mandatory + recommended + ['Visible for','Supplier transfer','Display severity','VIN','Blocking reason',
                                            'Follow-up','Lessons learned','LeLe category','LeLe responsible',
                                            'System test category','First use/SoP of function','Shift to SET',
                                            'Number of SET-Shifts']
    
    for i in range(1,6):
        
        for j in range(0,36):
            if pd.notnull(headers.iloc[j,i]):
                df.rename(columns={str(headers.iloc[j,i]): str(total_list[j])}, inplace = True) 
                
    return()

def missing_columns(df):
    
    list_columns=df.columns
    
    mandatory2=[]
    for i in mandatory:
        if i not in list_columns:
            mandatory2.append(i)
  
    recommended2=[]
    for i in recommended:
        if i not in list_columns:        
            recommended2.append(i)
                    
    return(mandatory2, recommended2)
# EMPTY CELLS FUNCTION

def empty_cells(df,ID):
    
    mandatory2=missing_columns(df)[0]
    recommended2=missing_columns(df)[1]
    
    comment=[]
    
    if ID in df['ID'].unique():
                       
        nan_values = []     
        ticket = df[df['ID'] == ID]

        nan_values = ticket.columns[ticket.isnull().any()].tolist()
     
        
        # LIST WITH EMPTY VARIABLES:        
        for i in nan_values:
            if i in mandatory:
                mandatory2.append(i) 
            elif i in recommended:
                recommended2.append(i)

        if mandatory2:
            passesvar='no'
            comment.append('The following mandatory variables are missing: ' + str(', '.join(mandatory2)))
            comment.append('The following recommended variables are missing: ' + str(', '.join(recommended2)))
        
        elif recommended2:
            passesvar='yes'
            comment.append('The following recommended variables are missing: ' + str(', '.join(recommended2)))
            
        else:   
            passesvar='yes'
            comment.append('All good')
      
        
    else:
        st.warning('the ID is not in the database', icon="⚠️")
        
    return(passesvar,comment)


# FUNCTION TO DOWNLOAD THE STATISTICS IN EXCEL FILE:

def to_excel(df):
    
    list2 = existing_columns(df)

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    for i in list2:
        if str(i) in df.columns:
            data = pd.DataFrame(df[i].value_counts(normalize=True).mul(100).round(1).rename_axis(str(i)).reset_index(name='Values (%)').astype(str))
            data.to_excel(writer, sheet_name=i, index=False)
            worksheet = writer.sheets[i]
            workbook = writer.book
            format1 = workbook.add_format({'num_format': '0.00'}) 
            worksheet.set_column('A:A', None, format1)  
            
    writer.save()
    processed_data = output.getvalue()
    
    return(processed_data)

#@st.cache

def convert_df(df):
    
    return(df.to_csv(index=False).encode('utf-8'))


# FUNCTION TO ADD HEADER NAMES TO AVOID THE PROBLEM THAT BMW CHANGES THE FORMAT/HEADER FILES

def headers():
    
    st.write('Please add possible new header names in the grey cells')
        
    col1, col2 = st.columns([1,8])
        
    def update():            
        
        coincidence = (st.session_state.headers.drop('Variable', axis=1).stack().loc[lambda s: s.str.strip().ne('')].duplicated().any()) 
              
        if coincidence:
        
            st.warning('Error. The table could not be saved. You tried to assign the same naming in two different cells', icon="⚠️")
        
        else:
            st.session_state.headers.to_csv(r'Configuration/headernames.csv', index = False) 
                
    def update2():
        st.session_state.headers = pd.read_csv('./Configuration/headernames_default.csv')
        st.session_state.headers.to_csv(r'Configuration/headernames.csv', index = False) 
        
    with col1:     
        st.button("📥 Save headers naming", on_click=update)
        st.button("📥 Restore default headers naming", on_click=update2)
        
    with col2:
        st.session_state.headers = pd.read_csv('Configuration/headernames.csv', index_col = None)
        st.session_state.headers = st.session_state.headers.astype(str)
        gb = GridOptionsBuilder.from_dataframe(st.session_state.headers)
        gb.configure_default_column(editable=True, cellStyle={'background': 'silver'})
        gb.configure_column('Variable', editable=False, cellStyle={'font-weight': 'bold','color':'red','background': 'white'}) 
        gb.configure_column('Accepted header naming 1', editable=False, cellStyle={'background': 'silver'})
        gridOptions = gb.build()   
        st.session_state.headers.replace(['nan'],'',inplace=True) 
        st.session_state.headers = AgGrid(st.session_state.headers, gridOptions=gridOptions, data_return_mode = DataReturnMode.AS_INPUT).data
             
    return()

# FUNCTION FOR TAKING ONLY THE COLUMNS THAT ARE ON THE LIST AND DISCARD THE OTHER ONES:
    
def existing_columns(df):
    
    list_total = ['Assigned ECU','Ticket Passes','Phase', 'Problem severity', 'Error occurrence',
        'Visible for','Owner', 'Supplier transfer', 'Lead model',
        'Display severity','Problem finder', 'Solution Responsible','Problem Finder Team', 'Problem category']   
       
    list2 = []
    
    for i in list_total:
        if i in df.columns:
            list2.append(str(i))
            
    return(list2)

def process_config(df2, config_name):
    df_filters = pd.read_csv('Configuration/formats.csv')
    df_filters = df_filters[['Column',config_name]].dropna()
    
    if df_filters[config_name].isnull().all():
        st.write(f'Please add values in the {config_name} Columns Filter Template')
    else:
        dictionary = dict(zip(df_filters['Column'], df_filters[config_name]))
        dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1]))
        mylist = list(dictionary.keys())
        mylist_allcolumns = list(df2.columns.values)

        common_list = list(sorted(set(mylist).intersection(mylist_allcolumns), key=lambda x:mylist.index(x)))
        df3 = df2[common_list].copy()

        uncommon_list = list(set(mylist).difference(mylist_allcolumns))
        for i in uncommon_list:
            df3[str(i)] = str('Column not found in "All Columns"')

        function_aggrid(df3)

def show_filters():

    tab1, tab2 = st.tabs(["Set Config", "Set Username"])

    with tab1:

        st.write('Please add the columns you want to filter and the positions from left (1) to right (2,3,4...)')               
        st.session_state.num = pd.read_csv(r'Configuration/formats.csv')
                              
        gb = GridOptionsBuilder.from_dataframe(st.session_state.num)
        gb.configure_column('Config A', editable=True)
        gb.configure_column('Config B', editable=True)
        gb.configure_column('Config C', editable=True)
        gb.configure_column('Config D', editable=True)
        gridOptions = gb.build()
                
        st.session_state.num = AgGrid(st.session_state.num, gridOptions=gridOptions, data_return_mode=DataReturnMode.AS_INPUT).data

               
        config_buttons = st.button('📥 Save configurations')
                        
        if config_buttons:
                            
            if st.session_state.num['Config A'].dropna().duplicated().any():
                st.write('Duplicated position, please check values')
            elif st.session_state.num['Config B'].dropna().duplicated().any():
                st.write('Duplicated position, please check values')
            elif st.session_state.num['Config C'].dropna().duplicated().any():
                st.write('Duplicated position, please check values')
            elif st.session_state.num['Config D'].dropna().duplicated().any():
                st.write('Duplicated position, please check values')
                            
            else:
                st.session_state.num.to_csv(r'Configuration/formats.csv', index = False)
                st.write('Configuration sucessfully saved!')
    with tab2:
        st.write('Please add possible new user names in the Username cells')
        st.session_state.name = pd.read_csv(r'Configuration/config_nicknames.csv')
        st.session_state.name= st.session_state.name.astype(str)
        st.session_state.name.replace(['nan'],'',inplace=True) 
        gbname = GridOptionsBuilder.from_dataframe(st.session_state.name)
        gbname.configure_column('Username', editable=True)
        gridOptionsname = gbname.build()
        st.session_state.name = AgGrid(st.session_state.name, gridOptions=gridOptionsname, data_return_mode=DataReturnMode.AS_INPUT).data
        
        configsname_buttons = st.button('📥 Save usernames')

        if configsname_buttons:
            if st.session_state.name['Username'].dropna().duplicated().any():
                st.write('Duplicated position, please check values')             
            
            else:
                st.session_state.name.to_csv(r'./Configuration/config_nicknames.csv', index = False)
                st.write('Username sucessfully saved!')
    return()

def change_filter_template(df2):
    username = pd.read_csv('./Configuration/config_nicknames.csv',usecols=[1])
    username= np.array(username.stack()).tolist()
    
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filters = st.selectbox('Which filters template would you like to use?',
                            ('All Columns', 'Config A '+' ('+username[0]+') ', 'Config B '+' ('+username[1]+') ', 
                             'Config C '+' ('+username[2]+') ','Config D '+ ' ('+username[3]+') ')) 
 
    
    if filters == 'All Columns':
        function_aggrid(df2)

    elif filters == 'Config A '+' ('+username[0]+') ':
        process_config(df2, 'Config A' )

    elif filters == 'Config B '+' ('+username[1]+') ':
        process_config(df2, 'Config B')

    elif filters == 'Config C '+' ('+username[2]+') ':
        process_config(df2, 'Config C')

    elif filters == 'Config D '+ ' ('+username[3]+') ':
        process_config(df2, 'Config D')

    return()

def process_mailconfig(df2, config_name):
    df_mail = pd.read_csv('Configuration/email.csv')
    df_filters = pd.read_csv('Configuration/email_formats.csv')
    df_filters = df_filters[['Column',config_name]].dropna()
    dictionary = dict(zip(df_filters['Column'], df_filters[config_name]))
    dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1]))
    mylist = list(dictionary.keys())
    mylist_allcolumns = list(df2.columns.values)
    common_list = list(sorted(set(mylist).intersection(mylist_allcolumns), key=lambda x:mylist.index(x)))
    df3 = df2[common_list].copy()
    uncommon_list = list(set(mylist).difference(mylist_allcolumns))
    for i in uncommon_list:
        df3[str(i)] = str('Column not found in "All Columns"')

    df3 = df3.merge(df_mail,how ='inner', on= 'Problem finder')

    mail_aggrid(df3)

    def update3():
        email_address = [entry["Problem Finder Email"] for entry in st.session_state.select_mail]
            
        if email_address:
            to_email = ",".join(email_address)
            webbrowser.open(f'mailto:{to_email}')
        else:
            st.warning("No e-mail addresses available", icon="⚠️")

    st.button("📥 Send Email", on_click=update3, key='key_2')


def send_mail(df2):
    
    tab1, tab2 = st.tabs(["Emails", "Database"])

    def update2():
        st.session_state.mail.to_csv(r'Configuration/email.csv', index = False)
        return()
    
    with tab1:

        process_mailconfig(df2, 'Config email')
        
    with tab2:
        st.write('Please add possible new Problem Finder here in the grey cells')
        st.session_state.mail = pd.read_csv(r'Configuration/email.csv')
        
        col1,col2 = st.columns([7,1])
        col3,col4 = st.columns([1,1])
        with col1:
            
            st.session_state.mail = pd.read_csv('Configuration/email.csv', index_col = None)
            st.session_state.mail = st.session_state.mail.astype(str)
            gb = GridOptionsBuilder.from_dataframe(st.session_state.mail)
            gb.configure_default_column(editable=True, cellStyle={'background': 'white'})
            st.session_state.mail.replace(['nan'],'',inplace=True) 
            gb.configure_side_bar()
            gridOptions = gb.build()   
            st.session_state.mail = AgGrid(
                st.session_state.mail, 
                gridOptions=gridOptions, 
                update_mode=GridUpdateMode.MODEL_CHANGED,
                data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                header_checkbox_selection_filtered_only=True,
                ).data

        # send Information from users    
        with col3:
            st.button("📥 Save Email", on_click=update2, key='key_1')
                 
    return()