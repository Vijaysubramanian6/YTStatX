from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import pickle as p
import matplotlib.pyplot as plt

# analysis of utube channel(statics)
# getting details using channel id


api_key ="AIzaSyArhL3qq30ywDCsueYHXzrQdfN-EWag5hg" # key 2
channel_id = "UCmXZxX_qexEZxhb5_vQKPCw"

api_service_name = "youtube"
api_version = "v3"

# creating a youtube service 
youtube  = build(api_service_name, api_version, developerKey=api_key)

# makes playlist data file, gets playlist ids
def playlist_id(youtube, channel_id):

   request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=50
    )
   
   response = request.execute()
   all_data = []
   # ***not able to extact channel name
   # j = response['items'][0]
   # channel_name = j['channelTitle']
   # print(channel_name)

   for i in response['items']:
      data  = {'name':i['snippet']['title'], 'id': i['id'], 'videos_count':i["contentDetails"]['itemCount'] }
      all_data.append(data)


   df = pd.DataFrame(all_data)
   df.to_csv(r"C:\workspace\api\youtube_api\playlist_data.csv")

# function to access video id for a given playlist
# has to do analysis of playlist of videos
def video_id(youtube, playlist_name):
   # global playlist_name
   # playlist_name = input("Enter the name of playlist: ")
   # fo  = open("playlist_ID.dat", "rb")
   # data = p.load(fo)
   
   df = pd.read_csv(r"C:\workspace\api\youtube_api\playlist_data.csv")

   for i in range(len(df['name'])):
      # j=0
      # print(i, "          ",df["id"][j])
      # print(type(i))
      # j+=1
      # break
      if(df['name'][i]== playlist_name):
        playlist_id=df["id"][i]      
#    else:
#       print("not found")
#       return
   
   request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        playlistId=playlist_id
    )
   
   response = request.execute()
   
   video_ids = []

   for i in response['items']:
    #   v_id = i['id']
    #   v_title = i['snippet']['title']

      data = {'v_title':i['snippet']['title'],'v_id': i['contentDetails']['videoId']}
      video_ids.append(data)


    
   # print(video_ids)
#    videos_stats(youtube, )
   return video_ids 


# function to get video stats
def videos_stats(youtube, video_ids):
   
   video_list  =""
   for i in video_ids:
      video_list+= i['v_id']+','

   request = youtube.videos().list(
       part="snippet,contentDetails,statistics",
       id=video_list
    )
   response  = request.execute()
   
   all_data = []
   # i = response['items'][0]
   # data = {'name': i['snippet']['title'],'id':i['id'], 'stats':i['statistics'], 'duration': i["contentDetails"]["duration"], 'category_id': int(i["categoryId"]) }
   # print(data)
   for i in response['items']:
      if "categoryId" not in i['snippet'].keys():
        print("s")
        data = {'name': i['snippet']['title'],'id':i['id'], 'stats':i['statistics'], 'duration': i["contentDetails"]["duration"], 'category_id': "0"} #, 'category_id': (i["categoryId"]) }
      else:
       
       data = {'name': i['snippet']['title'],'id':i['id'], 'stats':i['statistics'], 'duration': i["contentDetails"]["duration"],'category_id': (i["snippet"]["categoryId"]) } #, 'category_id': (i["categoryId"]) }
      all_data.append(data)
   return all_data # list of dictionary 
    # print(all_data)


# function to arrange video stats 
# makes the video data file after video_id and videos_stats function is run
def data_processing(data, playlist_name, j):
   df_data =[]
   # global counter
   # counter  =1
   check = 0
   # global playlist_name
   # print(j)
   # if playlist_name == 'Vedic Maths':
   #    return
   for i in (data): #,'category_id': int(i["category_id"]) l = [""]
      if "likeCount" not in i["stats"].keys():
        df_data.append({'name':i['name'],'id': i['id'] ,'view_Count': i['stats']['viewCount'],'like_Count':0 ,'comment_Count': i['stats']['commentCount'], "duration":(i['duration'][3:]), "category_id": i["category_id"] })
      else: 
        df_data.append({'name':i['name'],'id': i['id'] ,'view_Count': i['stats']['viewCount'],'like_Count':i['stats']['likeCount'] ,'comment_Count': i['stats']['commentCount'], "duration":(i['duration'][3:]),  "category_id": i["category_id"] })
    
   df = pd.DataFrame.from_dict(df_data)
   ele = ["\\","/",":","*", "?","\"","<",">","|"]
   # alternate_name = {}

   # Alternate naming
   for i in ele:
      if i in playlist_name:
         df.to_csv(f"C:\workspace\\api\youtube_api\\video_data{j}.csv")

         
         break
      check+=1

   if check== len(ele):
    df.to_csv(f"C:\workspace\\api\youtube_api\\video_data{playlist_name}.csv")
   
   # else:
   #    df.to_csv(f"C:\workspace\\api\youtube_api\\video_data{counter}.csv")
   # print(df)
   # return df
   

