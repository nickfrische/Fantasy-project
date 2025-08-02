#!/usr/bin/env python3
import subprocess
import os
import csv
from pathlib import Path

# Import the intro function from the main script
import sys
sys.path.append('/Users/nickfrische/Desktop/Fantasy project')
from create_wr_instagram_video import create_wr_intro, download_youtube_video

def create_blur_touch_v3_video(input_video, output_path):
    """
    Version 3: Even more zoomed (130%)
    - 640px blur sections
    - Middle video zoomed to 130% for dramatic effect
    """
    
    width, height = 1080, 1920
    
    blur_section_height = 640
    main_section_height = 640
    
    # Zoom the middle video by 130%
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
    
    print(f"Touch V3: 130% zoom, blur={blur_section_height}px")
    subprocess.run(cmd, check=True)

def test_blur_touch_v3():
    csv_path = "wr_top100_with_links.csv"
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    for row in rows:
        if row['Posted'].lower() == 'false':
            player_name = row['PlayerName']
            youtube_url = row['YouTubeLink']
            
            safe_name = player_name.replace("'", "").replace(" ", "_")
            youtube_path = f"output/{safe_name}_youtube_raw.mp4"
            final_path = f"output/{safe_name}_TOUCH_V3_130zoom.mp4"
            
            print(f"Testing Touch V3 with {player_name}...")
            download_youtube_video(youtube_url, youtube_path, duration=10)
            create_blur_touch_v3_video(youtube_path, final_path)
            
            if os.path.exists(youtube_path):
                os.remove(youtube_path)
            
            print(f"✅ Touch V3: {final_path}")
            return final_path

if __name__ == "__main__":
    test_blur_touch_v3()