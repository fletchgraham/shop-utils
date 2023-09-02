"""Update a listing with the Etsy API.

Follow the getting started Etsy API tutorial to generate the oauth token:
https://developers.etsy.com/documentation/tutorials/quickstart

"""

import requests

def update_etsy_listing(listing_id, updated_data):
    # Define the endpoint URL
    endpoint_url = f"https://api.etsy.com/v3/application/shops/<YOUR_SHOP_ID_HERE_AS_INT>/listings/{listing_id}"

    # Define the headers
    headers = {
        "x-api-key": "YOUR_API_KEY_HERE",
        "Authorization": "Bearer YOUR_OAUTH_TOKEN_HERE",
        "Content-Type": "application/json"
    }

    # Send the PATCH request
    response = requests.patch(endpoint_url, headers=headers, json=updated_data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Listing updated successfully!")
        return response.json()
    else:
        print(f"Failed to update listing! Response Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Your Etsy API key

    # The ID of the listing you want to update
    LISTING_ID = "YOUR_LISTING_ID_HERE"

    # The data you want to update, for example, changing the title
    data_to_update = {
        "title": "NEW TITLE HERE"
    }

    update_etsy_listing(LISTING_ID, data_to_update)


