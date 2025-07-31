import subprocess
import os

def add_intro_overlay(input_file, output_file, player_name, rank):
    """Add a 2-second intro overlay to video"""
    
    # Remove apostrophes from player names for ffmpeg
    player_name_clean = player_name.replace("'", "")
    
    # FFmpeg command
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
            f"drawtext=text='{player_name_clean}':"
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
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ Created intro for {player_name}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error processing {player_name}: {e.stderr}")

def main():
    # Define all videos to process
    videos = [
        {
            'input': 'video_clips/JaMarr_Chase_highlights.mp4.webm',
            'output': 'video_clips/JaMarr_Chase_final.mp4',
            'name': "Ja'Marr Chase",
            'rank': 1
        },
        {
            'input': 'video_clips/Justin_Jefferson_highlights.mp4.webm',
            'output': 'video_clips/Justin_Jefferson_final.mp4',
            'name': 'Justin Jefferson',
            'rank': 2
        },
        {
            'input': 'video_clips/Amon-Ra_St_Brown_highlights.mp4.webm',
            'output': 'video_clips/Amon-Ra_St_Brown_final.mp4',
            'name': 'Amon-Ra St. Brown',
            'rank': 3
        }
    ]
    
    print("Creating intro overlays for all videos...\n")
    
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