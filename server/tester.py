import joblib
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import re
import whois
import datetime
from urllib.parse import urlparse
import socket

# Load the trained models
best_rf_model = joblib.load('best_random_forest_model.joblib')
xgb_model = joblib.load('xgb_model.joblib')

def extract_port(url):
    parsed_url = urlparse(url)
    try:
        return parsed_url.port if parsed_url.port else (443 if parsed_url.scheme == "https" else 80)
    except ValueError:
        return None

def is_non_standard_port(port):
    return 1 if port is not None and port not in [80, 443] else 0

def count_dots(url):
    return url.count('.')

def count_special_chars(url):
    special_chars = r'[@\-_&=%]'
    return len(re.findall(special_chars, url))

def has_ip_address(url):
    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    return 1 if re.search(ip_pattern, url) else 0

def url_length(url):
    return len(url)

def domain_age(url):
    try:
        domain_info = whois.whois(url)
        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if isinstance(creation_date, str):
            try:
                creation_date = datetime.datetime.strptime(creation_date, '%Y-%m-%d')
            except ValueError:
                try:
                    creation_date = datetime.datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print(f"Unknown date format for {url}: {creation_date}")
                    return None

        if creation_date and isinstance(creation_date, datetime.datetime):
            return (datetime.datetime.now() - creation_date).days
        else:
            return None
    except Exception as e:
        print(f"Error fetching domain age for {url}: {e}")
        return None

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching URL content: {e}")
        return None

def contains_phishing_keywords(content):
    phishing_keywords = ['verify', 'login', 'update', 'security']
    return any(keyword in content.lower() for keyword in phishing_keywords)

def has_hidden_iframes(html):
    soup = BeautifulSoup(html, 'html.parser')
    iframes = soup.find_all('iframe', style=lambda value: value and 'display:none' in value)
    return len(iframes) > 0

def extract_features_from_url(url):
    html = get_html_content(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        port = extract_port(url)

        features = {
            'port': port or 80,  # Default to 80 if port is None
            'script_count': len(soup.find_all('script')),
            'iframe_count': len(soup.find_all('iframe')),
            'embed_count': len(soup.find_all('embed')),
            'has_javascript': 1 if soup.find('script') else 0,
            'contains_phishing_keywords': int(contains_phishing_keywords(text)),
            'has_hidden_iframes': int(has_hidden_iframes(html)),
            'domain_age': domain_age(url) or 0,
            'non_standard_port': is_non_standard_port(port),
            'num_dots': count_dots(url),
            'special_chars_present': count_special_chars(url),
            'ip_used': has_ip_address(url),
            'url_length': url_length(url)
        }
        return features
    else:
        print("Failed to fetch or process the URL.")
        return None

def predict(url):
    features = extract_features_from_url(url)
    if features is None:
        return {'error': 'Failed to fetch or process the URL'}
    
    # Ensure the DataFrame has the correct column names
    column_names = [ 'port', 'non_standard_port', 'url_length', 'num_dots', 'special_chars_present', 'ip_used', 'domain_age', 'script_count', 'iframe_count', 'embed_count', 'has_javascript']
    
    # Ensure all features are present in the DataFrame
    input_features = {key: features.get(key, 0) for key in column_names}
    
    input_df = pd.DataFrame([input_features], columns=column_names)
    
    # Make predictions using the loaded models
    best_rf_prediction = best_rf_model.predict(input_df)
    xgb_prediction = xgb_model.predict(input_df)
    
    # Determine if the content is malicious or not
    is_malicious = (best_rf_prediction[0] == 1 or xgb_prediction[0] == 1)
    
    # Return a result dictionary with serializable values
    response = {
        'is_malicious': bool(is_malicious)  # Ensure the boolean is correctly serialized
    }
    return response

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predict_url.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    result = predict(url)
    
    # Debug print the result before serializing
    print(f"Result before serialization: {result}")

    try:
        print(json.dumps(result, indent=4))
    except TypeError as e:
        print(f"Serialization error: {e}")
