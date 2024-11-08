# online evaluation strategy


We will determine the performance of our system while it is deployed based on the following factors:
- online evaluation metric (which we will define and explain below)
- response time of the API

## Online evaluation metric

We have defined a custom scoring metric which we use to track the performance of the model and compare it with how close is it to what the user expects. Usually, online evaluation involves A/B tests which means there should be another recommendation model to compare our recommendation with (as we do not have access to ground truth). But in our case, instead of contrasting and comparing our recommendations with another model, we instead looked at the logs and the ratings from the user in real time. Our rationale was something along the lines of the phenomenon observed while watching youtube. Say, the user is watching some video and he/she gets a bunch of recommendations and they may also get asked "what do you think about this recommendation?". Borrowing from that idea we thought, what if we look at the logs in real time to check for the ratings and latest watch history of the user.

So our online evaluation works like this: We look at the latest ratings provided by the user. For that user and the movie combination, we look at how much of the movie was watched by the user. Then we compare it with our recommendation. If the movie which the user rated high and watched a lot of is indeed part of our recommendation, then our recommendation was good. Lastly, we record the response time to get this recommendation and record this to track the performance across a random sample of users.

This approach makes sure that we make use of the telemetry information provided from the logs (in real systems, we presume there will more details available in the telemetry data including user behavior on the website, which is not present in the available logs. But we do have information on watchtime and ratings which we use.)

### How did we work with real time data?
To work with the log data in real time, we found that utilising promtail (logs forwarding), loki (log aggregationn) and grafana (visualisation) is clever solution. Intially, we were using these tools for log collection and monitoring but we discovered that they can be exposed over API to gain access to the log data so that it can be used as dataset which being updated in the real time from kafka stream. So, we wrote wrapper for the above mentioned tools to send API requests with the queries we wanted to obtain the results for our online processing.

### How does the metric work?

Following the steps to evaluate the metric:
1. Get the rating provided by any random user from the ratings exposed view on grafana.
2. Get the latest watched movie time for that user and movie combination.
    - If that user-movie combination is not found in the history exposed view, then look for a new user-movie combination in step-1.
3. Find the recommendation for that user from our model.
    - Count the response time to make that recommendation.
4. Record all the metrics and do the calculation. Upload everything back to grafana for creating visualisation of model performance.

### What is the calculation involved?

For any considered user-movie sample: We will refer to it as sample-user and sample-movie from here on.
We will have our own list of recommendations from the system. There will be 20 movies in our recommendation output with the movies first ranked higher than the ones at the end of the list.

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
Scale our recommended movie based on how the user perceived that recommendation depending on how much of the movie was watched and what rating was given.

Recommended_list_score x Ratings_score x runtime_score = predicted movie scaled score to tell us appropriiate the recommendation was.

#### What does the metric mean? How to interpret it?
The intention behind this metric was create a way to measure the performance of the model with what the user expects as we are aware of the user's preferences based on the telemetry we capture. Care was taken to ensure that we do not end up with zero values while multiplying the scores. 
We capture the following trends in our metric:
- How highly ranked was the sample-movie in the list of recommended movies or if the sample-movie was even part of the recommendation at all?
- What did the user feel about the movie? (captured by the rating they gave to the movie)
- Apart from feeling, how did the user actually act for that movie? (captured based on how much of the movie did they actually end up watching)
- How much time did we take to give our recommendation?


After randomly sampling a group of users, we will calculate our online evaluation metric for them and obtain a revolving average score for our recommendation. We will keep track of this score along with the time to gauge how our model is performing across the time. This will help us to determine if the model is improving over time and compare performances of different versions of our model.

The score range will be `[0.01-10]/10 x [1-5]/5 x [1-5]/5 = [0.00004-1]` with 1 being the best possible recommendation and 0.00004 being the worst possible recommendation.
(because we do not consider 0 rating by the user in our dataset)