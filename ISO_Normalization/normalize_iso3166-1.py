import googlemaps
import pandas as pd
import time

def normalize(location):
    """
    Normalize location input based on Google Maps Geocode API.
    """

    # sleep to handle API rate limit
    time.sleep(1)

    # create googlemaps client - enter your API key
    # info: https://developers.google.com/maps/documentation/geocoding/get-api-key
    gmaps = googlemaps.Client(key='ENTER YOUR API KEY HERE')
    # get geocode result
    geocode_result = gmaps.geocode(location)

    # check if there are results
    if len(geocode_result) > 0:
        # iterate results
        for element in geocode_result:
            # only consider country results
            if 'country' in element['types']:
                # extract normalized location name
                for component in element['address_components']:
                    if 'country' in component['types']:
                        norm_location = component['long_name']

                # extract coords
                lat = element['geometry']['location']['lat']
                long = element['geometry']['location']['lng']
        else:
            norm_location = "No country element found"
            lat = 0.0
            long = 0.0
    else:
        norm_location = "Not results found"
        lat = 0.0
        long = 0.0

    return pd.Series({'location_normalized': norm_location,
                      'latitude': lat,
                      'longitude': long})

# config - set csv paths
csv_input_path = './ISO_source_files/iso3166-1_country_codes.csv'
csv_output_path = './ISO_out/iso3166-1_normalized.csv'
# read csv file
df = pd.read_csv(csv_input_path)
# normalize location name and add to dataframe
merged_df = df.merge(df['English short name'].apply(normalize),
                     left_index=True, right_index=True)
# save new df as csv
merged_df.to_csv(csv_output_path, index=False)
