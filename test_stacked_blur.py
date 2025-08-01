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
    Create a stacked video effect with blurred top and bottom sections
    - Main video in center (maintains aspect ratio)
    - Blurred and scaled copies on top and bottom
    - Perfect for Instagram 9:16 format
    """
    
    width, height = 1080, 1920
    
    # Perfect proportions for amazing blur effect - simple and working
    blur_section_height = 400  # Top and bottom blur sections  
    main_section_height = 1120  # Center section
    
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-filter_complex', (
            # Create three copies of the input
            '[0:v]split=3[main][top][bottom];'
            
            # Main video in center - simple crop from center with some zoom out effect
            f'[main]crop={width}:{main_section_height}:0:(ih-{main_section_height})/2,'
            f'scale={int(width*0.9)}:-1:force_original_aspect_ratio=decrease,'
            f'pad={width}:{main_section_height}:(ow-iw)/2:(oh-ih)/2:color=black[main_scaled];'
            
            # Top blur section - crop top portion, then blur
            f'[top]crop={width}:{blur_section_height}:0:0,'
            f'gblur=sigma=35[top_blur];'
            
            # Bottom blur section - crop bottom portion, then blur
            f'[bottom]crop={width}:{blur_section_height}:0:ih-{blur_section_height},'
            f'gblur=sigma=35[bottom_blur];'
            
            # Stack all three sections vertically
            f'[top_blur][main_scaled][bottom_blur]vstack=inputs=3[final]'
        ),
        '-map', '[final]',
        '-map', '0:a?',  # Include audio if present
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-r', '30',
        '-y',
        output_path
    ]
    
    print(f"Creating stacked blur effect...")
    print(f"Input: {input_video}")
    print(f"Output: {output_path}")
    
    subprocess.run(cmd, check=True)
    print(f"✅ Stacked blur video created: {output_path}")

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
    
    print("Concatenating intro with stacked blur video...")
    try:
        subprocess.run(cmd, check=True)
    finally:
        if os.path.exists(concat_list):
            os.remove(concat_list)
    
    print(f"Final video: {output_path}")

def process_wr_with_stacked_blur(player_name, team, fantasy_points, rank, youtube_url, output_dir="output"):
    """Complete workflow: intro + stacked blur highlights"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # File paths
    safe_name = player_name.replace("'", "").replace(" ", "_")
    intro_path = f"{output_dir}/{safe_name}_intro.mp4"
    youtube_path = f"{output_dir}/{safe_name}_youtube_raw.mp4"
    stacked_path = f"{output_dir}/{safe_name}_stacked_blur.mp4"
    final_path = f"{output_dir}/{safe_name}_stacked_final.mp4"
    
    print(f"\n🎬 Processing {player_name} with stacked blur effect...")
    
    # Step 1: Create intro
    create_wr_intro(player_name, team, fantasy_points, rank, intro_path)
    
    # Step 2: Download YouTube video (30 seconds)
    download_youtube_video(youtube_url, youtube_path, duration=30)
    
    # Step 3: Create stacked blur version
    create_stacked_blur_video(youtube_path, stacked_path)
    
    # Step 4: Concatenate intro + stacked blur video
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
            
            print(f"\n🏈 Testing stacked blur with: {player_name} (#{rank})")
            
            try:
                final_video = process_wr_with_stacked_blur(
                    player_name, team, fantasy_points, rank, youtube_url
                )
                print(f"\n✅ Success! Stacked blur video: {final_video}")
                return final_video
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                return None
    
    print("All WRs have been posted!")
    return None

def test_with_existing_video():
    """Test stacked blur with existing video only"""
    
    # Look for existing video files
    test_videos = [
        "output/Brian_Thomas_Jr_instagram_final.mp4",
        "output/Amon-Ra_St._Brown_instagram_final.mp4"
    ]
    
    input_video = None
    for video in test_videos:
        if os.path.exists(video):
            input_video = video
            break
    
    if not input_video:
        print("❌ No test video found.")
        return
    
    # Create output filename
    base_name = os.path.basename(input_video).replace('.mp4', '')
    output_path = f"output/{base_name}_stacked_blur_fixed.mp4"
    
    # Process the video
    create_stacked_blur_video(input_video, output_path)
    
    print(f"\n🎬 Fixed stacked blur test complete!")
    print(f"Input: {input_video}")
    print(f"Output: {output_path}")

if __name__ == "__main__":
    # Test the fixed stacked blur first
    print("Testing fixed stacked blur effect...")
    test_with_existing_video()
    
    print("\n" + "="*50)
    print("Testing complete workflow with CSV data...")
    test_with_csv_data()