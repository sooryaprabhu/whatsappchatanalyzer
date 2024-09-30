## WhatsApp Chat Analyzer (NLP Project)
❗️❗️Note: This code is designed exclusively for controlling volume on macOS. It will not work on Windows or Linux. Sorry for the inconvenience, but feel free to update the code for other platforms. If you’re having trouble, you can also contact me for assistance.

![whatsapp_Chat_Analyzer_Image_1](https://github.com/user-attachments/assets/407b2472-cfea-4561-939b-ac3d945af733)

#Overview

The WhatsApp Chat Analyzer is a data analysis tool I developed to extract valuable insights from WhatsApp group conversations. Using Python and Streamlit, the project focuses on providing users with a comprehensive understanding of their chat dynamics, including communication patterns, sentiment analysis, word frequency, and more. This tool utilizes real-time data obtained from a WhatsApp hostel chat group, which was downloaded with the full consent of all participants, ensuring no ethical issues are associated with the data usage.

This project demonstrates how Natural Language Processing (NLP) and data visualization techniques can be applied to everyday conversations to uncover trends and patterns in communication.

#Key Features

📌 Data Preprocessing: The chat data is cleaned and organized using Pandas, making it suitable for analysis.

📌 Sentiment Analysis: Utilizes TextBlob to assess the sentiment (positive, neutral, or negative) of individual messages, offering an overview of the mood within the chat.

📌 Data Visualization: Various dynamic visualizations, such as word clouds and time series plots, are generated using Matplotlib, providing a clear, visual representation of chat data.

📌 Activity Analysis: Analyzes weekly and monthly chat activity to identify trends, peak times of communication, and user engagement.

📌 Word Frequency: Displays a list of the most frequently used words in the chat after removing common stopwords, giving insights into popular topics and phrases.

📌 Emoji Analysis: Counts and identifies the most frequently used emojis in the chat, reflecting the emotional tone of conversations.

📌 Interactive Interface: The entire application is built with Streamlit, allowing users to upload their WhatsApp chat files and interactively view the results in a user-friendly format.


#How to Use

You can try the analyzer with your own WhatsApp group chats by following these steps:

	1.	Export Chat Data:
	•	Open the group chat in WhatsApp.
	•	Tap the three dots in the top-right corner.
	•	Select “Export Chat” (choose the option to export without media).
 
	2.	For Mobile Users:
	•	You’ll be prompted to send the exported file via media platforms such as WhatsApp, Telegram, or Google Drive. Choose an option that lets you access the file easily.
 
	3.	For Laptop Users:
	•	The exported file will be saved directly to your system.
 
	4.	Upload the Chat File:
	•	Copy the URL link of the analyzer and paste it into any web browser.
	•	If you’re on mobile, you’ll see an arrow (>) in the top left corner of the screen—click it to reveal the option to upload a file.
	•	For laptop users, the option to upload will be immediately visible.
	•	Click on “Browse File” and select the WhatsApp chat file you want to analyze (either individual or group chats).
 
	5.	View the Analysis:
	•	Once the file is uploaded, click “Show Analysis”.
	•	If you see the analysis results, congratulations 🎉! You’ve successfully analyzed your WhatsApp chat.

#Ethical Considerations

The data used in this project comes from a real-time WhatsApp hostel group chat. All members of the group provided explicit permission for the data to be used in this project, ensuring that there are no ethical concerns regarding privacy or consent. Please ensure that you have similar permission before analyzing any personal or group chat data.
