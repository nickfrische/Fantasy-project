import subprocess
import os

def add_intro_overlay(input_file, output_file, player_name, rank):
    """Add a 2-second intro overlay with better formatting"""
    
    # FFmpeg command to add intro overlay
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', (
            # Create multiple text elements with better styling
            # Background box
            "drawbox=x=(iw-800)/2:y=(ih-400)/2:w=800:h=400:color=black@0.8:t=fill:enable='between(t,0,2)',"
            # Title text
            "drawtext=text='COUNTING DOWN THE TOP 100':"
            "fontfile=/System/Library/Fonts/Avenir.ttc:fontsize=36:"
            "fontcolor=white:x=(w-text_w)/2:y=(h-400)/2:"
            "enable='between(t,0,2)',"
            # Subtitle text
            "drawtext=text='FANTASY WRs OF 2024':"
            "fontfile=/System/Library/Fonts/Avenir.ttc:fontsize=36:"
            "fontcolor=white:x=(w-text_w)/2:y=(h-300)/2:"
            "enable='between(t,0,2)',"
            # Player name
            f"drawtext=text='{player_name}':"
            "fontfile=/System/Library/Fonts/Avenir.ttc:fontsize=60:"
            "fontcolor=yellow:x=(w-text_w)/2:y=(h-100)/2:"
            "enable='between(t,0,2)',"
            # Rank number
            f"drawtext=text='NUMBER {rank}':"
            "fontfile=/System/Library/Fonts/Avenir.ttc:fontsize=48:"
            "fontcolor=white:x=(w-text_w)/2:y=(h+100)/2:"
            "enable='between(t,0,2)'"
        ),
        '-c:v', 'libx264',  # Use H.264 codec for better compatibility
        '-preset', 'fast',
        '-crf', '23',
        '-c:a', 'copy',  # Copy audio without re-encoding
        '-y',  # Overwrite output file
        output_file
    ]
    
    try:
        print(f"Processing {player_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Created intro for {player_name}")
        else:
            print(f"✗ Error processing {player_name}")
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"✗ Exception processing {player_name}: {str(e)}")

def main():
    # Test with just the first video
    video = {
        'input': 'video_clips/JaMarr_Chase_highlights.mp4.webm',
        'output': 'video_clips/JaMarr_Chase_with_intro.mp4',
        'name': 'Ja\'Marr Chase',
        'rank': 1
    }
    
    print("Testing intro overlay with first video...")
    
    if os.path.exists(video['input']):
        add_intro_overlay(
            video['input'],
            video['output'],
            video['name'],
            video['rank']
        )
    else:
        print(f"✗ Input file not found: {video['input']}")

if __name__ == "__main__":
    main()