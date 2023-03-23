import pandas as pd
import streamlit as st 
# import numpy as np
from statsmodels.regression.linear_model import OLSResults
model = OLSResults.load(r"C:\Users\hp\Downloads\1111\Allot\plastic\Deployment\model.pickle")
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


def main():
    
    st.title("Forecasting")
    st.sidebar.title("Forecasting")

    # st.radio('Type of Cab you want to Book', options=['Mini', 'Sedan', 'XL', 'Premium', 'Rental'])
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Forecasting </h2>
    </div>
    
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    st.text("")
    

    uploadedFile = st.sidebar.file_uploader("Choose a file" ,type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    if uploadedFile is not None :
        try:

            data=pd.read_csv(uploadedFile,  index_col=0)
        except:
                try:
                    data = pd.read_excel(uploadedFile,  index_col=0)
                except:      
                    data = pd.DataFrame(uploadedFile)
                
    else:
        st.sidebar.warning("you need to upload a csv or excel file.")
    
    
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <p style="color:white;text-align:center;">Add DataBase Credientials </p>
    </div>
    """
    st.sidebar.markdown(html_temp, unsafe_allow_html = True)
            
    user = st.sidebar.text_input("user", "Type Here")
    pw = st.sidebar.text_input("password", "Type Here")
    db = st.sidebar.text_input("database", "Type Here")
    
    
    if st.button("Predict"):
        engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/{db}")
        
        
        ###############################################
        st.subheader(":red[Forecast for Test data]", anchor=None)
         
        forecast_test = pd.DataFrame(model.predict(data))
        results = pd.concat([data,forecast_test], axis=1)
        results = results[['quantity',0]]
        results.rename({0: 'Forecasted_quantity'}, axis = 1, inplace = True)
        results.to_sql('forecast_results', con = engine, if_exists = 'replace', index = False, chunksize = 1000)
        
        import seaborn as sns
        cm = sns.light_palette("blue", as_cmap=True)
        st.table(results.style.background_gradient(cmap=cm).set_precision(2))
        
        ###############################################
        st.text("")
        
        ###############################################
        st.text("")
       
        # data.to_sql('forecast_pred', con = engine, if_exists = 'replace', chunksize = 1000, index = False)
        # #st.dataframe(result) or
        # #st.table(result.style.set_properties(**{'background-color': 'white','color': 'black'}))
                           
        # import seaborn as sns
        # cm = sns.light_palette("blue", as_cmap=True)
        # st.table(result.style.background_gradient(cmap=cm).set_precision(2))

                           
if __name__=='__main__':
    main()


