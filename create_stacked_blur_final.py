#!/usr/bin/env python3
import subprocess
import os
import csv
from pathlib import Path

# Import the intro function from the main script
import sys
sys.path.append('/Users/nickfrische/Desktop/Fantasy project')
from create_wr_instagram_video import create_wr_intro, download_youtube_video

def create_stacked_blur_video(input_video, output_path):
    """
    Creates stacked blur video with Touch V3 settings:
    - 640px blur sections
    - Middle video zoomed to 130% for optimal balance
    - Blur touches top and bottom of middle video
    """
    
    width, height = 1080, 1920
    
    blur_section_height = 640
    main_section_height = 640
    
    # Zoom the middle video by 130% (Touch V3 setting)
    zoom_factor = 1.3
    
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-filter_complex', (
            '[0:v]split=3[top][bottom][overlay_main];'
            f'[top]crop={width}:{blur_section_height}:0:0,'
            f'gblur=sigma=30[top_blur];'
            f'[bottom]crop={width}:{blur_section_height}:0:ih-{blur_section_height},'
            f'gblur=sigma=30[bottom_blur];'
            f'color=black:size={width}x{main_section_height}:duration=10:rate=30[middle_empty];'
            f'[top_blur][middle_empty][bottom_blur]vstack=inputs=3[blur_bg];'
            # Scale with zoom factor
            f"[overlay_main]scale=w='min({int(width * zoom_factor)},iw*{int(main_section_height * zoom_factor)}/ih)':h='min({int(main_section_height * zoom_factor)},ih*{int(width * zoom_factor)}/iw)',"
            f"crop={width}:{main_section_height},"
            f"setsar=1[overlay_scaled];"
            f'[blur_bg][overlay_scaled]overlay=0:{blur_section_height}[final]'
        ),
        '-map', '[final]', '-map', '0:a?',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '25',
        '-c:a', 'aac', '-b:a', '128k', '-r', '30', '-t', '10', '-y', output_path
    ]
    
    print(f"Creating stacked blur video with 130% zoom...")
    subprocess.run(cmd, check=True)

def concatenate_intro_and_blur(intro_path, blur_path, output_path):
    """Concatenate intro video with stacked blur video"""
    concat_list_path = "concat_list.txt"
    
    with open(concat_list_path, 'w') as f:
        f.write(f"file '{intro_path}'\n")
        f.write(f"file '{blur_path}'\n")
    
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_list_path,
        '-c', 'copy',
        '-y', output_path
    ]
    
    print("Combining intro with stacked blur video...")
    subprocess.run(cmd, check=True)
    
    # Clean up
    if os.path.exists(concat_list_path):
        os.remove(concat_list_path)

def process_wr_stacked_video():
    """Process one WR from bottom of top 75 with complete workflow"""
    csv_path = "wr_top100_with_links.csv"
    
    # Read CSV
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Find the last unposted player in top 75 (rank 75 and up)
    target_player = None
    target_row_index = None
    
    for i, row in enumerate(rows):
        rank = int(row['Rank'])
        if rank <= 75 and row['False'].lower() == 'false':
            target_player = row
            target_row_index = i
    
    if not target_player:
        print("No unposted players found in top 75!")
        return
    
    player_name = target_player['PlayerName']
    team = target_player['Team']
    rank = target_player['Rank']
    fantasy_points = target_player['FantasyPoints']
    youtube_url = target_player['YouTubeLink']
    
    print(f"Processing #{rank} {player_name} ({team}) - {fantasy_points} points")
    
    # Create file paths
    safe_name = player_name.replace("'", "").replace(" ", "_")
    intro_path = f"output/{safe_name}_intro.mp4"
    youtube_path = f"output/{safe_name}_youtube_raw.mp4"
    blur_path = f"output/{safe_name}_stacked_blur.mp4"
    final_path = f"output/{safe_name}_FINAL_STACKED_WITH_INTRO.mp4"
    
    try:
        # Step 1: Create intro
        print("Step 1: Creating geometric intro...")
        create_wr_intro(player_name, team, rank, fantasy_points, intro_path)
        
        # Step 2: Download YouTube video
        print("Step 2: Downloading YouTube highlights...")
        download_youtube_video(youtube_url, youtube_path, duration=10)
        
        # Step 3: Create stacked blur video
        print("Step 3: Creating stacked blur video...")
        create_stacked_blur_video(youtube_path, blur_path)
        
        # Step 4: Concatenate intro + blur video
        print("Step 4: Combining intro with stacked blur...")
        concatenate_intro_and_blur(intro_path, blur_path, final_path)
        
        # Step 5: Update CSV to mark as posted
        print("Step 5: Updating CSV...")
        rows[target_row_index]['False'] = 'True'
        
        with open(csv_path, 'w', newline='') as f:
            fieldnames = ['Rank', 'PlayerName', 'Team', 'FantasyPoints', 'False', 'Notes', 'YouTubeLink']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        # Clean up intermediate files
        for temp_file in [intro_path, youtube_path, blur_path]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        print(f"✅ SUCCESS: {final_path}")
        print(f"   Player: {player_name} marked as posted in CSV")
        return final_path
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        # Clean up on error
        for temp_file in [intro_path, youtube_path, blur_path]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        raise

if __name__ == "__main__":
    process_wr_stacked_video()