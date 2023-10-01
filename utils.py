import re

def extract_code_from_response(response):
    """Extracts Python code from a string response."""
    
    pattern = r"```python(.*?)```"
    python_code_matches = re.search(pattern, response, re.DOTALL)

    if python_code_matches:
        return python_code_matches.group(1).strip()
    return None

import streamlit as st
import time


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