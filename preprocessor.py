import re
import pandas as pd
from urlextract import URLExtract

def preprocessor(data):
    # Define the pattern to extract date, time, sender, and message
    pattern = r"(\d{1,2}/\d{1,2}/\d{2}),\s(\d{1,2}:\d{2})\s([AP]M)\s-\s(.+?):\s(.+)"

    # Find all messages using the pattern
    messages = re.findall(pattern, data)

    # Create DataFrame from the extracted messages
    df = pd.DataFrame(messages, columns=['Date', 'Time', 'AM/PM', 'Sender', 'Message'])

    # Combine Date and Time columns into a single datetime column
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'] + ' ' + df['AM/PM'], format='%m/%d/%y %I:%M %p')

    # Add new columns for Year, Month (in name format), Day, Hour, and Minute
    df['Year'] = df['DateTime'].dt.year
    df['Month'] = df['DateTime'].dt.month_name()
    df['Day'] = df['DateTime'].dt.day
    df['Hour'] = df['DateTime'].dt.hour
    df['Minute'] = df['DateTime'].dt.minute

    return df

def count_media_messages(df):
    return df[df["Message"] == '<Media omitted>'].shape[0]

def count_links(df):
    extractor = URLExtract()
    return df['Message'].apply(lambda x: len(extractor.find_urls(x))).sum()

def load_stopwords(file_path):
    with open(file_path, 'r') as file:
        stop_words = file.read().splitlines()
    return set(stop_words)
