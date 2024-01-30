from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import requests
from xml.etree import ElementTree as ET

# URL of the sitemap
# sitemap_url = 'https://example.com/sitemap.xml'

sitemap_url = 'your site map url'

# this is the file you downloaded from google cloud
JSON_KEY_FILE = "service_account_file.json"

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


# Authorize credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    JSON_KEY_FILE, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())

# Fetch the sitemap XML
response = requests.get(sitemap_url)
if response.status_code != 200:
    print("Error fetching sitemap XML")
    exit()
else:
    print("Sitemap XML fetched successfully")
sitemap_xml = response.text

# Parse the sitemap XML
sitemap_root = ET.fromstring(sitemap_xml)

# Iterate over URLs in the sitemap
for child in sitemap_root:
    url = child[0].text  # Assuming the <loc> tag contains the URL

    # Build the request body
    content = {}
    content['url'] = url
    content['type'] = "URL_UPDATED"
    json_content = json.dumps(content)

    response, content = http.request(
        ENDPOINT, method="POST", body=json_content)
    result = json.loads(content.decode())

    # Handle the result as needed
    print(result)
