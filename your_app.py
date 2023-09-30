import streamlit as st
st.set_page_config(page_title="PNZ", layout="wide")

import matplotlib.pyplot as plt
import pandas as pd
from utils import extract_code_from_response
from custom_agent import customAgent
import requests
from io import BytesIO
import time


st.title("Talk to your financial data")

# --------------------------------------------------------------------------------

# Initialize Session State variables:
if 'message' not in st.session_state:
    st.session_state.message='To use this application, please login...'
if 'token' not in st.session_state:
    st.session_state.token={'value': None, 'expiry': None}
if 'user' not in st.session_state:
    st.session_state.user=None
if 'email' not in st.session_state:
    st.session_state.email=None
if 'report' not in st.session_state:
    st.session_state.report=[]
# --------------------------------------------------------------------------------
from utils import messageboard, check_token

# base_url = 'http://localhost:8080'
base_url = 'https://pnz-ai-assistant.azurewebsites.net/'

def authenticate():
            tokenData = requests.get(base_url + '/api/authenticate')
            if tokenData.status_code == 200:
                tokenData = tokenData.json()
                print(tokenData)
                accessToken = tokenData['token']['accessToken']
                tokenExpiry =  int(time.time()) + tokenData['token']['expiresIn']
                print("Access Token in authneticate:", accessToken)
                st.session_state.token = {'value': accessToken, 'expiry': tokenExpiry}


if st.button('Get transactions',"getTransactions"):
    if (check_token(st.session_state.token)):
            accesstoken = st.session_state.token['value']
            print("in check", accesstoken)
            data = {'access_token': accesstoken}
            transactions= requests.post(base_url + '/api/transaction', data=data)
            accounts = requests.post(base_url + '/api/accounts', data=data)

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
    else:
            authenticate()
            accesstoken = st.session_state.token['value']
            data = {'access_token': accesstoken}
            transactions= requests.post(base_url + '/api/transaction', data=data)
            accounts = requests.post(base_url + '/api/accounts', data=data)

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
    
def csv_analyzer_app(user_input):

    df = pd.read_csv("bank.csv")
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


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if type(message["content"]) is str:
            st.markdown(message["content"])
        else:            
            st.image(message["content"])  
            # st.pyplot(message["content"],use_container_width=False)

if user_input := st.chat_input("Plot a bar graph of credit and debit amount"):
        
        if not check_token(st.session_state.token):
            alert = st.warning("Please get transactions first!") 
            time.sleep(3)
            alert.empty() 
        else:
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(user_input)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input}) 

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                assistant_response =  csv_analyzer_app(user_input)
                if type(assistant_response) is str:
                    message_placeholder.markdown(assistant_response)
                else:
                    st.image(assistant_response)    
                    # st.pyplot(assistant_response,use_container_width=False)  
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response}) 
