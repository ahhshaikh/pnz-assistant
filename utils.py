import re

def extract_code_from_response(response):
    """Extracts Python code from a string response."""
    # Use a regex pattern to match content between triple backticks
    pattern = r"```python(.*?)```"
    python_code_matches = re.search(pattern, response, re.DOTALL)

    if python_code_matches:
        # Extract the matched code and strip any leading/trailing whitespaces
        return python_code_matches.group(1).strip()
    return None

import streamlit as st
import time

messageboard = st.empty()

def check_token(token):
    token_value = token['value']
    if token_value:
        token_expiry = token['expiry']

        tnow = int(time.time())
        expired = ( token_expiry - tnow) < 10

        if not expired:
            return True
        else:
            st.session_state.token['value'] = None
            return False