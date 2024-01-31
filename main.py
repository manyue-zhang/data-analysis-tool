# -*- coding: utf-8 -*-
"""
Authors: Miguel Gonzalez & Manyue Zhang
Cognizant Mobility AM-I5
"""

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from PIL import Image  # neue bei Ralf und Petra

from errors import error_messages
from comparison_matrixes import edit_ECU_comparison_matrix, edit_IStep_comparison_matrix
from displayed_results import graphics, statistics
from functionalities import (
    headers,
    to_excel,
    empty_cells,
    renaming_columns,
    show_filters,
    change_filter_template,
    send_mail,
    
)
from get_columns import search_duplicated_columns, columns,email_columns


def initial():
    hide_st_style = """
                <style>               
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    img = Image.open("./logocognizant.png")
    st.sidebar.image(img)

    uploaded_file = st.sidebar.file_uploader(
        label="Upload the Octane input database:", type=["csv", "xlsx"]
    )
    df = pd.DataFrame()

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

        except Exception:
            df = pd.read_excel(uploaded_file)

    return df


def main():
    st.set_page_config(
        page_title="Octane Analysis Tool", page_icon=":bar_chart:", layout="wide"
    )
    st.title("Octane Analysis Tool")
    # Read the uploaded file (if uploaded)
    df = initial()
    # Rename the columns, if the default column header was changed
    renaming_columns(df)
    # Display an error message in case that there are 2 columns with the same header
    search_duplicated_columns(df)

    # Implement all 5 checkboxes
    evaluation_checkbox = st.sidebar.checkbox("Evaluate")
    statistics_checkbox = st.sidebar.checkbox("Show Statistics")
    graphics_checkbox = st.sidebar.checkbox("Show Graphics")
    ECU_matrix_checkbox = st.sidebar.checkbox("ECU Comparison Matrix")
    Istep_matrix_checkbox = st.sidebar.checkbox("I-Step Comparison Matrix")
    headers_checkbox = st.sidebar.checkbox("Headers Naming")
    filters_checkbox = st.sidebar.checkbox("Column filters template")
    mail_checkbox = st.sidebar.checkbox("Send E-mails")

    # Case 1: "Evaluate" checkbox is activated
    if evaluation_checkbox:
        try:
            template = st.text_input(
                "Enter the text you would like to see in the comments column (the current date will be automatically added): ",
                "",
            )
            df2 = columns(df, template)

            # ADD HERE THE FILTERED COLUMNS

            st.write("Hint: use the right button to download/export the database")
            change_filter_template(df2)

            # Activate this button for downloading the whole df:
            # st.download_button("Download table", df.to_csv(),file_name='output_table.csv',mime='text/csv')

        except Exception:
            st.warning(
                "Please upload a correct database in order to display the evaluation",
                icon="⚠️",
            )
            error_messages(df)

    # Case 2: "Show Statistics" checkbox is activated
    if statistics_checkbox:
        try:
            df["Ticket Passes"] = df["ID"].apply(lambda x: empty_cells(df, x)[0])
            df_xlsx = to_excel(df)
            st.download_button(
                label="📥 Download Statistics", data=df_xlsx, file_name="statistics.xlsx"
            )
            statistics(df)

        except:
            st.warning(
                "Please upload a database in order to display the statistics", icon="⚠️"
            )

    # Case 3: "Show Graphics" checkbox is activated
    if graphics_checkbox:
        try:
            df["Ticket Passes"] = df["ID"].apply(lambda x: empty_cells(df, x)[0])
            graphics(df)

        except:
            st.warning(
                "Please upload a database in order to display the graphs", icon="⚠️"
            )

    # Case 4: "ECU Comparison Matrix" checkbox is activated
    if ECU_matrix_checkbox:
        try:
            st.session_state.num = pd.read_csv(
                "Configuration/ECU_Vergleichsmatrizen.csv"
            )
            cm = st.session_state.num
            edit_ECU_comparison_matrix(cm)

        except:
            st.warning("Error in the ECU comparison matrix", icon="⚠️")

    # Case 5: "I-step Comparison Matrix" checkbox is activated
    if Istep_matrix_checkbox:
        try:
            st.session_state.num = pd.read_csv(
                "Configuration/IStep_Vergleichsmatrizen.csv"
            )
            cm = st.session_state.num
            edit_IStep_comparison_matrix(cm)

        except:
            st.warning("Error in the I-Step comparison matrix", icon="⚠️")

    # Case 6: "Headers Naming" checkbox is activated:
    if headers_checkbox:
        try:
            headers()

        except:
            st.warning("the headers table could not be uploaded", icon="⚠️")

    # Case 7: "Table filters" checkbox is activated:
    if filters_checkbox:
        try:
            show_filters()

        except:
            st.warning("Error in the filters checkbox", icon="⚠️")
    
    
    # Case 8: "Send Email" checkbox is activated:
    if mail_checkbox:
        #try:
            df2 = email_columns(df)
            send_mail(df2)
### umschreiben###

        #except Exception:
            #st.warning("Please upload a correct database in order to display the evaluation",icon="⚠️",)
           # error_messages(df)

if __name__ == "__main__":
    main()
