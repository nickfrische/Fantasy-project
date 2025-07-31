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
            print("STDERR:", result.stderr[:500])  # Show first 500 chars of error
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")

def main():
    # Test with Ja'Marr Chase
    test_video = {
        'input': 'video_clips/JaMarr_Chase_highlights.mp4.webm',
        'output': 'video_clips/JaMarr_Chase_boxed_test.mp4',
        'name': "Ja'Marr Chase",
        'rank': 1
    }
    
    if os.path.exists(test_video['input']):
        add_boxed_intro(
            test_video['input'],
            test_video['output'],
            test_video['name'],
            test_video['rank']
        )
        
        # Check if file was created
        if os.path.exists(test_video['output']):
            size = os.path.getsize(test_video['output']) / (1024*1024)  # MB
            print(f"\nOutput file size: {size:.1f} MB")
            print("\nTo process all videos, update the script with all player info.")
    else:
        print(f"Input file not found: {test_video['input']}")

if __name__ == "__main__":
    main()