def get_comments( youtube):
   global playlist_name
   df = pd.read_csv(r"C:\workspace\api\youtube_api\video_data_Freelancing Skills.csv")

   video_name = input("Enter name of the video( from the playlist): ")

   comment_list = []
   for i in range(len(df['name'])):
      if(df['name'][i]== video_name):
        request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=df['id'][i]
    )
        response =request.execute()

        for i in response['items']:
           comment_list.append(i['snippet']['topLevelComment']['snippet']['textOriginal'])
         
        print(comment_list)
   # else:
   #    print("video Not found")

# *** running Main functions
   #  ###****each should be run only once

# playlist_id(youtube, channel_id) # ^^^ creating playlist_dataframe
# video = video_id(youtube) #**getting video_ids
   
# Data =videos_stats(youtube, video) # ***getting video stats
# data_processing(Data) 
# get_comments( youtube)


#*** graphing data

# channel analysis
def channel_playlist_analysis(youtube, channel_id):
   df = pd.read_csv(r"C:\workspace\api\youtube_api\playlist_data.csv")
   # condition = df[(df['name'] == "Vedic Maths | Fast Maths Tricks")].index
   # df.drop(condition, inplace=True)
   # print(df)

   for i in range(len(df['name'])):
      video = video_id(youtube, df["name"][i]) #**getting video_ids
      
      Data =videos_stats(youtube, video) # ***getting video stats

      # ^^^TO SOLVE: data_processing temoperyly is returning alternate_names, would have to find another way to store it
      # if df["name"][i] != "Vedic Maths | Fast Maths Tricks" :
      data_processing(Data, df["name"][i],i)
   
   # not to extract data from files to plot graph
   #--> bar chart playlists vs total views
   
   # playlist_name = input("Enter the name of the playlist to analyse: ")
   playlist_stats  = []
   for i in range(len(df['name'])):
         check =0

         # print(df['name'][i])
         ele = ["\\","/",":","*", "?","\"","<",">","|"]
   # alternate_name = {}
         for j in ele:
           if j in df['name'][i]:
            df1 = pd.read_csv(f"C:\workspace\\api\youtube_api\\video_data{i}.csv")
            break
           check+=1
         # print("Check: ", check)
         if check== len(ele):
              if i !=6:
               df1 = pd.read_csv(f"C:\workspace\\api\youtube_api\\video_data{df['name'][i]}.csv")
               pass
      #    df1 = pd.read_csv(f"C:\workspace\api\youtube_api\video_data{alternate_name[df['name'][i]]}.csv")
      # else:
      #    df1 = pd.read_csv(f"C:\workspace\api\youtube_api\video_data{df['name'][i]}.csv")
         Tviews = 0
         Tlikes = 0
         for k in range(len(df1['name'])): #len(df1['name'])
            # print(df1['name'][k])
            # print(df1["like_Count"][k])
            Tlikes+= df1["like_Count"][k]
            # print("Tlikes: ", Tlikes)
            Tviews+= df1["view_Count"][k]
      
         playlist_stats.append({"name":df['name'][i],"like_Count":Tlikes, "view_Count": Tviews})
   
   # print(Tviews, Tlikes)
   df2 = pd.DataFrame(playlist_stats)
   df2.to_csv(f"C:\workspace\\api\youtube_api\\video_data_test.csv")
   # print(df2)

   # Top 5 videos by views 
   top_plylist = df2.sort_values(by = "view_Count", ascending=False).head(5)
   # print(top_videos)
   p = sns.barplot(x= top_plylist['view_Count'], y= top_plylist['name']).set( 
    title="Playlist Vs Views(TOP 5)")
   plt.show()

   # # Top 5 videos by likes
   top_playlist_liked = df2.sort_values(by = "like_Count", ascending=False).head(5)
   # print(top_videos_l)
   p1 = sns.barplot(x= top_playlist_liked['like_Count'], y= top_playlist_liked['name']).set( 
    title="Playlist Vs Likes(TOP 5)")
   plt.show()


alternate_name= channel_playlist_analysis(youtube, channel_id)

