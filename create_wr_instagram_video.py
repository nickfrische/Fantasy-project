#!/usr/bin/env python3
import subprocess
import os
import csv
import sys
import tempfile
from pathlib import Path

def create_wr_intro(player_name, team, fantasy_points, rank, output_path):
    """Create an intro video for a WR with Instagram aspect ratio (9:16)"""
    
    # Instagram aspect ratio: 1080x1920 (9:16)
    width, height = 1080, 1920
    
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color=color=black@0.0:size={width}x{height}:duration=2:rate=30',
        '-f', 'lavfi', 
        '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100:duration=2',
        '-vf', (
            f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=120:"
            f"fontcolor=white:x=(w-text_w)/2:y=200:text='TOP 100 FANTASY WRs 2024',"
            
            f"drawbox=x=100:y=600:w=880:h=700:color=white@0.2:t=fill,"
            
            f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=80:"
            f"fontcolor=white:x=780:y=650:text='#{rank} WR',"
            
            f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=100:"
            f"fontcolor=white:x=(w-text_w)/2:y=900:text='{player_name}',"
            
            f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=60:"
            f"fontcolor=#6B8BFF:x=(w-text_w)/2:y=1050:text='{team}',"
            
            f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=50:"
            f"fontcolor=#888888:x=(w-text_w)/2:y=1200:text='2024 Fantasy Points',"
            
            f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=120:"
            f"fontcolor=#32CD32:x=(w-text_w)/2:y=1300:text='{fantasy_points}'"
        ),
        '-c:v', 'libx264',
        '-preset', 'slow',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-y',
        output_path
    ]
    
    print(f"Creating intro for {player_name}...")
    subprocess.run(cmd, check=True)
    print(f"Intro created: {output_path}")

def download_youtube_video(url, output_path, duration=30):
    """Download first N seconds of a YouTube video"""
    
    # Try different ways to call yt-dlp
    yt_dlp_commands = [
        ['yt-dlp'],
        ['python3', '-m', 'yt_dlp'],
        ['python', '-m', 'yt_dlp'],
        ['/opt/homebrew/bin/yt-dlp'],
        ['/usr/local/bin/yt-dlp']
    ]
    
    # Find which command works
    yt_dlp_cmd = None
    for cmd_prefix in yt_dlp_commands:
        try:
            test_cmd = cmd_prefix + ['--version']
            subprocess.run(test_cmd, check=True, capture_output=True)
            yt_dlp_cmd = cmd_prefix
            break
        except:
            continue
    
    if not yt_dlp_cmd:
        print("yt-dlp not found. Please install it with: pip install yt-dlp")
        raise Exception("yt-dlp not available")
    
    # Build the download command
    cmd = yt_dlp_cmd + [
        '-f', 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '--merge-output-format', 'mp4',
        '--download-sections', f'*0-{duration}',
        '-o', output_path,
        '--no-playlist',
        url
    ]
    
    print(f"Downloading first {duration} seconds from YouTube: {url}")
    subprocess.run(cmd, check=True)
    print(f"Downloaded: {output_path}")

def convert_to_instagram_format(video_path, output_path):
    """Convert video to Instagram aspect ratio (9:16) with proper scaling"""
    
    # Instagram dimensions
    target_width, target_height = 1080, 1920
    
    # Use a simpler approach: scale to fit height, then pad with black bars
    # This ensures the video fits in 9:16 without distortion
    scale_filter = (
        f"scale=w='min({target_width},iw*{target_height}/ih)':h='min({target_height},ih*{target_width}/iw)',"
        f"pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2:black,"
        f"setsar=1"
    )
    
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', scale_filter,
        '-r', '30',  # Set frame rate to 30fps
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-y',
        output_path
    ]
    
    print("Converting to Instagram format...")
    subprocess.run(cmd, check=True)
    print(f"Converted: {output_path}")

def concatenate_videos(intro_path, main_path, output_path):
    """Concatenate intro and main video"""
    
    concat_list = "concat_list.txt"
    
    with open(concat_list, 'w') as f:
        f.write(f"file '{os.path.abspath(intro_path)}'\n")
        f.write(f"file '{os.path.abspath(main_path)}'\n")
    
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_list,
        '-c', 'copy',
        '-y',
        output_path
    ]
    
    print("Concatenating videos...")
    try:
        subprocess.run(cmd, check=True)
    finally:
        if os.path.exists(concat_list):
            os.remove(concat_list)
    
    print(f"Final video: {output_path}")

def process_wr_video(player_name, team, fantasy_points, rank, youtube_url, output_dir="output"):
    """Complete workflow to create Instagram video for a WR"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # File paths
    safe_name = player_name.replace("'", "").replace(" ", "_")
    intro_path = f"{output_dir}/{safe_name}_intro.mp4"
    youtube_path = f"{output_dir}/{safe_name}_youtube_raw.mp4"
    youtube_instagram = f"{output_dir}/{safe_name}_youtube_instagram.mp4"
    final_path = f"{output_dir}/{safe_name}_instagram_final.mp4"
    
    # Step 1: Create intro
    create_wr_intro(player_name, team, fantasy_points, rank, intro_path)
    
    # Step 2: Download YouTube video
    download_youtube_video(youtube_url, youtube_path)
    
    # Step 3: Convert YouTube video to Instagram format
    convert_to_instagram_format(youtube_path, youtube_instagram)
    
    # Step 4: Concatenate intro and main video
    concatenate_videos(intro_path, youtube_instagram, final_path)
    
    # Cleanup intermediate files
    for path in [intro_path, youtube_path, youtube_instagram]:
        if os.path.exists(path):
            os.remove(path)
    
    return final_path

def main():
    # Read CSV and process first unposted WR
    csv_path = "wr_top100_with_links.csv"
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Find first unposted player
    for row in rows:
        if row['Posted'].lower() == 'false':
            rank = row['Rank']
            player_name = row['PlayerName']
            team = row['Team']
            fantasy_points = row['FantasyPoints']
            youtube_url = row['YouTubeLink']
            
            print(f"\nProcessing: {player_name} (#{rank})")
            print(f"Team: {team}")
            print(f"Fantasy Points: {fantasy_points}")
            print(f"YouTube URL: {youtube_url}")
            
            try:
                final_video = process_wr_video(
                    player_name, team, fantasy_points, rank, youtube_url
                )
                print(f"\n✅ Success! Video created: {final_video}")
                
                # Update CSV to mark as posted
                row['Posted'] = 'True'
                with open(csv_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                
                break
                
            except Exception as e:
                print(f"\n❌ Error processing {player_name}: {e}")
                break
    else:
        print("All WRs have been posted!")

if __name__ == "__main__":
    main()