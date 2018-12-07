
# coding: utf-8

# In[4]:


from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib


try:
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# In[5]:


API_KEY= 'LKgaKMZXmP9o6aHgkcTmxZpkjCbKPOhsDGCzTqHAHOLzKYqKPJ3ZFoa74f9fq5Xq0BYFCtsOTILhzgNYyepzH0J0A1W9ySNmuWnsjxVtV_6mpxnnaFCn32j78FPnW3Yx' 


# In[6]:


API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
REVIEWS_API_URL = '/reviews'


# In[7]:


DEFAULT_TERM = 'Restaurant'
DEFAULT_LOCATION = 'college park, MD'
SEARCH_LIMIT = 50


# In[8]:


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


# In[9]:


def search(api_key, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


# In[18]:


def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    print("--------------------------------------------------------")
   
    business_path = BUSINESS_PATH + business_id
    

    return request(API_HOST, business_path, api_key)


# In[19]:


def reviews_query(api_key, business_id ):
        """
            Query the Yelp Reviews API.
            
            documentation: https://www.yelp.com/developers/documentation/v3/business_reviews
            required parameters:
                * id - business ID
        """
        print("--------------------------------------------------------")
   
        business_path = BUSINESS_PATH + business_id + REVIEWS_API_URL

        return request(API_HOST, business_path, api_key)


# In[23]:


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return
    
    for i  in range(0,50):
        businesses_review = get_business(API_KEY, businesses[i]['id'])
        print("Business Id: " + businesses[i]['id'])
        print("Business Name: " + businesses[i]['name'])
        pprint.pprint(businesses_review, indent=3)
    
    


# In[24]:


def main():
    
    try:
        query_api('dinner', 'college park, MD')
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


# In[25]:


main()

