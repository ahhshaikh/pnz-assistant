from langchain.agents import  AgentExecutor
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.prompts import MessagesPlaceholder
from langchain.tools import PythonAstREPLTool
import pandas as pd
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.agents.agent_toolkits.conversational_retrieval.tool import create_retriever_tool
from langchain.document_loaders.csv_loader import CSVLoader
import os
from langchain.schema.messages import SystemMessage
import streamlit as st
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

memory_key = "chat_history"
memory = ConversationBufferWindowMemory(k=4,memory_key=memory_key,return_messages=True) 
# ConversationBufferMemory(memory_key=memory_key, return_messages=True)
llm = ChatOpenAI(temperature=0,model='gpt-4-0613')
# embeddings = OpenAIEmbeddings()
# loader = CSVLoader(file_path="merged_data.csv")
# documents = loader.load()
# vectorstore = FAISS.from_documents(documents, embeddings)
# retriever_tool = create_retriever_tool(vectorstore.as_retriever(), "qualitative_search", "Search for qualitative questions about structure of csv data")

TEMPLATE = """You are a smart financial analyst who can make charts and visualizations. You are good at analyzing and answering financial questions.

    You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
    It is important to understand the attributes of the dataframe before working with it. This is the result of running `df.head().to_markdown()`

    <df>
    {dhead}
    </df>

    You are not meant to use only these rows to answer questions - they are meant as a way of telling you about the shape and schema of the dataframe.
    You also do not have to use only the information here to answer questions - you can run intermediate queries to do exporatory data analysis to give you more information as needed.
    
    You have a tool called `qualitative_search` through which you can lookup a qualitative related to the structure of csv data by name and find the records corresponding to accounts, transacations with similar accounts as the query.
    You should only really use this if your search term contains a questions asking for structure of data. Otherwise, try to solve it with code.
    
    You have a tool called `python_repl` through which you can answer question related to data analysis. Donot use it for making graphs or charts.

    For example:

    <question>What is the latest transaction?</question>
    <logic>
    Use `python_repl` as the question requires running pandas code.
    </logic>

    <question>Plot a pie chart for transactions of different accounts?</question>
    <logic>
    Use no tool just return the python code wrapped inside ```python``` when you are asked to draw/plot/visualize data for generating graph. 
    The code can be composed of multiple lines.
    Look at the structure and type of data in dataframe enclosed in <df> </df> before generating code.
    Think what the data is and how it should be transformed according to query E.g BookingDateTime and ValueDateTime need to convert into datetime format
    Use the newer version of pandas e.g dt.week is depreciated so instead use dt.isocalendar().week
    Make sure the generated code is compilable, otherwise modify it
    Rotate the x-axis date labels for readability.
    Use plt.tight_layout() to ensure the labels are not cut off if needed
    Adjust the font size of the lables to be between 11px to 13px
    Make sure the figure size is (figsize=(6, 4))
    </logic>
    
    """

def customAgent(user_query):

    class PythonInputs(BaseModel):
        query: str = Field(description="code snippet to run")

    df = pd.read_csv("merged_data.csv")

    template = TEMPLATE.format(dhead=df.head().to_markdown())

    system_message = SystemMessage(
        content=template
    )
    
    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
    )
   
    repl = PythonAstREPLTool(locals={"df": df}, name="python_repl",
                            description="Useful when you need to do data analysis it runs code and returns the output of the final line")
                            # args_schema=PythonInputs)

    tools = [repl]

    agent = OpenAIFunctionsAgent(llm=llm, prompt=prompt, tools=tools)
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, max_iterations=4, early_stopping_method="generate",memory=memory,verbose=True)
    a= agent_executor.run(user_query)
    print(a)
    return a
    
