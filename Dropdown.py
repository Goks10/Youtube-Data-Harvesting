import streamlit as st
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="")
mycursor = mydb.cursor(buffered=True)
page_by_img = f"""<style>.stApp {{background-image: url("{"https://img.freepik.com/premium-photo/abstract-moving-geometric-shapes-from-top-bottom-animation-d-monochrome-rectangular_1096515-21089.jpg?w=996"}");background-size: cover;}}</style>"""
st.markdown(page_by_img, unsafe_allow_html=True)
def dropdown():
    # Question 1: Names of all the videos and their corresponding channels
        def question1():
            mycursor.execute("use youtube")
            query="""
        SELECT Video_Name, Channel_Name
        FROM video
        JOIN playlist ON video.Playlist_Id = playlist.Playlist_Id
        JOIN channel ON playlist.Channel_Id = channel.Channel_Id
    """
            z= pd.read_sql(query,mydb)
            st.write("Names of all the videos and their corresponding channels")
            st.write(z)

        # Question 2: Channels with the most number of videos, and how many videos they have
        def question2():
            mycursor.execute("use youtube")
            st.write("Channels with the most number of videos, and how many videos they have")
            query="""select channel.channel_name,count(video.video_id) as num_videos from channel
            join playlist on channel.channel_id = playlist.channel_id
            join video on playlist.playlist_id = video.playlist_id 
            group by channel.channel_name order by num_videos desc limit 1;"""
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 3: Top 10 most viewed videos and their respective channels
        def question3():
            mycursor.execute("use youtube")
            st.write("Top 10 most viewed videos and their respective channels")
            query="""select * from (select video.View_Count,channel.channel_name,video.Video_name from video 
                join playlist on video.playlist_id = playlist.playlist_id
                join channel on playlist.Channel_Id = channel.Channel_Id
                order by video.view_count desc limit 10) as new;"""
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 4: Number of comments on each video and their corresponding video names
        def question4():
            mycursor.execute("use youtube")
            st.write("Number of comments on each video and their corresponding video names")
            query="""select channel.Channel_Name,video.Video_Name,video.Comment_Count from video
                join playlist on video.playlist_id = playlist.playlist_id
                join channel on playlist.Channel_Id = channel.Channel_Id;"""
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 5: Videos with the highest number of likes and their corresponding channel names
        def question5():
            mycursor.execute("use youtube")
            st.write("Videos with the highest number of likes and their corresponding channel names")
            query="""select channel.Channel_Name,max(video.Like_Count) as highest_likes from video 
                join playlist on video.playlist_id =playlist.Playlist_Id
                join channel on playlist.Channel_Id = channel.Channel_Id 
                group by channel.Channel_Name order by highest_likes desc;"""
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 6: Total number of likes for each video and their corresponding video names
        def question6():
            mycursor.execute("use youtube")
            st.write("Total number of likes for each video and their corresponding video names")
            query="""select channel.Channel_Name,video.Video_Name,sum(video.Like_Count) as total_likes,
                sum(video.Dislike_Count) as total_dislike from video
                join playlist on video.playlist_id = playlist.Playlist_Id
                join channel on playlist.Channel_Id = channel.Channel_Id group by video.Video_Id;"""
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 7: Total number of views for each channel and their corresponding channel names
        def question7():
            mycursor.execute("use youtube")
            st.write("Total number of views for each channel and their corresponding channel names")
            query="""select channel.Channel_Name,channel.Channel_Views as total_no_views from channel;"""
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 8: Names of all the channels that have published videos in the year 2022
        def question8():
            mycursor.execute("use youtube")
            st.write("Names of all the channels that have published videos in the year 2022")
            query="""select channel.Channel_Name,video.Video_Name,video.PublishedAt as published_at_2023 from channel
                join playlist on channel.Channel_Id = playlist.Channel_Id
                join video on playlist.Playlist_Id = video.Playlist_Id where video.PublishedAt
                between '2023-01-01 00:00:00' and '2023-12-31 23:59:59' order by published_at_2023;"""
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 9: Average duration of all videos in each channel and their corresponding channel names
        def question9():
            mycursor.execute("use youtube")
            st.write("Average duration of all videos in each channel and their corresponding channel names")
            query = """select channel.Channel_Name,SEC_TO_TIME(AVG(
                        CASE
                            WHEN video.Duration LIKE 'PT%M%S' THEN
                                TIME_TO_SEC(SUBSTRING(video.Duration, 3, INSTR(video.Duration, 'M') - 3)) * 60 + SUBSTRING(video.Duration, INSTR(video.Duration, 'M') + 1, INSTR(video.Duration, 'S') - INSTR(video.Duration, 'M') - 1)
                            WHEN video.Duration LIKE 'PT%S' THEN
                                SUBSTRING(video.Duration, 3, INSTR(video.Duration, 'S') - 3)
                        END
                        )) AS avg_duration from video
                join playlist on video.Playlist_Id = playlist.Playlist_Id
                join channel on playlist.Channel_Id = channel.Channel_Id group by channel.Channel_Name;"""
            z= pd.read_sql(query,mydb)
            st.write(z)

        # Question 10: Videos with the highest number of comments and their corresponding channel names
        def question10():
            mycursor.execute("use youtube")
            st.write("Videos with the highest number of comments and their corresponding channel names")
            query="""select channel.Channel_Name,video.Video_Name,
                max(video.Comment_Count) as highest_count from video
                join playlist on video.Playlist_Id = playlist.Playlist_Id
                join channel on playlist.Channel_Id = channel.Channel_Id
                where video.Comment_Count = (select max(video.Comment_Count) from video
                where video.Playlist_Id = playlist.Playlist_Id) 
                group by channel.channel_name,video.Video_Name order by highest_count desc ;"""
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
