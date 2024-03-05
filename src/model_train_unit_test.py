from langchain_openai import ChatOpenAI
from components.backend.tools.model_trainer import ModelTrainingTool

import streamlit as st 
from langchain.agents import initialize_agent, create_openai_tools_agent
from langchain.agents import AgentExecutor
from langchain import hub
import time
import threading
import re 
import os


query = "Can you write a ai model to predict the DBH of the tree"
csv_path = '/Users/viktorciroski/Documents/Github/AI-Assistant/src/tmp/indiana_trees_remeasured.csv'
temperature=0
llm = ChatOpenAI(model_name='gpt-4', temperature=temperature, openai_api_key=os.getenv("OPENAI_KEY"))
tools = [
      ModelTrainingTool(llm=llm).initialize()
    ]

tools_agent = create_openai_tools_agent(llm, 
        tools,
        hub.pull("hwchase17/openai-functions-agent"),
        )

tools_agent = AgentExecutor(agent=tools_agent, tools=tools, verbose=True, handle_parsing_errors=True, 
        max_iterations=5)

prompt = """ 
    <system> 
    """

prompt += """ 
    IF YOU ARE ASKED ABOUT PEOPLE or SCIENTIFIC TERMS: START WITH web_search.
    FOR UNKNOWN NOUNS, NAMES AND OBJECTS: START WITH web_search and then arxiv_search.
    """
if csv_path: 
    prompt += """ 
        FOR QUESTIONS ABOUT DATA: START WITH csv_agent.
        IF YOU ARE ASKED TO VISUALIZE DATA: START WITH csv_agent, ASK IT TO MAKE A DF QUERYING COMMAND, PASS IT TO python_interpreter TO USE THE QUERY TO SAVE A VISUALIZATION. In this case, return ONLY "||{os.environ['TMP']}/*.png||". 
        IF YOU ARE ASKED TO TRAIN A MODEL: call the model_training_tool"""
    

if csv_path: 
      prompt += f""" 
    You have the following CSVs to chat with: {csv_path}
    """

prompt += """ 
    </system>
    """

prompt += f""" 
    Here is your question: <question>{query}</question> 
    
    </input>
    """

print('Prompt: \n', prompt)

#Function Call test
wb = ModelTrainingTool(llm=llm)#.initialize()
result = wb.create_model(csv_path, query)

#Agent Test
#result = tools_agent.invoke({'input': prompt.strip(), 'chat_history': []})

print(result)
