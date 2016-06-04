import csv
import geocoder

from pprint import pprint


def geocode_addresses(input_file, output_file):
    with open(input_file) as f:
        reader = csv.DictReader(f)
        data = list(reader)

    """
    geocodes looks like this:

    {
        'address1': [lat1, lng1],
        'address2': [lat2, lng2],
    }
    """
    geocodes = {}

    for row in data:
        address = '{0}, {1}, {2}'.format(row['det_facility'], row['city'], row['state'])

        # If address is not a key of geocodes, we need to geocode
        if address not in geocodes.keys():
            g = geocoder.google(address)
            geocodes[address] = {
                'lat': g.lat,
                'lng': g.lng,
            }

        latlng = geocodes[address]
        row['lat'] = latlng['lat']
        row['lng'] = latlng['lng']

    with open(output_file, 'w') as f:
        fieldnames = ['date', 'lift_reason', 'det_facility', 'city', 'state', 'detainer_type', 'lat', 'lng']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(data)


if __name__ == '__main__':
    geocode_addresses('pa_detainers.csv', 'pa_detainers_processed.csv')
    print('Done.')
