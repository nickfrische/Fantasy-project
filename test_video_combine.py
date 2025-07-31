#!/usr/bin/env python3
"""
Test script to combine video with intro using existing logic
Downloads a new YouTube video and combines it with an intro for testing
"""

import subprocess
import os
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def search_youtube_video(player_name, year="2024"):
    """Search for a YouTube video using existing logic"""
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
            return video_url, video_id
        else:
            return None, None
            
    except HttpError as e:
        print(f"Error searching for {player_name}: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error for {player_name}: {e}")
        return None, None

def download_youtube_video(video_url, output_path, duration=10):
    """Download YouTube video with specified duration"""
    print(f"Downloading video: {video_url}")
    
    cmd = [
        'yt-dlp',
        '--format', 'best[height<=720]',
        '--external-downloader', 'ffmpeg',
        '--external-downloader-args', f'ffmpeg:-t {duration}',
        '--output', output_path,
        video_url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Video downloaded: {output_path}")
            return True
        else:
            print(f"✗ Download failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Exception during download: {e}")
        return False

def create_intro_image(output_file, player_name, team, fantasy_points, rank):
    """Create intro using modern design logic"""
    player_name_clean = player_name.replace("'", "").replace(" ", " ")
    
    # Modern intro without silhouette
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', 'color=0x0a0a0a:size=1920x1080:duration=2',  # 16:9 for video
        '-vf', (
            # Gradient background
            "drawbox=x=0:y=0:w=1920:h=1080:color=0x6366f1@0.1:t=fill,"
            
            # Main card
            "drawbox=x=100:y=200:w=1720:h=680:color=white@0.98:t=fill,"
            "drawbox=x=102:y=202:w=1716:h=676:color=0x6366f1@0.05:t=fill,"
            
            # Top section
            "drawbox=x=100:y=200:w=1720:h=340:color=0xf8fafc:t=fill,"
            "drawbox=x=100:y=200:w=1720:h=340:color=0x6366f1@0.03:t=fill,"
            
            # Divider line
            "drawbox=x=140:y=540:w=1640:h=3:color=0x6366f1:t=fill,"
            
            # Player name
            f"drawtext=text='{player_name_clean}':"
            "fontsize=84:fontcolor=0x0f172a:x=160:y=580,"
            
            # Team
            f"drawtext=text='{team}':"
            "fontsize=54:fontcolor=0x6366f1:x=160:y=680,"
            
            # Fantasy points
            f"drawtext=text='2024_Fantasy_Points_{fantasy_points}':"
            "fontsize=48:fontcolor=0x059669:x=160:y=750,"
            
            # Rank badge
            "drawbox=x=1600:y=220:w=180:h=180:color=0x6366f1:t=fill,"
            f"drawtext=text='#{rank}':"
            "fontsize=72:fontcolor=white:x=(1600+90-text_w/2):y=280,"
            
            # Title at top
            "drawbox=x=0:y=50:w=1920:h=100:color=0x1e293b:t=fill,"
            "drawtext=text='TOP_100_FANTASY_PLAYERS_2024':"
            "fontsize=56:fontcolor=white:x=(w-text_w)/2:y=85"
        ),
        '-t', '2',
        '-y',
        output_file
    ]
    
    try:
        print(f"Creating intro for {player_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Intro created: {output_file}")
            return True
        else:
            print(f"✗ Intro creation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Exception creating intro: {e}")
        return False

def combine_intro_and_video(intro_path, video_path, output_path):
    """Combine intro and video using ffmpeg"""
    print(f"Combining intro and video...")
    
    # Create a concat file
    concat_file = "temp_concat.txt"
    with open(concat_file, 'w') as f:
        f.write(f"file '{intro_path}'\n")
        f.write(f"file '{video_path}'\n")
    
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_file,
        '-c', 'copy',
        '-y',
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up concat file
        if os.path.exists(concat_file):
            os.remove(concat_file)
        
        if result.returncode == 0:
            print(f"✓ Combined video created: {output_path}")
            return True
        else:
            print(f"✗ Combination failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Exception combining videos: {e}")
        if os.path.exists(concat_file):
            os.remove(concat_file)
        return False

def main():
    """Main test function"""
    print("🎬 Testing Video + Intro Combination")
    print("=" * 50)
    
    # Create video_clips directory if it doesn't exist
    os.makedirs('video_clips', exist_ok=True)
    
    # Test player data
    player_name = "Saquon Barkley"
    team = "PHI"
    fantasy_points = "245.3"
    rank = "5"
    
    # Step 1: Search for YouTube video
    print(f"\n1. Searching for {player_name} video...")
    video_url, video_id = search_youtube_video(player_name)
    
    if not video_url:
        print("❌ Could not find video. Exiting.")
        return
    
    print(f"✓ Found video: {video_url}")
    
    # Step 2: Download video (10 seconds)
    video_path = f"video_clips/test_{video_id}.mp4"
    print(f"\n2. Downloading video (10 seconds)...")
    
    if not download_youtube_video(video_url, video_path, 10):
        print("❌ Video download failed. Exiting.")
        return
    
    # Step 3: Create intro
    intro_path = f"video_clips/test_intro_{player_name.replace(' ', '_')}.mp4"
    print(f"\n3. Creating intro...")
    
    if not create_intro_image(intro_path, player_name, team, fantasy_points, rank):
        print("❌ Intro creation failed. Exiting.")
        return
    
    # Step 4: Combine intro and video
    final_path = f"video_clips/test_combined_{player_name.replace(' ', '_')}.mp4"
    print(f"\n4. Combining intro and video...")
    
    if combine_intro_and_video(intro_path, video_path, final_path):
        print(f"\n🎉 SUCCESS!")
        print(f"📁 Final video: {final_path}")
        
        if os.path.exists(final_path):
            size_mb = os.path.getsize(final_path) / (1024 * 1024)
            print(f"📏 File size: {size_mb:.1f} MB")
        
        print(f"\n📹 Video structure:")
        print(f"   • 2 seconds intro with player stats")
        print(f"   • 10 seconds highlight footage")
        print(f"   • Total duration: ~12 seconds")
    else:
        print("❌ Final combination failed.")

if __name__ == "__main__":
    main()