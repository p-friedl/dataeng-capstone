import googlemaps
import pandas as pd
import time


def country_lookup(iso_code, ref_table):
    """
    Lookup Country names based on ISO codes from a Reference Table
    """

    # lookup matching row
    row = ref_table.loc[ref_table['Alpha-2 code'] == iso_code]
    # get country name and convert to string
    country = row['location_normalized'].to_string(index=False)
    # note: we use country[1:] to remove the first space which was created by
    # the to_string method before
    return pd.Series({'country_name': country[1:]})


def normalize(location):
    """
    Normalize location input based on Google Maps Geocode API.
    """

    # sleep to handle API rate limit
    time.sleep(0.10)

    # create googlemaps client - enter your API key
    # info: https://developers.google.com/maps/documentation/geocoding/get-api-key
    gmaps = googlemaps.Client(key='ENTER YOUR API CODE HERE')
    # get geocode result
    geocode_result = gmaps.geocode(location)

    # console output
    print(location)
    print(geocode_result)

    result_found = False

    # check if there are results
    if len(geocode_result) > 0:
        # iterate results
        for element in geocode_result:
            # only consider country results
            if ('administrative_area_level_1' in element['types']
                or 'locality' in element['types']
                or 'administrative_area_level_2' in element['types']
                or 'administrative_area_level_3' in element['types']
                or 'sublocality' in element['types']
                or 'establishment' in element['types']
                or 'colloquial_area' in element['types']
                or 'neighborhood' in element['types']
                ):
                # check if there are address_components
                if len(element['address_components']) > 0:
                    # extract normalized location name
                    for component in element['address_components']:
                        if ('administrative_area_level_1' in component['types']
                            or 'administrative_area_level_2' in component['types']
                            or 'locality' in component['types']
                            or 'establishment' in component['types']
                            or 'colloquial_area' in component['types']
                            ):
                            norm_location = component['long_name']
                            # extract coords
                            lat = element['geometry']['location']['lat']
                            long = element['geometry']['location']['lng']
                            # extract place_id
                            place_id = element['place_id']
                            # found result
                            result_found = True
                else:
                    norm_location = element['formatted_address']
                    # extract coords
                    lat = element['geometry']['location']['lat']
                    long = element['geometry']['location']['lng']
                    # extract place_id
                    place_id = element['place_id']
                    # found result
                    result_found = True

    # handle cases without result
    if not result_found:
        norm_location = "No results found"
        lat = 0.0
        long = 0.0
        place_id = ""

    return pd.Series({'location_normalized': norm_location,
                      'latitude': lat,
                      'longitude': long,
                      'place_id': place_id})

# config - set csv paths
iso_ref_input_path = './ISO_out/iso3166-1_normalized.csv'
csv_input_path = './ISO_source_files/iso3166-2_no_results_second_run.csv'
csv_output_path = './ISO_out/iso3166-2_normalized_second_run.csv'

# read csv file
iso_ref = pd.read_csv(iso_ref_input_path, keep_default_na=False)
df = pd.read_csv(csv_input_path, keep_default_na=False)

# lookup country name and add to dataframe
lookup_df = df.merge(df['country_code']
                     .apply(country_lookup, ref_table=iso_ref),
                     left_index=True, right_index=True)

lookup_df['combined_name'] = lookup_df['subdivision_name'] + \
                             ', ' + lookup_df['country_name']

# normalize location name and add to dataframe
merged_df = lookup_df.merge(lookup_df['combined_name'].apply(normalize),
                     left_index=True, right_index=True)
# save new df as csv
merged_df.to_csv(csv_output_path, index=False)
