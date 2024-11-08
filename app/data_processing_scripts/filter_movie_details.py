import requests
import csv

# Function to send a cURL request and return the filtered data
def send_curl_request(movie_id):
    url = fr"http://fall2023-comp585.cs.mcgill.ca:8080/movie/{movie_id}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            
            # Filter out the desired parameters
            filtered_data = {
                "adult": data.get("adult", ""),
                "genres": [genre["name"] for genre in data.get("genres", [])],
                "runtime": data.get("runtime", ""),
                "vote_average": data.get("vote_average", ""),
                "spoken_languages": [lang["name"] for lang in data.get("spoken_languages", [])],
            }
            
            return filtered_data
        else:
            print(f"Request for {movie_id} failed with status code {response.status_code}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request for {movie_id} failed with error: {str(e)}")
        return None

def filter_response(data_path):
    # Open the CSV file with movie data
    # 'final_cleaned_movie_list.csv'
    try:
        with open(data_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            
            # Skip the header row if it exists
            next(csvreader, None)
            
            # Create a new CSV file to store filtered data
            with open('filtered_responses.csv', 'w', newline='') as filteredfile:
                csvwriter = csv.writer(filteredfile)
                csvwriter.writerow(['movie_id', 'adult', 'genres', 'runtime', 'vote_average', 'spoken_languages'])  # Header row
                
                # Loop through each row in the CSV file
                for row in csvreader:
                    movie_id = row[1]
                    
                    # Send the cURL request for each movie_id
                    filtered_data = send_curl_request(movie_id)
                    
                    # Save the filtered data along with the movie_id to the filtered responses CSV file
                    if filtered_data:
                        csvwriter.writerow([movie_id, filtered_data["adult"], ", ".join(filtered_data["genres"]), 
                                            filtered_data["runtime"], filtered_data["vote_average"], 
                                            ", ".join(filtered_data["spoken_languages"])])

        # Close both CSV files
        csvfile.close()
        filteredfile.close()
        return "OK"
        
    except FileNotFoundError:
        raise FileNotFoundError("file not found")

