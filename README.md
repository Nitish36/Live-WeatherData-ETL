### Method to run the project
1) Install a selenium driver based on your browser choice. It is different for different browser. Mine is Chrome browser.
2) Save it in Program Files(x86)
3) Copy the codes as it is from the file and rename the files in the same manner as how I have done
4) Install Google Drive and Google sheet api and save ur credentials in a separate folder
5) A attached a link of the two videos on how to do it here. https://youtu.be/PyaRgFJBnH4?si=gB29NNm0JmzEPdG0
6) Once the setup is done you can test it if everything is working correctly whether the data is getting stored in the csv file or not
7) Next create an account in prefect and follow the steps which I have given below
8) Run the following commands 1 by 1. 
9) To build pipeline: prefect deployment build pipelines.py 
10) To show on browser: prefect deployment build pipelines.py:push_to_database -n weather_deployment 
11) Run yaml file: prefect deployment apply push_to_database-deployment.yaml 
12) To start the agent:  prefect agent start -q 'default.' 
13) In the prefect cloud switch on the pipeline.
14) U can schedule the pipeline to run anytime as u wish
15) And finally visualize the same on a dashboard using any visualization tool. I have used PowerBI
