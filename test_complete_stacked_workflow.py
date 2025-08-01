#!/usr/bin/env python3
import subprocess
import os
import csv
from pathlib import Path

# Import functions from main script
import sys
sys.path.append('/Users/nickfrische/Desktop/Fantasy project')
from create_wr_instagram_video import create_wr_intro, download_youtube_video

def create_perfect_stacked_blur_video(input_video, output_path):
    """Create perfect stacked blur video - EXACTLY like the working version!"""
    
    width, height = 1080, 1920
    
    # EXACT proportions from the working version
    blur_section_height = 480  # Top and bottom blur sections
    main_section_height = 960  # Center section (larger for main content)
    
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-filter_complex', (
            # First convert to Instagram format, then create three copies
            f'scale=w=\'min({width},iw*{height}/ih)\':h=\'min({height},ih*{width}/iw)\','
            f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,'
            f'setsar=1[instagram];'
            f'[instagram]split=3[main][top][bottom];'
            
            # Main video in center - crop to center section size (EXACT WORKING METHOD)
            f'[main]crop={width}:{main_section_height}:0:(ih-{main_section_height})/2[main_cropped];'
            
            # Top blur section - crop top portion and blur heavily (AMAZING BLUR!)
            f'[top]crop={width}:{blur_section_height}:0:0,'
            f'gblur=sigma=30[top_blur];'
            
            # Bottom blur section - crop bottom portion and blur heavily (AMAZING BLUR!)
            f'[bottom]crop={width}:{blur_section_height}:0:ih-{blur_section_height},'
            f'gblur=sigma=30[bottom_blur];'
            
            # Stack all three sections vertically
            f'[top_blur][main_cropped][bottom_blur]vstack=inputs=3[final]'
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
    
    print(f"Creating AMAZING stacked blur video (EXACTLY like working version)...")
    print(f"Input: {input_video}")
    print(f"Output: {output_path}")
    
    subprocess.run(cmd, check=True)
    print(f"✅ AMAZING stacked blur video created: {output_path}")

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
    
    print("Concatenating geometric intro with perfect stacked blur video...")
    try:
        subprocess.run(cmd, check=True)
    finally:
        if os.path.exists(concat_list):
            os.remove(concat_list)
    
    print(f"✅ Final video created: {output_path}")

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

def process_wr_complete_stacked_workflow(player_name, team, fantasy_points, rank, youtube_url, output_dir="output"):
    """Complete workflow: Geometric intro + Perfect stacked blur highlights"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # File paths
    safe_name = player_name.replace("'", "").replace(" ", "_")
    intro_path = f"{output_dir}/{safe_name}_geometric_intro.mp4"
    youtube_path = f"{output_dir}/{safe_name}_youtube_raw.mp4"
    stacked_path = f"{output_dir}/{safe_name}_perfect_stacked.mp4"
    final_path = f"{output_dir}/{safe_name}_COMPLETE_STACKED.mp4"
    
    print(f"\n🎬 COMPLETE STACKED WORKFLOW: {player_name} (#{rank})")
    print(f"Team: {team} | Fantasy Points: {fantasy_points}")
    print(f"YouTube: {youtube_url}")
    print("="*60)
    
    # Step 1: Create geometric intro (2 seconds)
    print("📱 Step 1: Creating minimal geometric intro...")
    create_wr_intro(player_name, team, fantasy_points, rank, intro_path)
    
    # Step 2: Download YouTube video (30 seconds)
    print("📥 Step 2: Downloading YouTube highlights...")
    download_youtube_video(youtube_url, youtube_path, duration=30)
    
    # Step 3: Create stacked blur version DIRECTLY from YouTube video (this is the key!)
    print("✨ Step 3: Creating AMAZING stacked blur effect...")
    create_perfect_stacked_blur_video(youtube_path, stacked_path)
    
    # Step 4: Concatenate intro + stacked blur video
    print("🎞️  Step 4: Combining intro with stacked blur highlights...")
    concatenate_videos(intro_path, stacked_path, final_path)
    
    # Cleanup intermediate files
    print("🧹 Step 5: Cleaning up intermediate files...")
    for path in [intro_path, youtube_path, stacked_path]:
        if os.path.exists(path):
            os.remove(path)
            print(f"   Removed: {os.path.basename(path)}")
    
    print("="*60)
    print(f"🏆 SUCCESS! Complete stacked video created:")
    print(f"📁 {final_path}")
    print("="*60)
    
    return final_path

def test_complete_stacked_workflow():
    """Test complete workflow with next unposted player from CSV"""
    
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
            
            print(f"\n🏈 TESTING COMPLETE STACKED WORKFLOW")
            print(f"Player: {player_name} (#{rank}) - {team}")
            
            try:
                final_video = process_wr_complete_stacked_workflow(
                    player_name, team, fantasy_points, rank, youtube_url
                )
                
                print(f"\n🎉 COMPLETE SUCCESS!")
                print(f"📱 Ready for Instagram: {final_video}")
                print("\nThis video includes:")
                print("✅ 2-second minimal geometric intro")
                print("✅ 30 seconds of perfectly centered highlights")
                print("✅ Amazing blur effects (top & bottom)")
                print("✅ Professional Instagram 9:16 format")
                
                return final_video
                
            except Exception as e:
                print(f"\n❌ Error in complete workflow: {e}")
                return None
    
    print("All WRs have been posted!")
    return None

if __name__ == "__main__":
    print("🚀 TESTING COMPLETE STACKED WORKFLOW")
    print("Geometric Intro + Perfect Stacked Blur Highlights")
    print("="*60)
    
    test_complete_stacked_workflow()