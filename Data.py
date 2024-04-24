import streamlit as st
import pandas as pd
import googleapiclient.discovery
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="")
mycursor = mydb.cursor(buffered=True)
page_by_img = f"""<style>.stApp {{background-image: url("{"https://img.freepik.com/premium-photo/youtube-logo-abstract-geometry_41204-9711.jpg?w=826"}");background-size: cover;}}</style>"""
st.markdown(page_by_img, unsafe_allow_html=True)

api_service_name = "youtube"
api_version = "v3"
api_key ='# Use your own api key'

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
st.title('YOUTUBE')
st.write('YouTube Data Harvesting and Warehousing using and Streamlit')
channel_id=st.text_input("Enter Youtube Id")

def commentcount(count):
    if count > 100:
        return 100
    else:
        return count


def main():
    request = youtube.channels().list(part="snippet,contentDetails,statistics", id=channel_id)
    response = request.execute()
    channel_data = response.get('items', [{}])[0]
    channel_name = channel_data.get('snippet', {}).get('title', 'Unknown')
    channel_description = channel_data.get('snippet', {}).get('description', 'Unknown')
    channel_playlist = channel_data.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads', 'Unknown')
    channel_subcount = channel_data.get('statistics', {}).get('subscriberCount', 'Unknown')
    channel_videoCount = channel_data.get('statistics', {}).get('videoCount', 'Unknown')
    channel_viewCount = channel_data.get('statistics', {}).get('viewCount', 'Unknown')
    channel_logo_url = channel_data.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', 'Unknown')
    st.subheader("channel_Logo", divider='rainbow')
    st.image(channel_logo_url,width=300)
    st.subheader(channel_name, divider='rainbow')
    mycursor.execute('use youtube')
    query = """INSERT INTO channel (Channel_Id, Channel_Name, Subscription_Count, 
                Channel_Views, Channel_Description) 
                VALUES (%s, %s, %s, %s, %s)"""
    channel_data = (channel_id,channel_name,int(channel_subcount),int(channel_viewCount),channel_description)
    mycursor.execute(query, channel_data)
    query = """INSERT INTO playlist (Playlist_Id, Channel_Id) 
                    VALUES (%s, %s )"""
    playlist_data = (channel_playlist,channel_id)
    mycursor.execute(query, playlist_data)
    mydb.commit()
    request = youtube.playlistItems().list(part="snippet", playlistId=channel_playlist, maxResults=50)
    video_ids = []

    while request:
        response = request.execute()
        video_ids.extend([item["snippet"]["resourceId"]["videoId"] for item in response["items"]])
        if "nextPageToken" in response:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=channel_playlist,
                maxResults=50,
                pageToken=response["nextPageToken"]
            )
        else:
            request = None

    for video_id in video_ids:
        response = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id).execute()
        video_data = response["items"][0]
        video_name = video_data['snippet']['title']
        video_description = video_data['snippet']['description']
        video_publishedAt = video_data['snippet']['publishedAt']
        video_thumbnails = str(video_data['snippet']['thumbnails'])
        video_duration = video_data['contentDetails']['duration']
        video_viewCount = video_data['statistics']['viewCount']
        video_likeCount = video_data['statistics']['likeCount']
        video_favoriteCount = video_data['statistics']['favoriteCount']
        video_commentCount = video_data['statistics'].get('commentCount', 0)
        query = """INSERT INTO video (Video_Id, Playlist_Id, Video_Name, Video_Description, 
                    PublishedAt, View_Count, Like_Count, Favorite_Count, 
                    Comment_Count, Duration, Thumbnail) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        video_data= (video_id,channel_playlist,video_name,video_description,video_publishedAt,video_viewCount,video_likeCount,video_favoriteCount,video_commentCount,video_duration,video_thumbnails)
        mycursor.execute(query,video_data)
        mydb.commit()

        if int(video_commentCount) > 0:
            try:
                comments = youtube.commentThreads().list(part="id,snippet", videoId=video_id, maxResults=100).execute()
                count = commentcount(int(video_commentCount))
                for j in range(count):
                        comment_id = comments["items"][j]["id"]
                        comment_text = comments["items"][j]["snippet"]['topLevelComment']["snippet"]['textDisplay']
                        comment_author = comments["items"][j]["snippet"]['topLevelComment']["snippet"]['authorDisplayName']
                        comment_publishedAt = comments["items"][j]["snippet"]['topLevelComment']["snippet"]["publishedAt"]
                        
                        query="""INSERT INTO comment (Video_Id, Comment_Text, Comment_Author, Comment_PublishedAt) 
                        VALUES (%s, %s, %s, %s)"""
                        comment_data=(video_id,comment_text,comment_author,comment_publishedAt)
                        mycursor.execute(query,comment_data)
                        mydb.commit()
            except Exception as e:
                pass
        else:
            pass
        mydb.commit()
if st.button("Channel Details Table"):
    main()
if st.button("Questions"):
    st.switch_page(r'pages/Dropdown.py')
