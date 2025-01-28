#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from crew import DataCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Python_Developer',
        'row_count': '12',
        'column_names' : 'Company Name, Job Title, Job Description, Responsibilities, Qualifications and Skills, Experience Required',
        'url': 'https://www.linkedin.com/jobs/search/?currentJobId=4133700098&keywords=python%20developer&origin=SWITCH_SEARCH_VERTICAL',
        'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    }
    DataCrew().crew().kickoff(inputs=inputs)

run()