The project needs the following file, .env, at path CrewAI_API\data_crew.

Include the following in the file:
MODEL=gpt-4o-mini (can be changed to another LLM)
OPENAI_API_KEY=(include your api key from Open AI)
SERPER_API_KEY=(get serper api key from serper.dev)


In your terminal run the following to install extensions:

pip install crewai
pip install crewai[tools]
pip install flask
pip install thunderclient

I use and recommend Anaconda virtual environment for this project
