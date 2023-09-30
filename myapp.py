import streamlit as st
st.set_page_config(page_title="PNZ", layout="wide")

import matplotlib.pyplot as plt
import pandas as pd
from utils import extract_code_from_response
from custom_agent import customAgent
import requests
from io import BytesIO
import time
from pnz_auth import my_component

# # Create a horizontal navigation bar
# with st.container():
#     # Logo and brand name on the left
#     st.write("# Brand Name")

#     # Empty space to push buttons to the right
#     st.write("")

#     # Buttons on the right
#     button1 = st.button("Button 1")
#     button2 = st.button("Button 2")


auth_token_object = my_component()

st.title("Talk to your financial data")

# --------------------------------------------------------------------------------

# Initialize Session State variables:
if 'message' not in st.session_state:
    st.session_state.message56='To use this application, please login...'
if 'token' not in st.session_state:
    st.session_state.token={'value': None, 'expiry': None}

# --------------------------------------------------------------------------------
from utils import messageboard, check_token

base_url = 'https://pnz-ai-assistant.azurewebsites.net/'


# if st.session_state.token:
if auth_token_object["accessToken"] and auth_token_object['expiresIn'] != None:
    accessToken = auth_token_object["accessToken"]
    tokenExpiry =  int(time.time()) + auth_token_object['expiresIn']
    st.session_state.token = {'value': accessToken, 'expiry': tokenExpiry}
    st.write(auth_token_object["accessToken"],'tokenData')
    # st.write(auth_token_object)


if st.button('Get transactions'):
    if (check_token(st.session_state.token)):
            accesstoken = st.session_state.token.get('value')
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

# Accept user input
if user_input := st.chat_input("Plot a bar graph of credit and debit amount"):
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



# if settings.USE_AUTHENTICATION:
#         AUTH_LABEL = 'Authenticate'

#         label = AUTH_LABEL
#         # if (check_token(st.session_state.token)):
#         #     label = f'{st.session_state.user} ({st.session_state.email})'

#         with st.expander(label, expanded=True):
#             import component_runner
#             from component_event_handler import handle_event

#             component_runner.init(handle_event)

            # force a rerun to flip the expander label
            # just_logged_in = bool(check_token(st.session_state.token) and label == AUTH_LABEL)
            # just_logged_out = bool(not check_token(st.session_state.token) and label != AUTH_LABEL)
            # if (just_logged_in or just_logged_out):
            #     st.experimental_rerun()


# if 'history' not in st.session_state:
#         st.session_state['history'] = []

# if 'generated' not in st.session_state:
#         st.session_state['generated'] = ["Hello ! Ask me anything about 🤗"]

# if 'past' not in st.session_state:
#         st.session_state['past'] = ["Hey ! 👋"] 

#container for the chat history
# response_container = st.container()
#container for the user's text input
# container = st.container()    

# with container:
#         with st.form(key='my_form', clear_on_submit=True):
            
#             user_input = st.text_input("Query:", placeholder="Talk about your csv data here (:", key='input')
#             submit_button = st.form_submit_button(label='Send')
            
#         if submit_button and user_input:
#             output = csv_analyzer_app(user_input)
#             st.session_state['history'].append((user_input, output))
#             st.session_state['past'].append(user_input)
#             st.session_state['generated'].append(output) 
# if st.session_state['generated']:
#             with response_container:
#                 for i in range(len(st.session_state['generated'])):
#                     # output= str(i)
#                     # if type(i) !=  str:
#                     #     output = st.pyplot(i)  
#                     message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
#                     if  type (st.session_state['generated'] [i]) is str: 
#                         message(st.session_state["generated"][i], key=str(i)  , avatar_style="thumbs")
#                     else:
#                         message(st.session_state["generated"][i], key=st.pyplot(i) , avatar_style="thumbs")

# Button to generate visualization
# if st.button("Go"):
#     if user_input:
#         result = csv_analyzer_app(user_input)
#         st.session_state['history'].append((user_input, result))
#         if type(result) is str:
#              st.write(result)
#         else:
#              st.pyplot(result)  
