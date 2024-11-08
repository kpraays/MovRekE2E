# Meeting minutes

- Type of machine learning model to use: A combination of collaborative filtering and content-based recommendation
    - Why? The data we have is not particularly complicated - we just have a rating and the user's watch history. 
    - Will be easier to understand the implemented code completely
- Divide milestone into 4 main parts:
    1. Data creation and preprocessing - Luke
    2. Implementing ML model - Tamara and Rishabh
    3. Inference service - Aayush
    4. Deployment and CI/CD - Varun

- Specific tasks for the next week (also to be added as issues):
    - Create the dataset: Scrape Kafka log, write to CSV file
    - Preprocess data: Based on model parameters defined by ML engineers
    - Building the model: Working on implementing the actual recommender system using the decided ML techniques
    - Create the inference service: Look at Flask, cURL, model serving in ML; retrieve and parse request, send to ML model, serve output through API
    - Create Docker containers and other infrastructure for deployment

Other points/considerations discussed:
- Regarding training the model, training in collaborative filtering and content-based recommendation is almost instantaneous or ad-hoc. It is not as distinct a step as in deep learning.
- Discussed about the different types of content-based techniques: Recommendation based on explicit preferences given by user (rating), history and current trending content 
- We have to remember to focus also on the design and software engineering aspects, as the course is encompasses all of that.
