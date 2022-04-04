# Churn_probality

The task is to predict the probability of churn for for each user who views brochure

This project was prepared with two step. One of them is model creation, the other one is servis api. The output of machine learning algorithms were written in both sqlite as a database and csv as a file.
SQLite was chosen as the database because this project did not have a very complex data set and focused on that was paid to the ease of installation. Compared to other databases, SQLite performs lower performance, but high performance is not expected from a dataset in this project.

After prediction, you can create rest api to see results. "get_service.py" folder was created for rest service. In this step for easy and fast execution, I prefered to dockerize the service. For dockerization, you have to run below commands on terminal.

1) docker build --tag churn-probability-app:1.0 .
2) docker run -p 1001:1001 --name churn-probability-app churn-probability-app:1.0

After this process, you can use postman to test. There are four different get service under two main group. 

**Group one:**

a-(get_all_results) : This service return probability value for every transaction. This method doesn't need any parameter. 

b-(search_userId_churn_probablity) : This service get userId as a input parameter and return transactional results of specific user


**Group two:**

a-(get_all_unique_results) : This service return user based probability value. This method doesn't need any parameter. 

b-(search_unique_userId_churn_probablity) : This service get userId as a input parameter and return his/her result of churn probablity

Whole services return dataframe as a json message.

You can find postman collection on collection folder.
