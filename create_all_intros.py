import subprocess
import os

def add_boxed_intro(input_file, output_file, player_name, rank):
    """Add intro with text in boxes to ensure visibility"""
    
    # Clean player name for ffmpeg
    player_name_clean = player_name.replace("'", "")
    
    # FFmpeg command with boxed text
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', (
            # Full screen dark overlay for first 2 seconds
            "drawbox=x=0:y=0:w=iw:h=ih:color=black@0.9:t=fill:enable='between(t,0,2)',"
            
            # Title with box background
            "drawtext=text='TOP 100 FANTASY WRs 2024':"
            "fontsize=45:"
            "fontcolor=white:"
            "box=1:"
            "boxcolor=black:"
            "boxborderw=15:"
            "x=(w-text_w)/2:"
            "y=h/2-150:"
            "enable='between(t,0,2)',"
            
            # Player name with yellow text and box
            f"drawtext=text='{player_name_clean}':"
            "fontsize=65:"
            "fontcolor=yellow:"
            "box=1:"
            "boxcolor=black:"
            "boxborderw=15:"
            "x=(w-text_w)/2:"
            "y=h/2-20:"
            "enable='between(t,0,2)',"
            
            # Rank with box
            f"drawtext=text='NUMBER {rank}':"
            "fontsize=50:"
            "fontcolor=white:"
            "box=1:"
            "boxcolor=black:"
            "boxborderw=15:"
            "x=(w-text_w)/2:"
            "y=h/2+80:"
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
        print(f"Creating intro for {player_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Success! Created: {output_file}")
        else:
            print(f"✗ Error occurred")
            print("STDERR:", result.stderr[:500])
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")

def main():
    # All three videos to process
    videos = [
        {
            'input': 'video_clips/JaMarr_Chase_highlights.mp4.webm',
            'output': 'video_clips/JaMarr_Chase_FINAL.mp4',
            'name': "Ja'Marr Chase",
            'rank': 1
        },
        {
            'input': 'video_clips/Justin_Jefferson_highlights.mp4.webm',
            'output': 'video_clips/Justin_Jefferson_FINAL.mp4',
            'name': 'Justin Jefferson',
            'rank': 2
        },
        {
            'input': 'video_clips/Amon-Ra_St_Brown_highlights.mp4.webm',
            'output': 'video_clips/Amon-Ra_St_Brown_FINAL.mp4',
            'name': 'Amon-Ra St. Brown',
            'rank': 3
        }
    ]
    
    print("Creating intro overlays for all videos...\n")
    
    for video in videos:
        if os.path.exists(video['input']):
            add_boxed_intro(
                video['input'],
                video['output'],
                video['name'],
                video['rank']
            )
            print()  # Empty line for readability
        else:
            print(f"✗ Input file not found: {video['input']}\n")
    
    print("All videos processed!")
    print("\nFinal videos created:")
    for video in videos:
        if os.path.exists(video['output']):
            size = os.path.getsize(video['output']) / (1024*1024)
            print(f"  • {video['output']} ({size:.1f} MB)")

if __name__ == "__main__":
    main()