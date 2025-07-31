import subprocess
import os

def add_intro_overlay(input_file, output_file, player_name, rank):
    """Add a 2-second intro overlay to cover blurry beginning"""
    
    # Create the intro text
    intro_text = f"Counting down the Top 100 Fantasy WRs of 2024\\n\\n{player_name}\\n\\nNumber {rank}"
    
    # FFmpeg command with text overlay for first 2 seconds
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', (
            # Create a dark semi-transparent overlay for first 2 seconds
            f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.8:t=fill:enable='between(t,0,2)',"
            # Add the intro text with nice styling
            f"drawtext=text='{intro_text}':"
            "fontfile=/System/Library/Fonts/Helvetica.ttc:"
            "fontsize=48:"
            "fontcolor=white:"
            "x=(w-text_w)/2:"
            "y=(h-text_h)/2:"
            "enable='between(t,0,2)':"
            "line_spacing=20"
        ),
        '-c:a', 'copy',  # Copy audio without re-encoding
        '-y',  # Overwrite output file
        output_file
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ Created intro for {player_name}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error processing {player_name}: {e.stderr}")

def main():
    # Define the videos to process
    videos = [
        {
            'input': 'video_clips/JaMarr_Chase_highlights.mp4.webm',
            'output': 'video_clips/JaMarr_Chase_with_intro.mp4',
            'name': 'Ja\'Marr Chase',
            'rank': 1
        },
        {
            'input': 'video_clips/Justin_Jefferson_highlights.mp4.webm',
            'output': 'video_clips/Justin_Jefferson_with_intro.mp4',
            'name': 'Justin Jefferson',
            'rank': 2
        },
        {
            'input': 'video_clips/Amon-Ra_St_Brown_highlights.mp4.webm',
            'output': 'video_clips/Amon-Ra_St_Brown_with_intro.mp4',
            'name': 'Amon-Ra St. Brown',
            'rank': 3
        }
    ]
    
    print("Adding intro overlays to videos...")
    
    for video in videos:
        if os.path.exists(video['input']):
            add_intro_overlay(
                video['input'],
                video['output'],
                video['name'],
                video['rank']
            )
        else:
            print(f"✗ Input file not found: {video['input']}")
    
    print("\nAll videos processed!")

if __name__ == "__main__":
    main()