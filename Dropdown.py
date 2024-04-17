import streamlit as st
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="")
mycursor = mydb.cursor(buffered=True)
page_by_img = """
<style>
[data-testid="stAppViewContainer"]{
background-color: #5d6fff;
opacity: 1;
background-image: radial-gradient(circle at center center, #f8f8f8, #5d6fff), repeating-radial-gradient(circle at center center, #f8f8f8, #f8f8f8, 9px, transparent 18px, transparent 9px);
background-blend-mode: multiply;
}
</style>
"""
st.markdown(page_by_img, unsafe_allow_html=True)
def dropdown():
    # Question 1: Names of all the videos and their corresponding channels
        def question1():
            query='select distinct channel_name,video_name from youtube.youtube_channel_details'
            z= pd.read_sql(query,mydb)
            st.write("Names of all the videos and their corresponding channels")
            st.write(z)

        # Question 2: Channels with the most number of videos, and how many videos they have
        def question2():
            st.write("Channels with the most number of videos, and how many videos they have")
            query='select distinct channel_name,channel_videoCount from youtube.youtube_channel_details order by channel_videoCount desc limit 1 '
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 3: Top 10 most viewed videos and their respective channels
        def question3():
            st.write("Top 10 most viewed videos and their respective channels")
            query='select distinct channel_name,video_name,video_viewCount from youtube.youtube_channel_details order by video_viewCount desc limit 10'
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 4: Number of comments on each video and their corresponding video names
        def question4():
            st.write("Number of comments on each video and their corresponding video names")
            query='select  distinct video_name,video_commentCount from youtube.youtube_channel_details'
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 5: Videos with the highest number of likes and their corresponding channel names
        def question5():
            st.write("Videos with the highest number of likes and their corresponding channel names")
            query='select distinct channel_name,video_name,video_likeCount from youtube.youtube_channel_details order by video_likeCount desc'
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 6: Total number of likes for each video and their corresponding video names
        def question6():
            st.write("Total number of likes for each video and their corresponding video names")
            query='select  distinct video_name,video_likeCount from youtube.youtube_channel_details'
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 7: Total number of views for each channel and their corresponding channel names
        def question7():
            st.write("Total number of views for each channel and their corresponding channel names")
            query='select distinct channel_name,Channel_Viewcount from youtube.youtube_channel_details'
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 8: Names of all the channels that have published videos in the year 2022
        def question8():
            st.write("Names of all the channels that have published videos in the year 2022")
            query="select distinct channel_name,video_publishedAt from youtube.youtube_channel_details where substring(video_publishedAt,1,4)='2022'"
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 9: Average duration of all videos in each channel and their corresponding channel names
        def question9():
            st.write("Average duration of all videos in each channel and their corresponding channel names")
            query = """SELECT channel_name, AVG(CASE 
                WHEN video_duration REGEXP 'M' THEN -- If duration contains minutes
                SUBSTRING_INDEX(SUBSTRING_INDEX(video_duration, 'PT', -2), 'M', -1)
                    ELSE 0 -- If no minutes, set to 0
                    END) AS avg_duration
                FROM youtube.youtube_channel_details
                GROUP BY channel_name"""
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 10: Videos with the highest number of comments and their corresponding channel names
        def question10():
            st.write("Videos with the highest number of comments and their corresponding channel names")
            query='select distinct channel_name,video_commentCount from youtube.youtube_channel_details order by video_commentCount desc'
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Dropdown menu to select the question
        selected_question = st.selectbox('Select a question', 
                                        ['Names of all the videos and their corresponding channels',
                                        'Channels with the most number of videos, and how many videos they have',
                                        'Top 10 most viewed videos and their respective channels',
                                        'Number of comments on each video and their corresponding video names',
                                        'Videos with the highest number of likes and their corresponding channel names',
                                        'Total number of likes for each video and their corresponding video names',
                                        'Total number of views for each channel and their corresponding channel names',
                                        'Names of all the channels that have published videos in the year 2022',
                                        'Average duration of all videos in each channel and their corresponding channel names',
                                        'Videos with the highest number of comments and their corresponding channel names'])

        # Display the selected question
        if selected_question == 'Names of all the videos and their corresponding channels':
            question1()
        elif selected_question == 'Channels with the most number of videos, and how many videos they have':
            question2()
        elif selected_question == 'Top 10 most viewed videos and their respective channels':
            question3()
        elif selected_question == 'Number of comments on each video and their corresponding video names':
            question4()
        elif selected_question == 'Videos with the highest number of likes and their corresponding channel names':
            question5()
        elif selected_question == 'Total number of likes for each video and their corresponding video names':
            question6()
        elif selected_question == 'Total number of views for each channel and their corresponding channel names':
            question7()
        elif selected_question == 'Names of all the channels that have published videos in the year 2022':
            question8()
        elif selected_question == 'Average duration of all videos in each channel and their corresponding channel names':
            question9()
        elif selected_question == 'Videos with the highest number of comments and their corresponding channel names':
            question10()
dropdown()