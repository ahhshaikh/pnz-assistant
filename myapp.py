import streamlit as st
st.set_page_config(page_title="Payments NZ", layout="wide",page_icon="https://www.apicentre.paymentsnz.co.nz/static/apicentre-favicon.ico")

import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import requests
import time
import os

from utils import extract_code_from_response
from custom_agent import customAgent
from pnz_auth import my_component
from utils import check_token

st.title("Talk to your bank account")

messageboard = st.empty()
# --------------------------------------------------------------------------------

# Initialize Session State variables:
if 'token' not in st.session_state:
    st.session_state.token={'value': None, 'expiry': None}

# --------------------------------------------------------------------------------

base_url = 'https://pnz-ai-assistant.azurewebsites.net/'
# base_url = 'http://localhost:8080'

#---------------------------------------------------------------------------------

## Sidebar

with st.sidebar:

    st.sidebar.markdown("""
    <div >
        <h3 style="color: white;font-family: monospace; font-size: 1.75rem">payments<span style="color: #F8882B;font-family: monospace;font-size: 1.75rem">nz<span/></h3>
    </div>
    """, unsafe_allow_html=True)

    auth_token_object = my_component()

    if auth_token_object["accessToken"] and auth_token_object['expiresIn'] != None:
        accessToken = auth_token_object["accessToken"]
        tokenExpiry =  int(time.time()) + auth_token_object['expiresIn']
        st.session_state.token = {'value': accessToken, 'expiry': tokenExpiry}

    st.markdown("""
        <style> 
        div.stButton > button>div>p>div {
            border-color: #AFACAC;
            color:#ffffff;
        }
        .css-1v3lvwm{
            border: 1px solid #AFACAC;
        }
        </style>""", unsafe_allow_html=True)

    if st.button(":white[Get accounts and transactions data ]", type="secondary"):
        if (check_token(st.session_state.token)):
                accesstoken = st.session_state.token.get('value')
                data = {'access_token': accesstoken}
                transactions= requests.post(base_url + '/api/transaction', data=data)                
                accounts = requests.post(base_url + '/api/accounts', data=data)

                if transactions.status_code and accounts.status_code == 200:
                    
                    transactionsData = transactions.json()['transactionsData']           
                    accountsData = accounts.json()['accountsData']

                    selectedTransactionsData = [
                        {
                            'AccountId': entry['accountId'],
                            'TransactionAmount': entry['amount']['amount'],
                            'TransactionCurrency': entry['amount']['currency'],
                            'CreditDebitIndicator': entry['creditDebitIndicator'],
                            'BookingDateTime': entry['bookingDateTime'],
                            'Status': entry['status'],
                            'ValueDateTime': entry['valueDateTime'],
                            'BalanceAmount': entry['balance']['amount']['amount'],
                            'BalanceCurrency': entry['balance']['amount']['currency']
                        }
                        for entry in transactionsData
                    ]
                
                    selectedAccountsData = [
                        {
                            'AccountId': entry['accountId'],
                            'AccountCurrency': entry['currency'],
                            'AccountNickname': entry['nickname'],
                            'AccountType': entry['accountType'],
                            'AccountSubType': entry['accountSubType'],
                            'AccountName': entry['description'],                    
                        }
                        for entry in accountsData
                    ]

                    transactionsDataFrame = pd.DataFrame(selectedTransactionsData)            
                    
                    accountsDataFrame = pd.DataFrame(selectedAccountsData)

                    merged_df = transactionsDataFrame.merge(accountsDataFrame, left_on='AccountId', right_on='AccountId', how='inner')

                    merged_df.to_csv('merged_data.csv', index=False)
                    messageboard.success('Data fetched successfully', icon="🎉") 
                    time.sleep(3)
                    messageboard.empty() 
                else:                            
                    messageboard.error("Failed to fetch data, please try again", icon ='🚨') 
                    time.sleep(3)
                    messageboard.empty() 
        else:
            messageboard.warning("To use this application, please login...") 
            time.sleep(3)
            messageboard.empty() 

#---------------------------------------------------------------------------------

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def csv_analyzer_app(user_input):

    df = pd.read_csv("merged_data.csv")
    response = customAgent(user_input)
    print(response,"response")
    code_to_execute = extract_code_from_response(response)

    print(code_to_execute,"code_to_execute")       

    if code_to_execute:
        try:
            exec(code_to_execute, globals(), {"df": df, "plt": plt})        
            fig = plt.gcf() 
            buf = BytesIO()
            fig.savefig(buf, format="png")           
            return buf           
        except Exception as e:
            return (f"Error executing code: {e}")
    else:
            return response


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if type(message["content"]) is str:
            st.markdown(message["content"])
        else:            
            st.image(message["content"])  

#---------------------------------------------------------------------------------

# Accept user input
if user_input := st.chat_input("Plot a bar graph of credit and debit amount"):
    
    if not check_token(st.session_state.token):
        messageboard.warning("To use this application, please login...") 
        time.sleep(3)
        messageboard.empty() 
    elif os.stat("merged_data.csv").st_size == 0:
        messageboard.warning("Transaction and account data not found") 
        time.sleep(3)
        messageboard.empty() 
    else:
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.messages.append({"role": "user", "content": user_input}) 

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            assistant_response =  csv_analyzer_app(user_input)
            if type(assistant_response) is str:
                message_placeholder.markdown(assistant_response)
            else:
                st.image(assistant_response)    
                
        st.session_state.messages.append({"role": "assistant", "content": assistant_response}) 

