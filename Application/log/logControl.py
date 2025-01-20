#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
from Application.public import post_url

def log_to_server(data, url=post_url):
    """
    Sends log data to the server via an HTTP POST request.

    Parameters:
        data (dict): The log data to send.
        url (str): The base URL of the server. Defaults to `post_url`.

    Returns:
        response (requests.Response): The response object from the server if the request succeeds.
    """
    try:
        response = requests.post(f"{url}/log", json={"data": data})
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response
    except requests.RequestException as e:
        print(f"HTTP request error: {e}")
