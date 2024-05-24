import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from collections import Counter
import string
import pandas as pd
import emoji

st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocessor(data)

    # Ensure the 'Date' column is in datetime format
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['Date'] = df['DateTime'].dt.date

    st.dataframe(df)

    # Fetch unique senders
    sender_list = df["Sender"].unique().tolist()
    # Filter out numeric senders
    sender_list = [sender for sender in sender_list if not sender.replace(" ", "").isdigit()]
    # Sort the sender list
    sender_list.sort()
    # Insert 'Overall' at the beginning of the sender list
    sender_list.insert(0, "Overall")
    selected_sender = st.sidebar.selectbox('Show analysis with respect to', sender_list)

    if st.sidebar.button("Show Analysis"):
        if selected_sender == "Overall":
            filtered_df = df
        else:
            filtered_df = df[df["Sender"] == selected_sender]

        total_messages = filtered_df.shape[0]
        total_words = filtered_df['Message'].apply(lambda x: len(x.split())).sum()
        total_media_messages = preprocessor.count_media_messages(filtered_df)
        total_links = preprocessor.count_links(filtered_df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.write(total_messages)

        with col2:
            st.header("Total Words")
            st.write(total_words)

        with col3:
            st.header("Media Messages")
            st.write(total_media_messages)

        with col4:
            st.header("Links Shared")
            st.write(total_links)

        # Check if it's a group chat
        if len(sender_list) > 2:  # More than 'Overall' and one individual sender
            st.header("Top 5 Active Users")
            top_users = filtered_df['Sender'].value_counts().head(5)
            fig, ax = plt.subplots()
            ax.bar(top_users.index, top_users.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        # Generate and display the word cloud
        st.header("Word Cloud")
        all_text = ' '.join(filtered_df['Message'])
        wordcloud = WordCloud(width=800, height=400, max_words=200, background_color='white').generate(all_text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        # Perform sentiment analysis
        def get_sentiment(message):
            return TextBlob(message).sentiment.polarity

        filtered_df['Sentiment'] = filtered_df['Message'].apply(get_sentiment)
        average_sentiment = filtered_df['Sentiment'].mean()

        # Display the average sentiment with a header and description
        st.header("Average Sentiment Score")
        st.write(f"{average_sentiment:.2f}")
        st.markdown("""
        **Interpretation of Sentiment Score:**
        - **Negative Values (e.g., -0.5)**: Indicate a negative sentiment overall.
        - **Zero (0)**: Indicates a neutral sentiment.
        - **Positive Values (e.g., 0.5)**: Indicate a positive sentiment overall.
        """)

        # Most used words (excluding stop words, media messages, and group notifications)
        st.header("Most Used Words")
        stop_words = preprocessor.load_stopwords("NLTK's list of english stopwords")  # Update this to the correct path if needed

        all_words = ' '.join(filtered_df['Message'])
        all_words = all_words.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
        words = all_words.lower().split()
        words = [word for word in words if word not in stop_words]

        word_freq = Counter(words)
        most_common_words = word_freq.most_common(15)

        most_common_df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])
        st.dataframe(most_common_df)

        fig, ax = plt.subplots()
        ax.bar(most_common_df['Word'], most_common_df['Frequency'])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # Emoji Analysis
        def extract_emojis(s):
            return [c for c in s if c in emoji.EMOJI_DATA]

        all_emojis = [e for message in filtered_df['Message'] for e in extract_emojis(message)]
        emoji_freq = Counter(all_emojis)

        st.header("Emoji Analysis")
        st.write("Total Emojis:", len(all_emojis))
        st.write("Unique Emojis:", len(emoji_freq))

        # Create a DataFrame for the emojis and their frequencies
        top_n = 20  # Number of top emojis to display
        emoji_df = pd.DataFrame(emoji_freq.items(), columns=['Emoji', 'Frequency']).sort_values(by='Frequency', ascending=False).head(top_n)
        st.dataframe(emoji_df)

        fig, ax = plt.subplots(figsize=(12, 6))  # Increase figure size
        ax.barh(emoji_df['Emoji'], emoji_df['Frequency'])  # Horizontal bar chart
        ax.set_title('Top Emojis Frequency')
        plt.xlabel('Frequency')  # Add x-axis label
        plt.ylabel('Emoji')  # Add y-axis label
        st.pyplot(fig)

        # Time Series Analysis
        st.header("Time Series Analysis")
        # Create a new column 'Month-Year' in the DataFrame for grouping
        filtered_df['Month-Year'] = filtered_df['DateTime'].dt.strftime('%B-%Y')
        # Group the DataFrame by 'Month-Year' and count the number of messages
        time_series_df = filtered_df.groupby('Month-Year').size().reset_index(name='Message Count')
        # Convert 'Month-Year' to datetime for sorting
        time_series_df['Month-Year'] = pd.to_datetime(time_series_df['Month-Year'])
        # Sort the DataFrame by 'Month-Year'
        time_series_df = time_series_df.sort_values('Month-Year')
        # Plot the time series data
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(time_series_df['Month-Year'], time_series_df['Message Count'], marker='o')
        ax.set_title('Number of Messages Over Time')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Month-Year')
        plt.ylabel('Number of Messages')
        st.pyplot(fig)

        # Daily Time Series Analysis
        st.header("Daily Time Series Analysis")
        # Group the filtered DataFrame by date and count the number of messages
        daily_time_series_df = filtered_df.groupby(filtered_df['Date']).size().reset_index(name='Message Count')
        daily_time_series_df['Date'] = pd.to_datetime(daily_time_series_df['Date'])
        daily_time_series_df = daily_time_series_df.sort_values('Date')
        # Plot the daily time series data
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_time_series_df['Date'], daily_time_series_df['Message Count'], marker='o')
        ax.set_title('Number of Messages Per Day')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Date')
        plt.ylabel('Number of Messages')
        st.pyplot(fig)

        # Weekly Activity Analysis
        st.header("Weekly Activity Analysis")
        # Create a new column for the day of the week
        filtered_df['Day of Week'] = filtered_df['DateTime'].dt.day_name()
        weekly_activity_df = filtered_df.groupby('Day of Week').size().reset_index(name='Message Count')
        weekly_activity_df = weekly_activity_df.sort_values(by='Message Count', ascending=False)  # Sort by message count
        # Plot the weekly activity data
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(weekly_activity_df['Day of Week'], weekly_activity_df['Message Count'])
        ax.set_title('Number of Messages by Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Number of Messages')
        st.pyplot(fig)

        # Monthly Activity Analysis
        st.header("Monthly Activity Analysis")
        # Create a new column for the month
        filtered_df['Month'] = filtered_df['DateTime'].dt.strftime('%B')
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        monthly_activity_df = filtered_df.groupby('Month').size().reindex(month_order).reset_index(name='Message Count')
        monthly_activity_df = monthly_activity_df.sort_values(by='Message Count', ascending=False)  # Sort by message count
        # Plot the monthly activity data
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(monthly_activity_df['Month'], monthly_activity_df['Message Count'])
        ax.set_title('Number of Messages by Month')
        plt.xlabel('Month')
        plt.ylabel('Number of Messages')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
