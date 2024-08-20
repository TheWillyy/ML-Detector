import pandas as pd
import whois
from datetime import datetime
import time
from bs4 import BeautifulSoup
import re
import joblib
import urllib

# Import all the feature extraction functions from the main script
from extractnew import main as extract_features

def read_urls_from_csv(input_csv):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    return df

def save_features_to_csv(features, output_csv):
    # Save the features DataFrame to a CSV file
    features.to_csv(output_csv, index=False)

def extract_features_from_urls(df):
    features_list = []
    for index, row in df.iterrows():
        url = row['url']
        # Call the main function from your script to extract features
        features = extract_features(url)
        features_list.append(features)
    # Create a DataFrame from the list of features
    features_df = pd.DataFrame(features_list, columns=[
        'having_ip_address', 'url_length', 'shortening_service', 'having_at_symbol',
        'double_slash_redirecting', 'prefix_suffix', 'having_sub_domain', 'domain_registration_length',
        'favicon', 'https_token', 'url_of_anchor', 'links_in_tags', 'submitting_to_email',
        'abnormal_url', 'i_frame', 'age_of_domain', 'dns_record'
    ])

    result_df = pd.concat([df, features_df], axis=1)
    return result_df


if __name__ == "__main__":
    input_csv = 'balanced_urls.csv'  # Path to your input CSV file
    output_csv = 'final_output_dataset.csv'  # Path to your output CSV file

    # Read the URLs from the input CSV
    df = read_urls_from_csv(input_csv)

    # Extract features from the URLs
    features_df = extract_features_from_urls(df)


    # Save the extracted features to the output CSV
    save_features_to_csv(features_df, output_csv)

    print(f"Features extracted and saved to {output_csv}")
