# Import Libraries
import pickle
import pandas as pd

# Custom function imports
from auth import auth 
from api import get_genres
from clean import existing_artist_genres, add_genre_ids

# Load ML Model
model = pickle.load(open('genre_model_2023.pkl', 'rb'))

# Authenticate and get necessary objects
am, dd_singles, genre_list, gen_ids = auth('config.ini')

# Get existing genres for singles from your data source
dd_singles_no_genre_remaining, dd_singles_PA_genred = existing_artist_genres(dd_singles)

# Fetch genres for remaining singles from Apple Music API
df = get_genres(dd_singles_no_genre_remaining, genre_list, 25, am, model)

# Append the 2 DataFrames with new genres added
all_genred_singles = pd.concat([df,dd_singles_PA_genred])

# Add genre IDs to the dataframe
all_genred_singles = add_genre_ids(all_genred_singles, gen_ids)

# Export the final DataFrame to a CSV file
all_genred_singles.to_csv('api_genre_data.csv', index=False)