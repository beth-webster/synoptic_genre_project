import pandas as pd
import requests


def get_genres(data, genre_list, batch_size, am, model):

    # Extract ISRC codes from the data
    isrcs = ["" + str(value) + "" for value in data.iloc[:, 0]]
    
    # Create empty list to store API output
    api_output = []
    # Loop through ISRCs in batches and fetch genre information from API   
    for i in range(0,len(isrcs),batch_size):
        isrcs_batch = isrcs[i:i+batch_size]
        batch_output = []
        processed_isrcs = set()
        try:
            # Call API to fetch genre information for the current batch of ISRCs
            json_output = am.songs_by_isrc(isrcs_batch, storefront='gb')
            # Process API response        
            for item in json_output['data']:
                isrc = item['attributes']['isrc']
                if (isrc in isrcs_batch) and (isrc not in processed_isrcs):  # Check if the ISRC is in the list of queried ISRCs
                    genres = item['attributes']['genreNames']
                    batch_output.append([isrc, genres])
                    processed_isrcs.add(isrc)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            continue  # Skip to the next batch if an HTTP error occurs
            
        # Extend the main API output list with the current batch output    
        api_output.extend(batch_output)
   
    # Create DataFrame from the API output
    df = pd.DataFrame(api_output, columns=['ISRC', 'GENRES'])
    
    # Merge the API output with the original track data based on ISRC
    merged_df = pd.merge(data, df, on='ISRC')

    # Read potential genres from the provided genre list
    unique_genres = pd.read_csv(genre_list)
    genres = ["" + str(value) + "" for value in unique_genres.iloc[:, 0]]

    # Create OHE DataFrame for genres to use in the ML model
    genre_df = pd.DataFrame()
    for genre in genres:
        genre_df[genre] = merged_df['GENRES'].apply(lambda genre_list: 1 if genre in genre_list else 0)
        
    # Concatenate the OHE genre DataFrame with the merged DataFrame
    df_ohe_genres = pd.concat([merged_df, genre_df], axis=1)
    
    # Drop unnecessary columns for model input
    model_input = df_ohe_genres.drop(['ISRC', ' Product ID', ' Title', ' Artist', 'GENRES'], axis=1)
    
    # Make predictions using the ML model
    genre_predictions = model.predict(model_input)
    
    # Create a DataFrame from the predictions
    pred_genre_col = pd.DataFrame(genre_predictions, columns=[' Genre'])
    
    # Concatenate the prediction column with the OHE genre DataFrame
    genred_df = pd.concat([df_ohe_genres, pred_genre_col], axis=1)
    
    # Select columns and return the DataFrame
    df = genred_df[['ISRC', ' Product ID', ' Title', ' Artist', ' Genre']]
    
    return df