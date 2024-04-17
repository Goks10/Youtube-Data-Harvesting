# YouTube Data Harvesting and Warehousing using SQL and Streamlit

## Skills Learned
- Python scripting
- Data collection
- Streamlit
- API integration
- Data management using SQL

## Domain
Social Media

## Problem Statement
The task is to develop a Streamlit application enabling users to access and analyze data from multiple YouTube channels. Key features include:

- Inputting a YouTube channel ID to retrieve relevant data (e.g., subscribers, video count, likes, comments) using the Google API.
- Collecting data of YouTube channels and storing it in a data lake.
- Option to store data in MySQL .
- Ability to search and retrieve data from the SQL database, including joining tables for detailed channel analysis.

## Approach
1. **Set up a Streamlit app**: Utilize Streamlit to create a simple UI for users to input channel IDs, view details, and select channels for migration.
2. **Connect to the YouTube API**: Utilize the Google API client library in Python to fetch channel and video data.
3. **Store and clean data**: After retrieving data from the YouTube API, store it temporarily in suitable formats (e.g., pandas DataFrames) before migrating to the data warehouse. Ensure data cleanliness and integrity.
4. **Migrate data to a SQL data warehouse**: Use MySQL or PostgreSQL to store data after collecting for multiple channels.
5. **Query the SQL data warehouse**: Use SQL queries to retrieve specific channel data based on user input, including joining tables for comprehensive analysis.
6. **Display data in the Streamlit app**: Present retrieved data using Streamlit's data visualization features, including charts and graphs.

## References
- [Streamlit Documentation](https://docs.streamlit.io/library/api-reference)
- [YouTube API Reference](https://developers.google.com/youtube/v3/getting-started)

## Results
This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on YouTube channels, stores it in a SQL database, and enables users to search for channel details and join tables to view data in the Streamlit app.
