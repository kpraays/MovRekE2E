Data Quality Requirements
### What makes data "high quality" in our context? 
_Common dimensions of data quality include accuracy, completeness, consistency, reliability, and timeliness._

Our pipeline for data was as follows:
- Save the logs to flat files.
- Preprocess the flat files to clean data collected. Inspection was done to identify any obvious issues with the data collected. We found missing values and spurious entries. We dropped all those records.
- Filter and segregate data collected according to the type of data files. Convert them to csv files.

- The user data was scrapped from the simulator API for 1 million users.
- Movie attributes were scrapped from the API for the items obtained from kafka logs.
    - As an enhancement, we loaded the movie attributes and imdb ratings from external sources too for M2. This was done using the "tmdb_id" attribute we had for each movie
    - From the kafka logs, sometimes we would get made up movie details. Since it was mentioned in the requirements of the project that the simulator is using imdb movie database to generate logs, we went directly to the external source to avoid such spurious logs.
- Kafka logs are responsible for giving watch history, telemetry and ratings by each user (whether the liked the movie or not). We loaded the kafka logs to grafana monitoring. Further, we found that grafana can be used a database to serve the logs in response to API queries. So to retrieve real time information about the system for online evaluation, we added processing at the destination endpoint of those API queries to get filtered data outputs.
