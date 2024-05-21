# YouTube Channel Data Analysis

This project analyzes YouTube channel data using the YouTube API. It retrieves playlists and video details such as views, likes, comments, and durations, processes the data, and stores it in CSV files. The project also creates visualizations to compare the popularity and engagement of different playlists and videos.

## Features

- **Playlist Retrieval:** Fetches playlist details from a YouTube channel.
- **Video Details Extraction:** Retrieves video IDs and statistics (views, likes, comments, duration) from playlists.
- **Data Storage:** Saves playlist and video data into CSV files.
- **Visualization:** Creates bar charts to analyze and compare playlists and videos based on views and likes.
- **Comment Extraction:** Extracts and displays comments from specific videos.

## Requirements

- Python 3.x
- pandas
- seaborn
- matplotlib
- google-api-python-client

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/youtube-channel-analysis.git
   cd youtube-channel-analysis
   ```

2. Install the required packages:
   ```sh
   pip install pandas seaborn matplotlib google-api-python-client
   ```

## Usage

1. Set your YouTube API key and channel ID in the script:

   ```python
   api_key = "YOUR_API_KEY"
   channel_id = "YOUR_CHANNEL_ID"
   ```

2. Run the script to fetch playlist data:

   ```python
   playlist_id(youtube, channel_id)
   ```

3. Get video details for a specific playlist:

   ```python
   video_ids = video_id(youtube, "Playlist Name")
   data = videos_stats(youtube, video_ids)
   data_processing(data, "Playlist Name", index)
   ```

4. Analyze and visualize the channel's playlists:

   ```python
   channel_playlist_analysis(youtube, channel_id)
   ```

5. Extract comments from a specific video:
   ```python
   get_comments(youtube)
   ```

## Functions

- `playlist_id(youtube, channel_id)`: Fetches playlist details and saves them to a CSV file.
- `video_id(youtube, playlist_name)`: Retrieves video IDs from a given playlist.
- `videos_stats(youtube, video_ids)`: Fetches video statistics.
- `data_processing(data, playlist_name, j)`: Processes and saves video statistics data to a CSV file.
- `channel_playlist_analysis(youtube, channel_id)`: Analyzes and visualizes playlist data.
- `get_comments(youtube)`: Extracts and displays comments from a specific video.

## License

This project is licensed under the MIT License.
