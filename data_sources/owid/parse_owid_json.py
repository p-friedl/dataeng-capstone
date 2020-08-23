import json


def main():
    """Parse and clean OWID JSON."""

    # read source file
    with open("owid-covid-data.json", "r") as file:
        # convert to dict
        owid = json.loads(file.read())

        # extract data
        for country_code, country_data in owid.items():
            parsed_data = []

            if 'continent' in country_data:
                continent = country_data['continent']
            else:
                continent = ""

            if 'location' in country_data:
                location = country_data['location']
            else:
                location = ""

            if 'population' in country_data:
                population = int(country_data['population'])
            else:
                population = 0

            if 'population_density' in country_data:
                population_density = country_data['population_density']
            else:
                population_density = 0.0

            if 'median_age' in country_data:
                median_age = country_data['median_age']
            else:
                median_age = 0.0

            for entry in country_data['data']:
                date = entry['date']

                if 'total_tests' in entry:
                    total_tests = int(entry['total_tests'])
                else:
                    total_tests = 0

                if 'new_tests' in entry:
                    new_tests = int(entry['new_tests'])
                else:
                    new_tests = 0

                if 'new_tests_smoothed' in entry:
                    new_tests_smoothed = int(entry['new_tests_smoothed'])
                else:
                    new_tests_smoothed = 0

                if 'tests_units' in entry:
                    tests_units = entry['tests_units']
                else:
                    tests_units = "undefined"

                if 'stringency_index' in entry:
                    stringency_index = entry['stringency_index']
                else:
                    stringency_index = 0.0

                # structure data
                parsed_data.append(json.dumps({
                    'iso_code': country_code,
                    'continent': continent,
                    'location': location,
                    'population': population,
                    'population_density': population_density,
                    'date': date,
                    'median_age': median_age,
                    'total_tests': total_tests,
                    'new_tests': new_tests,
                    'new_tests_smoothed': new_tests_smoothed,
                    'tests_units': tests_units,
                    'stringency_index': stringency_index
                    }))

            # exclude world aggregation
            if location != 'World':
                # group into separate output files per country_code
                # to avoid exceeding Redshift JSON file size limit
                output_file = '{}.json'.format(country_code)
                with open(output_file, 'w') as file:
                    file.write(''.join(parsed_data))


if __name__ == "__main__":
    main()
