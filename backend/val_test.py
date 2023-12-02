import requests

def send_post_request():
    url = "http://validate_package:5000"  # Update the URL as needed
    packagename = "hello_world"

    files = {'package': ('registry.tar.gz', open('static/registry.tar.gz', 'rb'))}
    data = {'packagename': packagename}

    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Example usage
result = send_post_request()
print(result)
