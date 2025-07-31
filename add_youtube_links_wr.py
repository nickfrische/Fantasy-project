import os
import csv
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def search_youtube_video(player_name, year="2024"):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    search_query = f"{player_name} {year} highlights"
    
    try:
        search_response = youtube.search().list(
            q=search_query,
            part='snippet',
            maxResults=1,
            type='video'
        ).execute()
        
        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        else:
            return "No video found"
            
    except HttpError as e:
        print(f"Error searching for {player_name}: {e}")
        return "Error"
    except Exception as e:
        print(f"Unexpected error for {player_name}: {e}")
        return "Error"

def process_csv_file(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['YouTubeLink']
        
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                player_name = row['PlayerName']
                print(f"Searching for {player_name}...")
                
                youtube_link = search_youtube_video(player_name)
                row['YouTubeLink'] = youtube_link
                
                writer.writerow(row)
                
                time.sleep(0.5)
                
    print(f"Completed processing {input_file}")

def main():
    input_file = 'wr_top100.csv'
    output_file = 'wr_top100_with_links.csv'
    
    if os.path.exists(input_file):
        print(f"Processing {input_file}...")
        process_csv_file(input_file, output_file)
    else:
        print(f"File {input_file} not found!")
    
    print("\nWide receivers processed successfully!")

if __name__ == "__main__":
    main()