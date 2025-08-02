#!/usr/bin/env python3
import subprocess
import os
import csv
from pathlib import Path

# Import the intro function from the main script
import sys
sys.path.append('/Users/nickfrische/Desktop/Fantasy project')
from create_wr_instagram_video import create_wr_intro, download_youtube_video

def create_balanced_stacked_blur_video(input_video, output_path):
    """
    Create stacked blur effect with more blur coverage
    - Larger top blur section 
    - Smaller middle section with properly formatted main video
    - Larger bottom blur section
    """
    
    width, height = 1080, 1920
    
    # NEW: Adjusted section heights for more blur coverage
    blur_section_height = 640  # Increased from 480 - more blur space
    main_section_height = 640  # Decreased from 960 - smaller middle video
    
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-filter_complex', (
            # Split input into 3 copies
            '[0:v]split=3[top][bottom][overlay_main];'
            
            # Top blur section - crop top portion, then blur
            f'[top]crop={width}:{blur_section_height}:0:0,'
            f'gblur=sigma=30[top_blur];'
            
            # Bottom blur section - crop bottom portion, then blur  
            f'[bottom]crop={width}:{blur_section_height}:0:ih-{blur_section_height},'
            f'gblur=sigma=30[bottom_blur];'
            
            # Create transparent middle section (empty black)
            f'color=black:size={width}x{main_section_height}:duration=30:rate=30[middle_empty];'
            
            # Stack: top blur + empty middle + bottom blur
            f'[top_blur][middle_empty][bottom_blur]vstack=inputs=3[blur_bg];'
            
            # Create overlay video with proper Instagram format scaling
            f"[overlay_main]scale=w='min({width},iw*{main_section_height}/ih)':h='min({main_section_height},ih*{width}/iw)',"
            f"pad={width}:{main_section_height}:(ow-iw)/2:(oh-ih)/2:black,"
            f"setsar=1[overlay_scaled];"
            
            # Overlay the properly scaled video in the middle section
            f'[blur_bg][overlay_scaled]overlay=0:{blur_section_height}[final]'
        ),
        '-map', '[final]',
        '-map', '0:a?',  # Include audio if present
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-r', '30',
        '-t', '30',  # Duration limit
        '-y',
        output_path
    ]
    
    print(f"Creating balanced stacked blur effect...")
    print(f"Blur sections: {blur_section_height}px each (top/bottom)")
    print(f"Middle section: {width}x{main_section_height}px")
    print(f"Input: {input_video}")
    print(f"Output: {output_path}")
    
    subprocess.run(cmd, check=True)
    print(f"✅ Balanced stacked blur video created: {output_path}")

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
    
    print("Concatenating intro with balanced stacked blur video...")
    try:
        subprocess.run(cmd, check=True)
    finally:
        if os.path.exists(concat_list):
            os.remove(concat_list)
    
    print(f"Final video: {output_path}")

def process_wr_with_balanced_stacked_blur(player_name, team, fantasy_points, rank, youtube_url, output_dir="output"):
    """Complete workflow: intro + balanced stacked blur highlights"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # File paths
    safe_name = player_name.replace("'", "").replace(" ", "_")
    intro_path = f"{output_dir}/{safe_name}_intro.mp4"
    youtube_path = f"{output_dir}/{safe_name}_youtube_raw.mp4"
    stacked_path = f"{output_dir}/{safe_name}_balanced_stacked_blur.mp4"
    final_path = f"{output_dir}/{safe_name}_BALANCED_STACKED_FINAL.mp4"
    
    print(f"\n🎬 Processing {player_name} with balanced stacked blur effect...")
    
    # Step 1: Create intro
    create_wr_intro(player_name, team, fantasy_points, rank, intro_path)
    
    # Step 2: Download YouTube video (30 seconds)
    download_youtube_video(youtube_url, youtube_path, duration=30)
    
    # Step 3: Create balanced stacked blur version
    create_balanced_stacked_blur_video(youtube_path, stacked_path)
    
    # Step 4: Concatenate intro + balanced stacked blur video
    concatenate_videos(intro_path, stacked_path, final_path)
    
    # Cleanup intermediate files
    for path in [intro_path, youtube_path, stacked_path]:
        if os.path.exists(path):
            os.remove(path)
    
    return final_path

def test_with_csv_data():
    """Test with next unposted player from CSV"""
    
    csv_path = "wr_top100_with_links.csv"
    
    if not os.path.exists(csv_path):
        print("❌ CSV file not found:", csv_path)
        return
    
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
            
            print(f"\n🏈 Testing balanced stacked blur with: {player_name} (#{rank})")
            
            try:
                final_video = process_wr_with_balanced_stacked_blur(
                    player_name, team, fantasy_points, rank, youtube_url
                )
                print(f"\n✅ Success! Balanced stacked blur video: {final_video}")
                return final_video
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                return None
    
    print("All WRs have been posted!")
    return None

if __name__ == "__main__":
    print("Testing balanced stacked blur effect...")
    test_with_csv_data()