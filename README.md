# MovRekE2E
MovRekE2E - Movie Recommendations end to end: is a movie recommendation service. 

### What's the impact here?
This project is special because the focus here was not on the modelling side of a recommendation service but instead end to end development, monitoring and load balancing of the inference service. End result was a containerised inference service supporting automated model updates with canary releases and data provenance tracking. All this was managed by CI/CD pipeline as well as evaluation, data quality issues and fairness aspects were also considered.

### What was done?
- Implementation of the recommendation service
- Evaluation of service: Offline and Online eval
- Data Quality and pipeline
- Continuous integration and Testing
- Monitoring
- Containerization and automated model updates
- Load balancing and Provenance
- Reflections on fairness, deployed service and teamwork

### Who did it?
This project was a collaborative effort between:
  - Aayush
  - Rishabh
  - Tamara
  - Varun
  - Yaoqiang

### What was my role?
- Implementation of the recommendation service: Load and infrastructure considerations, assisted in modelling at later stages.
- Online Evaluation
- Data processing, Data Quality, Provenance
- Test reports and runners
- Containerization
- Monitoring, deployment considerations on kubernetes



- [](#)
    - [What was done?](#what-was-done)
    - [Who did it?](#who-did-it)
    - [What was my role?](#what-was-my-role)
      - [Tools I used](#tools-i-used)
    - [What's the impact here?](#whats-the-impact-here)
- [Modelling and inference service](#modelling-and-inference-service)
  - [Learning](#learning)
    - [Collaborative filtering](#collaborative-filtering)
    - [Cold start](#cold-start)
    - [Adult movie filter](#adult-movie-filter)
    - [Implementation](#implementation)
    - [Limitations](#limitations)
  - [Inference service](#inference-service)
    - [Implementation of the recommendation service](#implementation-of-the-recommendation-service)
    - [Design decisions](#design-decisions)
    - [Architecture](#architecture)
    - [Load and infrastructure considerations](#load-and-infrastructure-considerations)
    - [Dockerization of our inference service](#dockerization-of-our-inference-service)
    - [CI/CD pipeline](#cicd-pipeline)
- [Evaluation of service](#evaluation-of-service)
  - [Offline evaluation](#offline-evaluation)
    - [Evaluation of the performance of the model](#evaluation-of-the-performance-of-the-model)
    - [Unit tests for offline evaluation](#unit-tests-for-offline-evaluation)
  - [Online Evaluation](#online-evaluation)
  - [Online evaluation metric](#online-evaluation-metric)
    - [Telemetry collection system: How did we work with real time data?](#telemetry-collection-system-how-did-we-work-with-real-time-data)
    - [Calculation involved?](#calculation-involved)
      - [Scoring recommendation list](#scoring-recommendation-list)
      - [Scoring ratings](#scoring-ratings)
      - [Scoring runtime](#scoring-runtime)
      - [Final calculation](#final-calculation)
      - [What does the metric mean? How to interpret it?](#what-does-the-metric-mean-how-to-interpret-it)
      - [Special note](#special-note)
- [Data Quality and pipeline](#data-quality-and-pipeline)
  - [Data Quality](#data-quality)
    - [What makes data "high quality" in our context?](#what-makes-data-high-quality-in-our-context)
    - [Data processing at different end points](#data-processing-at-different-end-points)
    - [Data quality reports](#data-quality-reports)
  - [Pipeline:](#pipeline)
  - [Pipeline structure:](#pipeline-structure)
    - [Description of each stage:](#description-of-each-stage)
- [Continuous integration and Testing](#continuous-integration-and-testing)
    - [1. Infrastructure:](#1-infrastructure)
    - [2. Automated Model Testing:](#2-automated-model-testing)
      - [Unit tests for data quality](#unit-tests-for-data-quality)
    - [Data processing tests](#data-processing-tests)
    - [Test reports and runners](#test-reports-and-runners)
- [Monitoring](#monitoring)
    - [Prometheus](#prometheus)
    - [Grafana](#grafana)
    - [Alert Manager](#alert-manager)
- [Containerization and automated model updates](#containerization-and-automated-model-updates)
    - [Container set up](#container-set-up)
      - [Flask application](#flask-application)
      - [Load balancer](#load-balancer)
    - [Orchestration and automatic container creation in CI/CD pipeline](#orchestration-and-automatic-container-creation-in-cicd-pipeline)
  - [Automated model updates](#automated-model-updates)
- [Releases](#releases)
    - [Triggering releases](#triggering-releases)
    - [Monitoring the release](#monitoring-the-release)
    - [Load balancing](#load-balancing)
    - [Metrics](#metrics)
    - [Provenance](#provenance)
- [Fairness](#fairness)
    - [Definition](#definition)
    - [Potential issue 1](#potential-issue-1)
    - [Potential issue 2](#potential-issue-2)
    - [Reduce potential issues](#reduce-potential-issues)
  - [Feedback loop](#feedback-loop)
    - [Potential issue 1 - Echo chamber](#potential-issue-1---echo-chamber)
      - [Description](#description)
      - [Detection](#detection)
      - [Mitigation](#mitigation)
    - [Potential issue 2 - Filter bubble](#potential-issue-2---filter-bubble)
      - [Description](#description-1)
      - [Detection](#detection-1)
      - [Mitigation](#mitigation-1)
  - [Analysis of Problems in log Data](#analysis-of-problems-in-log-data)
  - [Fairness](#fairness-1)
    - [Dataset analysis](#dataset-analysis)
    - [Quality of recommendations](#quality-of-recommendations)
  - [Feedback loop](#feedback-loop-1)
- [Reflections on Recommendation Service](#reflections-on-recommendation-service)
    - [Cold start problem](#cold-start-problem)
    - [Telemetry Collection System](#telemetry-collection-system)
    - [Load Balancing and Kubernetes](#load-balancing-and-kubernetes)
  - [Reflections on Teamwork](#reflections-on-teamwork)
    - [What went well](#what-went-well)
    - [Challenges](#challenges)
    - [Takeaways](#takeaways)
    - [Some points worth highlighting about our implementation:](#some-points-worth-highlighting-about-our-implementation)

# Modelling and inference service
## Learning

For our movie recommender model, we used collaborative filtering and other filtering techniques to produce the recommendation.  
Following is a brief description of the learning methods involved:

### Collaborative filtering

Collaborative filtering is a widely used technique in recommender systems based on the idea that the users who previously liked the same movies in the past are more likely to like the same movies in the future. It estimates the similarities between the users and uses it to produce the prediction. To compute the similarities, we use the k-nearest neighbors algorithm with cosine similarity function.
We chose this technique because it is very popular for recommendation systems and allows us to have a good starting point that we can improve on later.
To estimate how much a user liked a movie, we use the ratings given by that user.

### Cold start

To improve our algorithm, we decided to reduce the cold start problem. The cold start problem is one of the biggest problems of collaborative filtering: when a user has not yet given enough ratings, the collaborative filter does not have enough data to find similar users. In case there is not enough data on a user, we decided to use their demographic data to find similar users and also the IMDB rating of the movies to recommend the movies liked by everyone based on matching priority. For now, the only demographic info taken in account by our model is gender.

### Adult movie filter

We also put an adult movie filter that avoids recommending adult movies to kids.

### Implementation

For our implementation, we utilized the Python library Pandas to manage the databases, and we employed Surprise for the machine learning component. Our model's primary function is to estimate movie ratings for those films a user has not yet rated. We then select the top 20 highest-rated movies, sorted in descending order.

In the case of adult-oriented movies and users under the age of 18, the predicted rating for such movies is set to 0. If we possess sufficient data to employ collaborative filtering, we rely on its predictions. In situations where collaborative filtering data is insufficient, our predictions are derived from a combination of the IMDb rating and the average ratings given by users of the same gender for the respective movies.


### Limitations

Due to the substantial user base, collaborative filtering necessitates an extensive volume of ratings to yield meaningful results. The process of gathering data from the stream is time-consuming, and as a result, we faced limitations in accumulating a sufficient amount of data to make our model truly effective. This situation has led to the "cold start problem" affecting the majority of users, as we currently lack the requisite data for them.

Our solution moving forward entails planning to retrain our model once we have amassed a more substantial dataset. This proactive approach will help mitigate the cold start problem and enhance the overall effectiveness of our model.

## Inference service

### Implementation of the recommendation service

The training weights were exported to the model file which can be used for making predictions in response to incoming requests from the simulator. We placed the model, app and its dependencies in a docker container which interfaces to port 8082 of the VM in McGill infrastructure.

### Design decisions

Since we did not want to retrain the model for each request, we are calling the training function when the docker container is started and it is mounted to persist across rebuilds. With the model loaded, we are calling the prediction on it after loading supporting data from the csv which is added in our container so that we do not have to query the simulator for user or movie attributes to provide as input to our model. To maintain the principle of separation of concerns, we kept the model and the prediction service in two distinct modules.

We wrapped the call to model in the prediction service and exposed it as the API endpoint for the get requests from the simulator. We would return the list of movies to the simulator. The list of movies is sorted by the rating score when provided to the prediction service as the output from the model.

### Architecture

The simulator hits the following endpoint 'recommend/<userid>' running on our team's machine (fall2023-comp585-4.cs.mcgill.ca) with 'GET' requests which then routes it to prediction service for handling. This was implemented in flask. To further reduce the load in terms of data loading on the container, we made a user_details fetcher in the request handler which would send back a query to the simulator on the user_api to fetch attributes (age, occupation and gender). As we had already scrapped the whole user data set (1 million users) by the time we submitted M1, we did not end up using back_queries for now. The predictions are returned to the handler service from the model (model's working described in learning.md). We return the predicted list (which is already sorted based on the rating's ranking) as a string to the simulator for which we see the success response in the kafka logs. We found that a list object (or) dictionary object is not interpreted as a successful response by the simulator.

### Load and infrastructure considerations

We deliberated on the following system design related issues which may arise due to scaling the requests. For instance, a load balancer could be exposed to the simulator API consisting of a buffer which will redirect the requests to multiple containers. Each container will consist of the model prediction service. Further, a performance argument could be made against the redundancy of maintaining multiple copies of the same model across different containers to ensure load balancing. This could be problematic while incorporating model updates and testing different model versions. Lastly, if we have huge datasets to be used for training, deploying the same datasets on multiple containers to train multiple models for load sharing can be further optimized. A fine tuned approach could be to split the dataset across containers so that training is distributed and we can combine the weights in a single container to form the model which can live on a separate container. We can use caching to serve the model weights or apply concepts similar to Content Delivery Networks to ensure fast servicing of prediction requests from multiple containers to which our load balancer is redirecting the requests. It is to be noted that we did not implement their resolutions considering the deadline for M1.




### Dockerization of our inference service

We have placed the model file and the app driver code in the same container. Port (8082) inside the container is mapped to the port (8082) of the host machine (fall2023-comp585-4.cs.mcgill.ca) such that the requests received at the VM are forwarded to container's port when the container is deployed. We tried using the alpine version of the Python image to keep our container lightweight, but we found that packages end up with dependency errors. So we decided to use the Python base image (though larger) for the moment due to time constraints. We will work on optimizing the Docker container in the future. We set the working directory as app (base directory) in the container where we place the model and data directories. When we launch the container, we run the app.py to start our inference service. When started for the first time, we launch the training on the container for model creation to avoid packaging the model (2GB in size) within the containers as it would slow down the deployment.

### CI/CD pipeline

Though not part of milestone 1, we decided to leverage GitLab's CI/CD capabilities to set up a pipeline in the early stages of development. This is an important step in automating the development lifecycle. A pipeline was set up to automatically deploy the inference service onto a Docker container running on our remote server whenever code is merged into the main branch. A GitLab runner was set up on one of our teammate's local machine in order to run the CI/CD jobs. The CI/CD job itself used an Ubuntu Docker container to SSH into our remote server using a private key generated on the server. The private key was converted to base64 format and added as a masked GitLab CI/CD variable, which means that the variable is hidden in job logs. This is vital from a security standpoint. The job pulls the latest code from the GitLab repository, builds the Docker image and deploys the container. The CI/CD pipeline simplifies the process of deployment, precluding the need for manual intervention during the deployment stage.

# Evaluation of service
## Offline evaluation

### Evaluation of the performance of the model

To evaluate the performance of the collaborative filtering model, we divided the dataset containing the ratings into two parts:
- A test dataset that corresponds to 20% of all ratings we have collected.
- A train dataset that corresponds to 80% of all ratings we have collected.
The model is then trained only on the train dataset. Then, we predict a rating with the model for each of the (user_id, movie_id) pairs present in the test dataset, and we calculate the Root Mean Squared Error between the list of predictions of the model and the list of real ratings present in the test dataset. Because the model was not trained on the data from the test dataset, we are know that RMSE is not biased by overfitting the test data. 

The Root Mean Squared Error measures the average difference between values predicted by a model and the actual values. We choose this performance indicators because it permits to know the average error that is made on predictions in general, which seemed to us to be the most relevant indicator. For example, this value can then be compared to the standard deviation of the rating dataset, which allows us to compare our predictor to a predictor which would always predict the average of the ratings. 

With our ratings dataset we have a Root Mean Squared Error of: 0.7215937657284225

### Unit tests for offline evaluation

We also coded unit tests allowing us to see if the recommendations seemed at least coherent and which also allows us to test the other filters. For these unit tests, we created our own datasets, much smaller and simpler than the real datasets. Creating these small datasets allows us to have a better understanding of what is happening and to be able to more easily test simple cases. 

In these unit tests, we test:
- If a person under the age of 18, no film marked as "for adults" has been recommended to them (test for the adult filter)
- Verify that the recommendation includes 20 movies
- Verify that movies already rated by a user are not recommended to him/her again.
- Verify that a new user have also a list of 20 movies when he asks for recommendation.

We also test some functions used for our model in the unit tests:
- Verify that the model saves in the correct file.
- Verify that our helping function that print the results of the recommendation prints the result correctly.
- Verify that we load the entire dataset by checking the size.



## Online Evaluation

We will determine the performance of our system while it is deployed based on the following factors:
- online evaluation metric (which we will define and explain below)
- response time of the API

## Online evaluation metric

Usually, online evaluation involves A/B tests which means there should be another recommendation model to compare our recommendation with (as we do not have access to ground truth). But in our case, instead of contrasting and comparing our recommendations with another model, we instead looked at the logs and the ratings from the user in real time. Our rationale was something along the lines of the phenomenon observed while watching youtube. Say, the user is watching some video and he/she gets a bunch of recommendations and they may also get asked "what do you think about this recommendation?". Borrowing from that idea we thought, what if we look at the logs in real time to check for the ratings and latest watch history of the user.

So our online evaluation works like this: We look at the latest ratings provided by a user. We also collect the data on what proportion of the movie is watched. Then we compare them with what our recommendation is and calculate a score for each recommendation. Lastly, we record the response time to get this recommendation and record this to track the performance across a random sample of users.

This approach makes sure that we make use of the telemetry information provided from the logs (in real systems, we presume there will more details available in the telemetry data including user behavior on the website, which is not present in the available logs. But we do have information on watchtime and ratings which we use.)

### Telemetry collection system: How did we work with real time data?
Our team initially considered the use of a standard database along with Python scripts to collect, process and store data from the Kafka stream in different formats. However, while exploring tools for our monitoring infrastructure, we came across Grafana Loki, an efficient log aggregation system inspired by Prometheus. Quoting from their description, "It is designed to be very cost effective and easy to operate. It does not index the contents of the logs, but rather a set of labels for each log stream." [^1] Considering the volume of data and the experiences of our peers shared during the M1 presentation, we decided to use Loki as our logs database. Loki seemed promising as it would help us evade both the problem of quickly running out space on our server with a local database or running out of limited free storage on a cloud database. We used the default Loki storage option, where logs are compressed and stored in chunks in the file system. The logs are rotated weekly. 

To send the logs from our Kafka stream to Grafana Loki, we used the agent Promtail. We also parsed and processed the logs with the help of Promtail. We defined four categories of logs: recommendation (successful recommendation requests with status 200), error (failed recommendation requests with status 0), history (records of the users' watch history, i.e. the GET /data endpoint) and rating (records of users' ratings for different movies, i.e. the GET /rate endpoint). Each log line was matched to a regular expression to identify its category. Named groups pertaining to important details were extracted from the log line and processed to create the final log to be sent to Loki in different formats depending on the category. (For example, *timestamp, userid, movied, minute_watched* for history and *timestamp, userid, error, error_msg, response_time* for error). An example can be found [here](http://fall2023-comp585-4.cs.mcgill.ca:3000/d/ce43d1d7-0e50-4bd0-95b8-3f28d8f9f804/monitoring-dashboard?orgId=1). This categorization of logs made it easy for us to fetch only the logs of interest during online evaluation and monitoring. Initially, we were using these tools for log collection and monitoring but we discovered that they can be exposed over an API to gain access to the log data so that it can be used as dataset that would be updated in real time from the Kafka stream. So, we wrote a wrapper for the above mentioned tools to send API requests with the queries we wanted to obtain the results for our online processing

[^1]: https://grafana.com/oss/loki/

### Calculation involved?

#### Scoring recommendation list
- If the sample-movie lies in the top 5: score = 10/10
- If the sample-movie lies in the top 6-10: score = 8/10
- If the sample-movie lies in the top 11-15: score = 5/10
- If the sample-movie lies in the top 16-20: score = 3/10
- If the sample-movie does nit lie in the recommended list: score = 0.01/10

#### Scoring ratings
The users would have given some rating to the movie: (score/5)

#### Scoring runtime
Based on how much of the movie the user has watched.
```
    [0-20%):    1/5
    [20-50%):   3/5
    [50-70%):   4/5
    [70-100%]:  5/5
```
#### Final calculation
We wanted to capture how the user is perceiving our recommendations:
i) Depending on how much of the movie was watched: Recommended_list_score x runtime_score
ii) what rating was given: Recommended_list_score x Ratings_score

(i+ii): predicted movie scaled score to tell us appropriate the recommendation was.

#### What does the metric mean? How to interpret it?
Care was taken to ensure that we do not end up with zero values while multiplying the scores. 
We capture the following trends in our metric:
- How highly ranked was the sample-movie in the list of recommended movies or if the sample-movie was even part of the recommendation at all?
- What did the user feel about the movie? (captured by the rating they gave to the movie)
- Apart from feeling, how did the user actually act for that movie? (captured based on how much of the movie did they actually end up watching)
- How much time did we take to give our recommendation?

#### Special note
Originally we spent quite a bit of time to calculate the score for online evaluations as follows:

We looked at the latest ratings provided by the user. For that user and the movie combination, we looked at how much of the movie was watched by the user. Then we compared it with our recommendation. If the movie which the user rated high and watched a lot of was indeed part of our recommendation, then our recommendation was good.

This would have given us a single scaled score as follows: Recommended_list_score x Ratings_score x runtime_score = predicted movie scaled score to tell us appropriiate the recommendation was.

But **the problem** we faced with this approach was that we were limited by the LOKI API to get the result set for our queries to ratings and history view. This meant we could not access more than 5000 records at a time through the request in our code but we had the access to full history through directly getting the values in the grafana dashboard. The problem was that a common movie and user combination did not exist in the ratings and history view for the 5000 records we had access to in a single API request. We did not have the time to write a selenium script to bypass their restrictive limit. It is possible that since we are using free which is why we had this limitation. To overcome this, we changed our evaluation strategy such that it could work with rolling logs as described above.



# Data Quality and pipeline
## Data Quality


### What makes data "high quality" in our context? 
_Common dimensions of data quality include accuracy, completeness, consistency, reliability, and timeliness._

Our pipeline for data was as follows:
- Save the logs to flat files.
- Preprocess the flat files to clean data collected. Inspection was done to identify any obvious issues with the data collected. We found missing values and spurious entries. We dropped all those records.
- Filter and segregate data collected according to the type of data files. Convert them to csv files.

- The user data was scrapped from the simulator API for 1 million users.
- Movie attributes were scrapped from the API for the items obtained from kafka logs.
    - As an enhancement, we loaded the movie attributes and imdb ratings from external sources too for M2. This was done using the "tmdb_id" attribute we had for each movie
    
    ### how can you use the external imdb files?

    The movieids from the simulator comprise of the name of the movie and the year separated by '+' symbol. Movie attributes returned by the simulator contain a mixture of data from imdb and tmdb datasets. There are unique ids corresponding to each of these datasets in the response. We want to use the imdb dataset as an external source and found that the name of the movie corresponds to original column of the imdb dataset and the year to endyear column. Through this we can obtain the imdb_id which can be used to join to other tables from imdb to get more information for the movies.


    - From the kafka logs, sometimes we would get made up movie details. Since it was mentioned in the requirements of the project that the simulator is using imdb movie database to generate logs, we went directly to the external source to avoid such spurious logs.

- Kafka logs are responsible for giving watch history, telemetry and ratings by each user (whether the liked the movie or not). We loaded the kafka logs to grafana monitoring. Further, we found that grafana can be used a database to serve the logs in response to API queries. So to retrieve real time information about the system for online evaluation, we added processing at the destination endpoint of those API queries to get filtered data outputs.

### Data processing at different end points
One notable aspect was the handling of data at end points. Since we have parsed logs to loki and were accessing them through grafana, we made sure to take care of duplicates and spurious values when retrieving data through those end points.

### Data quality reports
We generated reports for each of the data set used for training the model. In the report we tracked missing cells, duplicate rows, memory size, variable types, distinct values, data range and correlation among attributes. Following are the screenshots from one of our data reports:

![data_quality_1](milestones/M2/artifacts/data_profile_1.PNG)
![data_quality_2](milestones/M2/artifacts/data_profile_2.PNG)
![data_quality_3](milestones/M2/artifacts/data_profile_3.PNG)
![data_quality_4](milestones/M2/artifacts/data_profile_4.PNG)
![data_quality_5](milestones/M2/artifacts/data_profile_5.PNG)



## Pipeline:
We implemented an MLOps to get constant feedback during the development process and make sure that our code works seamlessly across different modules (data, ML model, app, etc.). 


## Pipeline structure:

![pipeline](milestones/M2/artifacts/pipeline.png)

We configured our pipeline to sequentially run the following different jobs/stages:
  - test-data
  - test-model
  - test-app
  - coverage
  - deploy

### Description of each stage:
- **test-data:** This pipeline runs tests on the data quality and data processing ensuring that the data which is being fed into the model is of good quality. 
  - It runs tests like checking if the movies are getting filtered, curl requests are working etc.  
  - Works on the following branches: main, development

- **test-model:** This pipeline runs tests on the model and ensures that functionalities like printing recommendations, test-train split, global dataset values etc. are working fine.     Based on these tests we get a good benchmark of our model performance.  
  - Works on the following branches: main, development.

- **test-app:** This pipeline runs tests on the flask app and ensures that functionalities like testing the endpoint of the flask app and other functions of the API are working fine.  
  - Works on the following branches: main, development

- **coverage:** We implemented a pipeline for the code coverage which tells us how much code of the app has been tested by the tests that we developed. 
  - This pipeline combines the results of all our tests described previously (data, model, app) and returns the final code coverage report. Currently our test coverage is at 91%.
  - Works on the following branches: main, development  

**Screenshot of our coverage report:**
![coverage](milestones/M2/artifacts/coverage.png)


- **deploy:** After all tests have passed, this final pipeline deploys our model and the app to our team server hosted on GitLab.  
Works on the following branches: main  
  - We set this job to work on only the `main` branch and not `development` as we don’t want to deploy a new model each time a new commit is pushed to development which is our final testing branch. Only when we are confident of our code we push to the `main` branch which deploys the model.  

**Reason why our testing is adequate:**  
As described above, we have tested the most crucial aspects of a machine learning model pipeline i.e. the data quality and the model performance. Additionally we have also tested the app interaction which makes our end-to-end test suite robust.


**Reason for making the jobs sequential:**
We wanted to make sure that in case any of the jobs like `test-dat`, `test-model` and `test-app` fails, we don’t proceed forward unless we have fixed the issue concerned with the failing pipeline.

# Continuous integration and Testing
In addition to the various stages of the pipeline as described above, we also focussed on the following:
### 1. Infrastructure:

We have configured our systems to act as GitLab runners. This allows for efficient and rapid execution of CI/CD jobs in a Doker environment, ensuring that our code integrations are validated in real-time. By hosting our runners, we could manage the CI process to match our project’s requirements.  
\
Following is a screenshot of our runners:
![runners](milestones/M2/artifacts/runners.png)

### 2. Automated Model Testing:

The model testing phase not only evaluates the model's correctness but also benchmarks its performance. This ensures that the model not only produces the right results but also operates within the expected time and resource constraints.  

**Service:**
The CI process is integrated within our GitLab repository.  

#### Unit tests for data quality
We have done some unit test to be sure that the data is consistent. In these unit tests, we test:
- If all the user_ids in the ratings dataset are existing user_ids in the users dataset
- If all the movie_ids in the ratings dataset are existing movie_ids in the users dataset


### Data processing tests
We added made sure to add tests while considering that we do not introduce test specific flows in the programs. The unit tests were added to run before the deployment pipeline so that regression tests were covered. For data preprocessing scripts, unit tests for fetching movies, filtering movies and sending curl requests to API for creating the dataset were covered. We also included negative cases and tests to unpack the ratings and history data. Dummy dataset files were used so that the unit tests do not have to interface with actual data and make these unit tests pretty quick. 

### Test reports and runners
Most of the unit tests were written in pytests. They were kept under tests directory on the app folder. Some tests had to be kept outside because of relative module import issues. We used html-report package added as a plugin to the pytest runner so that we can generate reports for our test suites. The report runner keeps track of the history of the past runs. It saved in the archival files which are read everytime report is generated.

Following are the artifacts from our test reports:
![test report 1](milestones/M2/artifacts/test_report_1.PNG)
![test report 2](milestones/M2/artifacts/test_report_2.PNG)
![test report 3](milestones/M2/artifacts/test_report_3.PNG)
![test report 4](milestones/M2/artifacts/test_report_4.PNG)

# Monitoring

Our monitoring system operates on four main components: the telemetry collection system (described in the online evaluation section), the system metrics collection stack involving Prometheus, cAdvisor and node-exporter, the Grafana dashboard and the alert manager ([Docker configuration](monitoring/docker-compose.yml))

### Prometheus
Prometheus was set up along with cAdvisor and node-exporter to scrape metrics from our running containers, such as resource usage, filesystem usage etc. In addition, Prometheus was configured to scrape metrics from Loki and Promtail as well. Custom metrics were defined in Promtail to collect the number of successful and failed recommendation requests, and a histogram of response time. 

### Grafana
Two dashboards were created in Grafana: the Logs dashboard ([link](http://fall2023-comp585-4.cs.mcgill.ca:3000/d/e027f147-6f47-4cf3-b7af-8ffa87ac664b/logs-dashboard?orgId=1)) and the Monitoring dashboard ([link](http://fall2023-comp585-4.cs.mcgill.ca:3000/d/ce43d1d7-0e50-4bd0-95b8-3f28d8f9f804/monitoring-dashboard?orgId=1)). The Logs dashboard provides a playground to view and explore the 4 categories of logs collected by Loki, as explained in the online evaluation section. 
![logs_dashboard](milestones/M2/artifacts/logs.png)

The Monitoring dashboard is made up of two parts. The first row provides visualizations and statistics to monitor the availability of our recommendation system. In particular, it display the number of successful and timed out requests obtained from the custom Promtail metrics, along with the percentage of failed recommendations. There is a panel to monitor the health of our recommender service infrastructure, that displays the number of associated running containers. Our recommender service has 3 containers, one nginx load balancer and two instances of our Flask service. Thus, this metric should always have a value of 3. We also provide the CPU usage to monitor that our service is not overloaded. 
![availability](milestones/M2/artifacts/availability.png)

The second row monitors the model quality. Currently, we have two plots derived from the histogram metric: the average response time and the a histogram of the response time. The histogram gives us a picture of the distribution of the response time.
![model_quality](milestones/M2/artifacts/model_quality.png)

### Alert Manager
Three rules were defined in Prometheus to trigger alerts in case of aberrations in the running of the recommendation service.
Alert Manager was set up to send the alerts on our private group channel on the COMP585_ISS_A2023 Slack server. ([rules.yml](monitoring/prometheus/rules.yml))
- Alert when any of the services Prometheus is monitoring is down for more than 2 minutes (cadvisor, node-exporter, promtail, loki). This rule was set up to ensure that the monitoring infrastructure itself is functioning well
- Alert when any one of the three recommendation service containers (1 nginx and 2 flask) goes down. This rule is very important as this alert could imply that there is a disruption in our service or that the server would get overloaded (with just one flask container running)
- Alert when more than 80% of recommendation requests time out. This rule is important as it means that our service is largely unavailable and requires immediate diagnosis. 

![Slack alert](milestones/M2/artifacts/slack.png)



# Containerization and automated model updates
We have four running containers for our inference service at all times: two containers for the stable deployment, one for the canary deployment and one for the load balancer. We additionally have containers running Prometheus and cadvisor as part of our monitoring service.

### Container set up 
#### Flask application
The containers for the stable and canary deployment of our application are built using the [same Dockerfile](/app/Dockerfile) with configurable options. They use a lightweight Python alpine image as the base image to minimize the size of the resulting image. Extra system dependencies needed to run the `surprise` library [^surp] for our recommendation service are installed onto the base image. Our container set up packs both the model and the inference service within the same container. Gunicorn is the web server used to deploy the Flask application. Gunicorn is a Python WSGI HTTP server ideal for deploying Python web applications in production [^gu].

#### Load balancer
We use NGINX as our load balancer [^nginx] to distribute the load between the stable and canary deployments. We again use an alpine version of the NGINX image to reduce the container size. Our custom [NGINX configuration](/app/nginx/nginx.conf) is mounted as a volume onto the container. 

### Orchestration and automatic container creation in CI/CD pipeline
We use [docker compose](/app/docker-compose.yml) to orchestrate the deployment of our containers. For the initial launch, all our containers can be created simply by running a single command in the `app` directory: `docker compose up -d`. During subsequent launches, a [bash script](/scripts/deploy.sh) in our CI/CD pipeline handles the creation and replacement of containers. Docker compose is used to take down or relaunch the required services. Containers are automatically created as part of our canary release pipeline. This process is explained in detail in the Releases section.

[^nginx]: https://www.nginx.com/
[^surp]: https://surpriselib.com/
[^gu]: https://gunicorn.org/ 

## Automated model updates
We implemented the automatic training and deployment of the models by developing a python script (`auto_deployment/auto_deploy.py`) which broadly performs the following tasks: \
\
**1. Data collection and pre-processing from the Kafka stream:** \
The raw data is collected from the Kafka stream for 15 minutes and pre-processed. After this it is appended to the records previously collected in `data/clean_rating.csv`.

**2. Training the models with the new data:** \
The newly collected data is now used to train the model \

**3. Checking if RMSE score is < 1:** \
We do our offline evaluation i.e. checking if RMSE score is less than 1  after the model has successfully been trained as described previously. If this condition is not satisfied, the new model doesn’t get deployed and the user gets an email mentioning that the new model wasn’t deployed and also reports the RMSE score.

**4. Versions the new model using DVC:** \
If the offline evaluation metric is satisfied, the new model gets versioned by DVC.

**5. Pushes the newly collected data to GitLab:** \
Finally, if everything works fine till this point, the newly collected data as well as the version is pushed to GitLab. This triggers the automated testing pipeline and also deploys the new model. 

**6. Users get notified via an email:** \
After the successful deployment of the model the users get an automated email confirming that the deployment was successful.

Additionally, we developed a Python scheduler script (`auto_deployment/scheduler.py`) which runs in the background on our team-4 server and triggers the auto deployment pipeline every 2 days.


# Releases

### Triggering releases
As described in the previous section, when the new data is periodically pushed to our GitLab repository, the pipeline is triggered which passes through data quality checks ([test-data](/.gitlab-ci.yml)) and tests for the model ([test-model](/.gitlab-ci.yml)) and inference service ([test-app](/.gitlab-ci.yml)). If the tests run successfully, the final job of the pipeline `deploy` establishes an SSH connection to our server and pulls the latest version of our repository on the server. It then launches a [background script](/scripts/deploy.sh) to perform the canary release.

### Monitoring the release
The release script performs the following actions: (1) It kills the current canary container, builds a new image containing the new model and recreates the canary container. (2) It waits for 12 hours to allow the new deployment to stabilize and receive a fair amount of requests (3) After 12 hours, it sends a curl request to the Prometheus HTTP API to fetch the average response time of the successful requests over the past 12 hours. (4) Our threshold response time is 500ms. If the average response time is below the threshold, it builds a new image with the `stable` tag and recreates the two stable containers. At this point our canary release is successfully completed. If the average response time is greater than the threshold, the canary release is aborted by removing the canary container and sending an email notification to our team informing of the failed release.

After the canary release is complete, we retain the canary container along with the newly deployed stable containers as this will increase availability of our service. This means that all three containers serve the stable deployment at the time. Though this may not be an ideal practice in production, we chose to follow this approach as it allows us to serve a greater number of successful requests.

### Load balancing
Our NGINX load balancer is configured to execute a 80-20 split of the incoming traffic between the two containers of the stable deployment and the canary container respectively. 

```
upstream backend {
        server inference_stable:5000 weight=4;
        server inference_canary:5001 weight=1;
    }
```

NGINX automatically distributes the load to available services in case any service is unavailable. For instance, when the canary container is recreated to deploy a new model, all traffic will be routed to the stable service when the container is being created. Similarly, all traffic will be momentarily directed to the canary container when the stable containers are being recreated to finish the new release. In any case, the downtime while recreating the containers is negligible, however, our load balancer ensures that we have zero downtime.

![Pipeline for canary release](milestones/M3/artifacts/canary.png)
Figure 1: Workflow of canary release

### Metrics
Prometheus was set up to track metrics for our Flask application using `prometheus-flask-exporter` [^pfe]. This is a Python package that needs to be installed in our Flask application (check [app.py](/app/app.py)). It exports some default metrics like the response time for each request and the number of successful and failed requests.

```
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
```
To determine whether to perform the canary release, we perform the following PromQL query which computes the average of all recommendation requests. `flask_http_request_duration_seconds_sum` is a metric that gives the time taken for each request in seconds and `lask_http_request_duration_seconds_count` records the number of requests received.

`sum(flask_http_request_duration_seconds_sum{path=~"/recommend/.*"}) / sum(flask_http_request_duration_seconds_count{path=~"/recommend/.*"})`

[^pfe]: https://pypi.org/project/prometheus-flask-exporter/

### Provenance
Our idea behind having provenance in the system was to bind the data and models to our gitlab commits. We wanted to include precise commit messages to help us track the evolution of data/ model with each iteration. As the pipeline code is already tracked based on the commits, we figured this would be a good idea. It is to be noted that uploading models to gitlab is impractical due to size issues. Also, our deployment works through the code changes on our repo and it is heavily making use of gitlab CI/CD so we wanted the benefits of versioning using gitlab for models as well.

**We do the following:** On the host machine (our team-4 server), we have initialized dvc in the deployed repo. We use it to create .dvc files for models. These files are metadata for the models which can be uploaded to gitlab. Multiple files can be created corresponding to different versions of the model. These files primarily consist of md5 hash and as such are small in size. But they (.dvc files) provide a way for us to link models to commits without actually committing model files. We decided it would be practical to add the model.pkl.dvc file for tracking in the same pipeline as auto-deployment. So whenever, our automated data collection script appends processed data to existing data on the host machine (outside of any container), we also initiate training of the model and include the resulting .dvc file of the trained model to the github commit. (**link to code demontrating that:** [dvc tracking within automated data creation pipeline]) It can be argued that the host machine does not possess resources to store different versions of model. This is because each model is roughly 2GB in size. We can offload those models to remote storage using dvc with the .dvc files acting as symbolic links. Since we did not have access to a free remote storage to host multiple models, as a proof of concept: we kept different versions of models but in the form of .dvc files along with the data files. We committed these to the gitlab repo too. This is to denote the remote offloading in real scenario. (**link to code demontrating that**: [remote offloading and versioning]) This allows us to have a great versioning track record of the models and data as depicted in the highlights towards the end of this report.

**Further enhancement**: With the above approach, we were able to track the evolution of data and models along with the pipeline code but linking each individual recommendation with the pipeline code, model and data used to make that recommendation was difficult. We worked out the following approach:
- We created a new mysql container which would host a database on our team's server host machine. To put in perspective, this will be a separate container apart from the release containers and the host machine itself where the auto-data collection scripts were scheduled with cron job. Also, the mysql container has a persistently mounted storage. It is connected to the same docker network as the release containers and is part of docker compose.yml for releases. This was necessary to ensure database connection from within release containers to the mysql docker container. (**link to code implementation**: [docker compose file])
- We created two tables in the database namely:
  - reccom (version_number INT, user_id INT);
  - tracking (version_number INT, data_creation TIMESTAMP, trained_on TIMESTAMP, model_rmse FLOAT);
- Since the mysql container had its port exposed, the host machine could insert data in the tracking table while the release containers were bound to the mysql database when the app was launched. The connection was opened and closed using app_context and tear_down methods of flask. The release containers would insert records in reccom table linking version_number and user_ids of the recommendations being served.
- Lastly, with each iteration of data training and model updation: we [increment] a unique identifier in our auto_deployment module known as version_number which essentially tracks and relates the changes in data to models. It is to be noted that the [version.txt]) file having the number is part of our commit whenever auto-deployment updation happens. Now, each container would have its own copy of the version number ([code link]) depending on which model it is serving which in turn is dependent on the data being used to train it.
- As a result, we store the version_number, and the userID served by the container running that version of model+data along with the data creation timestamp, model creation timestamp and model_rmse score for that version_number in our database. Using a join query helps deliver the output of granular provenance per userID request. (**link to concrete example**: *we recorded [a small video depicting](https://mcgill-my.sharepoint.com/:v:/g/personal/aayush_kapur_mail_mcgill_ca/EY5S8Etc4EFMq9C9PnjU9g0BVhjLkSmJ-ZtK6FXSVEIq3A?e=CtQZNN) it in action and explaining more*)
**example:** Following screenshot depicts the last two rows of the result set sorted in descending order for user_ids. We could not display all the rows due to space limitations in the screenshot.

![Version numbers per requests](milestones/M3/artifacts/version%20number%20to%20user%20ids.PNG)


# Fairness

### Definition

In order to analyze the fairness of our model, it is important to define what we mean by fairness. In the scientific literature, there are numerous definitions of fairness, and a taxonomy of these definitions can be found in [this paper](https://dl.acm.org/doi/pdf/10.1145/3547333). The definition of fairness that we will use in our project is based on three principles:

- Our definition is **outcome-oriented**, meaning that it considers the fairness of the outputs of our model rather than the process.
- We evaluate fairness in relation to **groups of individuals** (for example, based on their gender, age, etc.) rather than the individuals themselves.
- Our definition is based on the concept of **Consistent Fairness**, meaning that two similar groups of individuals should be treated similarly. In the context of our project, this implies that two groups of people should have a similar quality of recommended outcomes, regardless of the social group to which they belong.

### Potential issue 1

A first issue that may arise is that our model does not have the same quality of recommendation depending on the social group to which an individual belongs. The quality of recommendations can be evaluated based on how close the model's predictions are to reality, so we can use the Root Mean Square Error (RMSE). To detect this problem, we can separate our test dataset into different social groups and compare the RMSE for each social group. For example, in the context of our project, we can assess differences in RMSE for each gender, age, and occupation.

### Potential issue 2

A second issue that can arise in the context of recommendation systems is that two groups of individuals may not have the same variety of recommended items. To address this, we can compare the variety of movies that a social group watches and compare it with the variety of recommendations provided. Two groups of individuals with the same variety of movie genres watched should have the same variety of genres in their recommendations.  To detect this problem, we can evaluate the variance of movie genres proposed in the recommendations for each social group and compare it to the variance of the movies watched by that group.

### Reduce potential issues

Issues of fairness often have numerous sources. First, we will discuss one source that can lead to fairness problems: the dataset. Our recommendation system relies on the proximity between users, whether through our demographic filter grouping individuals by social groups or our collaborative filter, which is also influenced by the demographics of individuals because our tastes often align with those of people in the same social groups. Consequently, if we have too little data on a particular social group, the quality and variety of recommendations for that group may be poorer. It is crucial to have a diverse and representative dataset. Note that the dataset should not only contain sufficient data for all social groups but also for all intersections of social groups. One way to address this issue would be to collect more data on social groups with less data.

The lack of variety in our system's recommendations can also be attributed to the implementation of our model. Our model includes a demographic filter that acts solely based on a person's gender. This can lead to gender stereotyping of recommendations, especially if combined with an imbalanced dataset between the two genders, as the variety of films appreciated by one gender might be less well captured. One way to address this problem would be to consider additional demographic factors in our demographic filter.

## Feedback loop

### Potential issue 1 - Echo chamber

#### Description

The first feedback loop is called the "echo chamber". This feedback loop occurs when an item is highly recommended, leading to more users watching it. In the context of our model, this can happen because we consider the overall popularity of a movie to estimate its recommendation, and thus, movies that are generally well-liked are highly recommended.

The echo chamber can have both positive and negative consequences. The positive impact of this feedback loop is that most of the time, when a movie is liked by many users, there's a high probability that it will appeal to the majority of users. Consequently, it will appear in the recommendations of more and more users as it gains popularity.

But, if a movie becomes highly rated because it is extensively watched by a bubble of people who like that type of movie, it will then be propelled into everyone's recommendations, including those not particularly interested in that type of movie. With this movie repeatedly appearing in recommendations, even users who are not interested may eventually watch it. If it turns out not to be to their liking, they might give it a poor rating. The impact of this can vary depending on the recommendation model used: if the model primarily considers the number of people who have watched the movie, it might further boost its recommendations. However, if the model is based on ratings (like ours) or viewing time, the movie might cease to be recommended altogether, even to those who initially enjoyed that type of movie.

On the contrary, this can also lead to some movies never recommended. For instance, if a movie receives an initial poor rating, it may not appear in the recommendations for anyone and, consequently, never get watched, so never get rated again, etc.

#### Detection

This feedback loop can be detected by observing how the ratings of certain movies evolve based on how much they have been recommended. It's also crucial to examine which films are never recommended. Monitoring these patterns can provide insights into the presence and impact of the echo chamber feedback loop.

#### Mitigation

A solution to mitigate this is to place less emphasis on the popularity of a movie if the positive ratings come from users who have little resemblance (this can be assessed using the similarity matrix generated by collaborative filtering, for example), and to give it more weight if it comes from a bubble of people with similar tastes.

Another solution, especially to prevent movies from never being recommended, is to introduce a small element of randomness. This allows certain movies to have a second chance and be recommended to users, even if they haven't received high popularity or ratings initially.

### Potential issue 2 - Filter bubble

#### Description

The second feedback loop is the "Filter Bubble." This feedback loop occurs when a user's recommendations become increasingly personalized, showing the user only a very limited and homogeneous subset of all the films on the platform. 

The primary positive consequence of this feedback loop is that users will receive recommendations with a very high probability of enjoyment. However, the downside is that it confines users to a bubble where the content they consume is limited, giving them the impression that their preferences are generalizable to everyone. Moreover, these bubbles can be observed demographically and may contribute to reinforcing social biases. For example, a movie about a princess might be more recommended to little girls, thus reinforcing the social bias as it is more watched by them, even if little boys might like it too.

#### Detection

Analyzing the variety of films recommended to users and how it varies across user demographics can provide insights into the existence and impact of this type of feedback loop.

#### Mitigation

To mitigate this feedback loop, we can introduce a small element of randomization into everyone's recommendations. This helps recommend slightly more diverse types of films, breaking the homogeneity of personalized recommendations. Even though adding this random element may lead to a decrease in accuracy, it can also enable users to discover new interests. It strikes a balance between personalized recommendations and the exploration of diverse content.

## Analysis of Problems in log Data

## Fairness

### Dataset analysis

From our data analysis, it seems that social groups are distributed similarly between the ratings dataset and the users dataset. 

However, the distribution within the datasets is highly uneven between social groups themselves. As seen in the diagrams below, the dataset contains significantly more men than women, with the majority of individuals being between 24 and 35 years old, and students being much more represented than other occupations. 

We have also examined intersections of social groups. For example, we observed that, on average, women are older than men, and 11% of women are academics/educators compared to 2% of men. Regarding differences in occupations between women and men, we would like to emphasize that achieving balance in this intersection of social groups can be more complex than simply having a similar representation across occupations between women and men because a person's occupation is not an independent variable from their gender, unlike age and gender, which can be considered independent. 





### Quality of recommendations

We then analyzed the differences in the quality of recommendations based on gender, age, and occupation. After training our model on the train dataset, we divided the test dataset according to the gender, age, and occupation of the users, calculating the RMSE for these sub-datasets of the test dataset. 

We then displayed our results in the graphs below. We can observe that while there is only a small difference in RMSE between women and men, the disparity in RMSE is much greater when calculated based on age or occupation. The explanation for this could be that our demographic filter only takes into account the gender, and not other demographic factors such as age or occupation. Expanding the demographic filter to include these additional factors may help address the observed disparities in RMSE across different age groups and occupations. 

We notice also that for age, the less data we have for an age group, the more heterogeneous the RMSE is.



## Feedback loop

We decided to analyze the Echo Chamber feedback loop. To gather a new dataset of ratings and examine how ratings have evolved since the implementation of our model, we calculated the average ratings for each movie in our initial training set and in the new dataset we have just collected. We then compare the evolution of the ratings:

In an [Excel spreadsheet], we compared the correlation between the ratings given to these movies in our training dataset and the difference (both absolute and non-absolute) in the average ratings these movies received between the beginning of the semester and now. We have observes correlations, but these can be explained by an other factor than the Echo Chamber feedback loop. 

For example, we observe a very significant negative correlation when comparing with the non-absolute difference with the previous mean of ratings (r = -0.61221059, p = 3.0293E-250). This means that the most liked films are the ones that have lost the most in popularity, and the least liked films are the ones that have gained the most in popularity. However, this can be explained by the fact that movies that are nearly rated 5/5 have little room for improvement, and movies that are nearly rated 1/5 have little room for deterioration.




# Reflections on Recommendation Service
We had no shortage of problems, both technical and logistic, in developing our recommendation system. But in the end, we are happy to have encountered these problems as you learn more from these challenges than you would if everything worked perfectly fine. Here are 3 main challenges we dealt with:

### Cold start problem

**Challenge:**
One of our biggest challenges in developing a decent recommendation system was the lack of sufficient data, which limited the model's effectiveness and accuracy. Since we had a million users, we would need a substantial amount of data related to their watch history and ratings to give meaningful predictions. A major limitation with the collected data was duplication, since there was a log entry for each minute of the movie watched by a user. When we filtered these logs to extract unique entries, there was often a 70-80% reduction. For example, 5 million records would reduce to just 50,000. However, the cold start problem is common in recommendation systems and better data collection pipelines would have helped us improve our models. 

**Future Improvement:**
Moving forward, the focus will be on enhancing data collection and curation processes. We would need to set up a more robust system to collect, parse and store our logs. Acquiring more comprehensive and diverse datasets is a primary goal to improve the model's performance and reliability. 

### Telemetry Collection System
**Challenge:**
The initial challenge was managing a vast volume of logs. Loki was chosen for its promise of efficient storage, but it presented limitations in log retrieval as we could only retrieve 5,000 logs in one API request and it also averaged high CPU usage.


**Current Solution:**
Our team transitioned to a file-based system, opting to store logs in CSV files. This approach, while simpler, demands more storage and requires regular log cleanups. However, given the timeframe of the project, we decided this was a reasonable approach.


**Future Direction:**
With additional resources, the ideal solution would be to implement a database specifically for telemetry post-processing, aiming to enhance storage efficiency and retrieval capabilities.


### Load Balancing and Kubernetes

**Challenge:**
Implementing Kubernetes for load balancing and canary deployment was challenging, particularly due to the lack of root access and difficulties in configuring load balancers on  port 8082. We installed Docker using Kubernetes in Docker (KIND) which is alright for test environments. While we were able to set up all pods, deployments and services, and our service worked on port 80 of the team URL, we were not able to get it to work on port 8082, the port to which the simulator sends requests. We believe this was an ingress configuration issue, but could not figure out a solution. After putting in around three to four days of relentless effort into fixing this without success, we decided to move on. 


**Current Solution:**
Our team reverted to a simpler solution using an NGINX load balancer and bash scripts for canary deployment. All the containers are orchestrated using docker compose and Docker networks.

**Reflection:**
This part of the project highlighted the importance of balancing ambitious technological implementations with practical project management considerations. Kubernetes may have been a bit overkill for the scope of our project, but we wanted to kill two birds with one stone (load balancing and canary releases), which did not turn out very well. It is important to consider the scale of the project and available resources and limitations before venturing into a big technology.


## Reflections on Teamwork

### What went well
Our experience in this team has been quite a rollercoaster ride, but in the end, we believe that things turned out fairly well. We did not have the most ideal team kickoff, but we managed to settle disputes and patch up stronger after that. Over time, we understood each other better and our workability and compatibility increased. We also some exchanged some skills with each other and got to learn new things and workstyles from each other. Especially during M3, everyone was active and pitched in their ideas and collaborated well. The whole project helped us develop not only technical skills, but also some valuable interpersonal skills that we present below.

### Challenges
- **Ensuring that all team members feel included**: We started off on a not-so-good note as there were some initial conflicts with regard to the involvement of all team members. Some team members knew each other outside of the course and this led to misunderstandings with regard to involving other team members, though it was never the intention. However, these were resolved by talking things out and setting expectations right. After the small tiff, our team cohesion was quite good and we had no differences with each other for the most part.

- **Juggling commitments and varying availabilities**: Each team member had other commitments in terms of coursework from other classes or research projects.  This made it hard to find a common time to meet and to have a continual progress on the milestones. We were quite diligent with our meetings at the start, but as we got burdened with increasing workloads converging at the same time, the regularity of our meetings started to wane. We realize that this is typical and expected of a university student, so it is unfair to expect team members to devote a hundred percent of their time toward the project. But it is important to set up an appropriate workflow to work asynchronously and sync up regularly to ensure the project does not stall.

- **Responsiveness**: As the team got busier, we experienced communication gaps that slowed down our progress as a whole. Sometimes it used to be tough to get a response or acknowledgement from all team members when issues were being discussed or work was being allocated via WhatsApp. We realized that messaging, in general, tends to be a less engaging form of communication and actual conversations are important from time to time. 

- **Balancing expertise**: Though our team had varying domains of expertise that helped cover different aspects of the project, this also posed a challenge at times, especially in M1. As only one member in our team had solid hands-on machine learning experience, there was a high dependance on them to get things moving for M1. However, this was taken care of in subsequent milestones as the project's scope widened out. 

### Takeaways
Based on the challenges we discussed, here are the lessons we learnt to make future collaborations more productive and successful:

- **Being accountable and taking initiative**: The essence of teamwork is the team working together and playing an equally active role towards the advancement of the project, at least in projects in such a context. Despite one's packed schedule, if each team member takes personal responsibility to allot some time for the project at hand rather than leaving the heavylifting to just a few members, it can improve the overall quality of the project and can prevent cramming work close to the deadline.

- **Accept constructive criticism**: We did not have a major problem in this regard, but something that we observed in general is that it is important for one to be open minded and accept suggestions and different perspectives rather than be fixated on one's own idea. You should also be willing to accept that you don't know things and should be willing to learn from your teammates.

- **Pair programming is a good productivity booster**: We did not have extensive pair programming for the first two milestones, however, we did this fairly regularly for Milestone 3 and found it to be quite effective to bounce off ideas and get work done by sharing each other's expertise. We were able to complete our work faster and accomplish more this way. This is something we would definitely want to do more of in future projects.

### Some points worth highlighting about our implementation:

- Our commit messages are linked to the version of the data and model being committed. It gives a clear overview when observed within the repo as follows: (more description on why this is so - added in provenance)
![data-versioning](milestones/M3/artifacts/data-versioning.PNG)
![model-versioning](milestones/M3/artifacts/model-versioning.PNG)
![commit-version-txt](milestones/M3/artifacts/commit-version-txt.PNG)
(commit includes the version number which we save in the version txt)

- If the average response time of the deployed canary release is greater than 500ms then the canary release is abandoned. We get slack and email alerts for the same.
![canary-slack](milestones/M3/artifacts/canary-release-aborted-alert-slack-average-response-time.PNG)
![canary-email](milestones/M3/artifacts/canary-release-aborted-alert-email-average-response-time.PNG)

- If the rmse_score is acceptable after auto-updation of data and models then we proceed with deployment of the pipeline. Upon successful auto-updation, we get the following email. This is separate from the alerts we get after aborting a release which was deployed as canary but could not be switched to the main container due to average response time issue mentioned above.
![successful-deployment](milestones/M3/artifacts/successful-deployment-email.PNG)

- The screenshot of how our mysql database looks for per request tracking, has been attached under provenance.

- We have a nifty logging module. Following is the screenshot of how we create the logs. We tried to create ours in a similar fashion as a production app.
![logging](milestones/M3/artifacts/logging-sample.PNG)
