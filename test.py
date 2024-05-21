import pandas as pd
from googleapiclient.discovery import build

playlist = input("Enter PLaylist")
df1 = pd.read_csv(f"C:\\workspace\\api\youtube_api\\video_data{playlist}.csv")

top_videos_category = df1[["category_id","view_Count" , "like_Count", "comment_Count"]].groupby("category_id")


# print(top_videos_category.sum())

df2 = pd.read_csv(f"C:\\workspace\\api\youtube_api\\utube_category.csv")
df_merged = df1.merge(df2[['category_id', 'cat_name']], on = "category_id")

print(df_merged["cat_name"])


# api_key ="AIzaSyArhL3qq30ywDCsueYHXzrQdfN-EWag5hg" # key 2
# channel_id = "UCmXZxX_qexEZxhb5_vQKPCw"

# api_service_name = "youtube"
# api_version = "v3"

# # creating a youtube service 
# youtube  = build(api_service_name, api_version, developerKey=api_key)

# request = youtube.videos().list(
#        part="snippet,contentDetails,statistics",
#        id="Je5AM5eGUUY"
#     )
# response  = request.execute()

# print(response['items'][0].keys())