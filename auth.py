import configparser
import applemusicpy

def auth(config_file):
    # Create a ConfigParser object to read the configuration file
    config = configparser.ConfigParser()
    # Read config file
    credentials = config.read(config_file)
    
    # Retrieve parameters from the config file
    secret_key = config.get('itunesapi', 'secret_key')
    key_id = config.get('itunesapi', 'key_id')
    team_id = config.get('itunesapi', 'team_id')
    track_data = config.get('csv', 'app_report')
    gen_ids = config.get('csv', 'ids')
    genre_list = config.get('csv', 'genres')
    
    # Initialise AppleMusic object for API authentication
    am = applemusicpy.AppleMusic(secret_key, key_id, team_id)
    
    return am, track_data, genre_list, gen_ids