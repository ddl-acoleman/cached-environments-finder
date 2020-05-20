import urllib.request
import json
import csv

"""
This script will look at a source CSV (data.csv), which should be in the root
of this directory, and then look up the Domino environments based on the 
provided API Key, and add them by name to a output.csv file.

Input/Outputs:
data.csv - a list of cached image ids you would like translated to their real Domino name
output.csv - the environment names from the Domino API
apiKey - the Domino API Key for the environment you would like to pull data from
"""


def format_image_name(image_name):
    if "-" in image_name:
        split_environment_id = image_name.split("-")[1]
        if ":" in split_environment_id:
            return split_environment_id.split(":")[0]
        else:
            return split_environment_id
    else:
        print(f'image name {image_name} not in expected format')


# Use environment APIs to get actual name of environment from Id
def get_remote_environments():
    api_key = "<API-KEY-HERE>"
    headers = {'X-Domino-Api-Key': api_key}
    url = "<DOMINO-ENVIRONMENT-HERE>"
    request = urllib.request.Request(url, None, headers)

    with urllib.request.urlopen(request) as response:
        http_info = response.info()
        contents = response.read().decode(http_info.get_content_charset('utf8'))
        return json.loads(contents)


def write_environment_names(names):
    filename = "output.csv"
    with open(filename, 'w', newline='') as csv_file:
        for name in names:
            csv_file.write(name + '\n')

    print(f'Completed...Please check {filename} for Domino Environment names')


def read_csv():
    ids = []
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                ids.append(format_image_name(row[0]))
                line_count += 1

    print(f'Found {line_count - 1} environments. Proceeding to looking up their names...')
    return ids


def check_if_env_name_exists(envs, ids):
    environment_names = []
    for env in envs:
        if ids.__contains__(env['id']):
            environment_names.append(env["name"])
            print(f'Adding environment ({env["name"]}) to output.csv')
        else:
            print(f'Environment Id ({env["id"]}) not found in input data')

    write_environment_names(environment_names)


environments = get_remote_environments()
environment_ids = read_csv()
check_if_env_name_exists(environments['data'], environment_ids)
