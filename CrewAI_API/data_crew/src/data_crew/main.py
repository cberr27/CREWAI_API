#!/usr/bin/env python
import string
import sys
import warnings
from datetime import datetime

from data_crew.src.data_crew.crew import DataCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

url = 'https://www.linkedin.com/jobs'
roles_to_search = 'Python_Developer'
total_roles_to_fetch = 12
column_names = 'Company Name, Job Title, Job Description, Responsibilities, Qualifications and Skills, Experience Required'


def change_topic(new_topic : str):
    global roles_to_search
    roles_to_search = str(new_topic)
    topic_without_spaces = ''
    for c in roles_to_search:
        if c != " ":
            topic_without_spaces += c
        else:
            topic_without_spaces += "_"
    roles_to_search = topic_without_spaces
    return roles_to_search

def run():
    """
    Run the crew.
    """



    inputs = {
        'topic': roles_to_search,
        'row_count': total_roles_to_fetch,
        'column_names' : column_names,
        'url': url,
        'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    }
    DataCrew().crew().kickoff(inputs=inputs)