# ^^^^ Video Engagement Metrics
def playlist_videos_analysis(): # yet to decide input paramenter
   # video = video_id(youtube) #**getting video_ids
   
   # Data =videos_stats(youtube, video) # ***getting video stats
   # data_processing(Data) 
   
   playlist_name = input("Enter the name of the playlist to analyse: ")

   ele = ["\\","/",":","*", "?","\"","<",">","|"]
   check =0
   # alternate_name = {}
   for j in ele:
      if j in playlist_name:
         df = pd.read_csv(r"C:\workspace\api\youtube_api\playlist_data.csv")
         idex = df[(df['name'] == playlist_name)].index
         df1 = pd.read_csv(f"C:\\workspace\\api\youtube_api\\video_data{idex}.csv")
         check=1
   if check:
      pass
   else: 
    df1 = pd.read_csv(f"C:\\workspace\\api\youtube_api\\video_data{playlist_name}.csv")

   # All category wies
    ##--> some issue in accessing category

   # # Top 5 videos_category by views 
   top_videos_category = df1[["category_id","view_Count" , "like_Count", "comment_Count"]].groupby("category_id").sum()
   df2 = pd.read_csv(f"C:\\workspace\\api\youtube_api\\utube_category.csv")
   df_merged = df1.merge(df2[['category_id', 'cat_name']])

   p = sns.barplot(x= df_merged['view_Count'], y= df_merged['cat_name']).set( 
    title="videos_category Vs Views")
   plt.show()

   # # Top 5 videos_category by likes
   p = sns.barplot(x= df_merged['like_Count'], y= df_merged['cat_name']).set( 
    title="videos_category Vs Likes")
   plt.show()

   # # Top 5 videos_category by commentcount
   p = sns.barplot(x= df_merged['comment_Count'], y= df_merged['cat_name']).set( 
    title="videos_category Vs Comments")
   plt.show()

   # All videos wise
   # # Top 5 videos by views 
   top_videos = df1.sort_values(by = "view_Count", ascending=False).head(5)
   # print(top_videos)
   p = sns.barplot(x= top_videos['view_Count'], y= top_videos['name']).set( 
    title="Video Vs Views(TOP 5)")
   plt.show()

   # # Top 5 videos by likes
   top_videos_liked = df1.sort_values(by = "like_Count", ascending=False).head(5)
   # print(top_videos_l)
   p1 = sns.barplot(x= top_videos_liked['like_Count'], y= top_videos_liked['name']).set( 
    title="Video Vs Likes (TOP 5)")
   plt.show()

   # # Top 5 videos by comments
   top_videos_liked = df1.sort_values(by = "comment_Count", ascending=False).head(5)
   # print(top_videos_l)
   p1 = sns.barplot(x= top_videos_liked['comment_Count'], y= top_videos_liked['name']).set( 
    title="Video Vs Comments (TOP 5)")
   plt.show()


playlist_videos_analysis()


# function to get playlistIds
# def get_playlist_id(youtube, channel_id):
#     request = youtube.channels().list(
#         part = "snippet, id",
#         id = channel_id
#     )

#     response = request.execute()
#     return response
#     # fo  = open("playlist_ID.dat", "wb")
#     # print(len(response['items'][0]))

#     for playlist in response["items"]:
#         playlist_title = playlist["snippet"]["title"]
#         playlist_id = playlist["id"]
#         data = {"title": playlist_title, "id": playlist_id}
#         print(data)
#         # p.dump(data, fo)


#     # for i in range(18):
#     #     data = {"name": response['items'][i]["snippet"]["title"], "ID": response['items'][i]["id"]}
#     #     p.dump(data, fo)
    
#     # fo.close()


# function to get statistics for channel

def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(
        part = "snippet, contentDetails, statistics", # details we want to retrive 
        id = channel_id
    )


    # response = request.execute()
    # title  = response['items'][0]['snippet']['title']
    # subscribers  = response['items'][0]['statistics']['subscriberCount']
    # views = response['items'][0]['statistics']['viewCount']
    # Total_vid = response['items'][0]['statistics']['videoCount']

    # data = {"channel_name": title,"sub": subscribers, "views":views,"total viedos": Total_vid}  

    # print(response)
    # return data

# print(get_channel_stats(youtube, channel_id))
    
# get_playlist_id(youtube, channel_id)
    
# 

# **writting file
# fo  = open("playlist_ID.dat", "wb")
# playlist_data = []

# for playlist in response["items"]:
#     # print(playlist['id'])
#     # print(playlist['snippet']['title'])
#     playlist_info = {"title": playlist["snippet"]["title"], "ID": playlist["id"]}
#     playlist_data.append(playlist_info)

#     # data = {"title":playlist['snippet']['title'] , "ID": playlist['id']}
#     # p.dump(data, fo)

# p.dump(playlist_data, fo)

# fo.close()


# ** reading the file
# fo  = open("playlist_ID.dat", "rb")

# for i in p.load(fo):
#     print(i)

# fo.close()

# fo  = open("playlist_ID.dat", "rb")
# data = p.load(fo)

# for i in data:
#     print(data)



#

# storing data frame    
# df.to_csv('video_data.csv')
    
# df = pd.read_csv('video_data.csv') # for Computer Science for Class 12 board playlist
# print(df[['like_Count','view_Count']])

# p1 =sns.histplot(data = df[['like_Count']])
# plt.show()

# p=sns.histplot(data = df[['view_Count']])
# plt.show()

# #  lets plot some graph
# sns.set_style("dark")

# # Top 5 videos by views
# top_videos = df.sort_values(by = "view_Count", ascending=False).head(5)
# print(top_videos)
# p1 = sns.barplot(x= top_videos['view_Count'], y= top_videos['name'])
# plt.show()

# # Top 5 videos by likes
# top_videos_l = df.sort_values(by = "like_Count", ascending=False).head(5)
# print(top_videos_l)
# p1 = sns.barplot(x= top_videos_l['like_Count'], y= top_videos_l['name'])
# plt.show()

# print(Data)

# fo = open("data.dat", 'wb')
# p.dump(Data, fo) # dumped the whole list , so only one element in data.dat file

# fo.close()
    
# fo = open("data.dat", 'rb')
# for i in p.load(fo):
#    print(i)
