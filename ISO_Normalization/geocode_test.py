import googlemaps

location = "Turks and Caicos Islands (the)"
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


print("name: " + norm_location)
print("latitude: " + str(lat))
print("longitude: " + str(long))
print("======================")
print(geocode_result)
