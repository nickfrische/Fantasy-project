import subprocess
import os

def add_intro_overlay(input_file, output_file, player_name, rank):
    """Add a 2-second intro overlay with simple text"""
    
    # Escape single quotes in player name
    player_name_escaped = player_name.replace("'", "\\'")
    
    # FFmpeg command with simpler text overlay
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', (
            # Black background for first 2 seconds
            "drawbox=x=0:y=0:w=iw:h=ih:color=black:t=fill:enable='between(t,0,2)',"
            # Main title
            "drawtext=text='COUNTING DOWN THE TOP 100 FANTASY WRs OF 2024':"
            "fontsize=40:fontcolor=white:x=(w-text_w)/2:y=h/2-150:"
            "enable='between(t,0,2)',"
            # Player name
            f"drawtext=text='{player_name_escaped}':"
            "fontsize=60:fontcolor=yellow:x=(w-text_w)/2:y=h/2:"
            "enable='between(t,0,2)',"
            # Rank
            f"drawtext=text='NUMBER {rank}':"
            "fontsize=50:fontcolor=white:x=(w-text_w)/2:y=h/2+100:"
            "enable='between(t,0,2)'"
        ),
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-c:a', 'copy',
        '-y',
        output_file
    ]
    
    try:
        print(f"Processing {player_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Created intro for {player_name}")
            print(f"Output saved to: {output_file}")
        else:
            print(f"✗ Error processing {player_name}")
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"✗ Exception processing {player_name}: {str(e)}")

def main():
    # Test with first video
    video = {
        'input': 'video_clips/JaMarr_Chase_highlights.mp4.webm',
        'output': 'video_clips/JaMarr_Chase_with_intro.mp4',
        'name': "Ja'Marr Chase",
        'rank': 1
    }
    
    print("Creating intro overlay...")
    
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