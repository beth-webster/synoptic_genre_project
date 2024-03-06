import pandas as pd

def existing_artist_genres(dd_singles):
    # Read csv
    dd_singles = pd.read_csv(dd_singles, encoding='unicode_escape')
    
    # Drop rows with OOD genres
    mask_rockpop = dd_singles[' Genre'] != 'Rock/Pop (pre 2004)'
    dd_singles = dd_singles[mask_rockpop].copy()  
    
    # Extract primary artist from the ARTIST column using regex    
    dd_singles['Primary_artist'] = dd_singles[' Artist'].str.extract(r'^([^/&]+)(?:[/&]| FT )')
    
    # Identify rows where primary artist could not be extracted and fill them with the original artist value
    mask_primaryart = dd_singles['Primary_artist'].isnull()
    dd_singles.loc[mask_primaryart, 'Primary_artist'] = dd_singles.loc[mask_primaryart, ' Artist'].copy()
    
    # Filter rows with missing genre information
    dd_singles_no_genre = dd_singles[dd_singles[' Genre'].isnull()]
    
    # Filter rows with genre information
    dd_singles_genred = dd_singles.dropna(subset=[' Genre'])
    
    # Group by primary artist and genre, and reset index
    grouped_artist_genres = dd_singles_genred.groupby(['Primary_artist', ' Genre']).size().reset_index()[['Primary_artist', ' Genre']]
    
    # Remove duplicate primary artist entries
    artist_genres_no_dupes = grouped_artist_genres[~grouped_artist_genres['Primary_artist'].duplicated(keep=False)]
    
    # Rename the GENRE column in artist_genres_no_dupes to primary_artist_genre
    artist_genres_no_dupes = artist_genres_no_dupes.rename(columns={' Genre': 'Primary_Artist_Genre'})
    
    # Merge dataframes to fill missing genre information based on primary artist
    result_df = dd_singles_no_genre.merge(artist_genres_no_dupes, how='left', on='Primary_artist')
    
    # Create a DataFrame for all singles with no genre assigned for the Primary Artist
    dd_singles_no_genre_remaining = result_df[result_df['Primary_Artist_Genre'].isnull()]
    
    # Create a DataFrame for all singles with a genre assigned by the Primary Artist
    dd_singles_PA_genred = result_df[~result_df['Primary_Artist_Genre'].isnull()]
    
    # Drop the unnecessary columns
    dd_singles_PA_genred = dd_singles_PA_genred.drop(['Primary_artist', ' Genre', ' Genre ID'], axis=1)
    dd_singles_no_genre_remaining = dd_singles_no_genre_remaining.drop([' Genre', ' Genre ID', 'Primary_artist', 'Primary_Artist_Genre'], axis=1)

    # Rename the primary_artist_genre column in dd_singles_PA_genred to primary_artist_genre
    dd_singles_PA_genred = dd_singles_PA_genred.rename(columns={'Primary_Artist_Genre': ' Genre'})    
    
        
    return dd_singles_no_genre_remaining, dd_singles_PA_genred



def add_genre_ids(df, gen_ids):
    gen_ids = pd.read_csv(gen_ids)
    df = df.merge(gen_ids, how='left', on=' Genre')
    
    return df