import subprocess
import os

def create_simple_nice_intro(output_file, player_name, team, fantasy_points, rank):
    """Create a clean intro design without complex filters"""
    
    # Clean player name
    player_name_clean = player_name.replace("'", "").replace(" ", "_")
    
    # Create without silhouette first to test the layout
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', 'color=black:size=1920x1080:duration=1',
        '-vf', (
            # Main white background box
            "drawbox=x=360:y=200:w=1200:h=680:color=white@0.95:t=fill,"
            # Blue border
            "drawbox=x=360:y=200:w=1200:h=680:color=0x4169E1:t=8,"
            
            # Top section (silhouette area) - light gray
            "drawbox=x=380:y=220:w=1160:h=380:color=0xF0F0F0:t=fill,"
            "drawbox=x=380:y=220:w=1160:h=380:color=0xCCCCCC:t=2,"
            
            # Placeholder text for silhouette
            "drawtext=text='PLAYER_SILHOUETTE':"
            "fontsize=24:fontcolor=0x666666:x=(w-text_w)/2:y=400,"
            
            # Divider line
            "drawbox=x=380:y=610:w=1160:h=4:color=0x4169E1:t=fill,"
            
            # Player name - large and bold
            f"drawtext=text='{player_name_clean}':"
            "fontsize=52:fontcolor=black:x=400:y=640,"
            
            # Team abbreviation
            f"drawtext=text='{team}':"
            "fontsize=36:fontcolor=0x666666:x=400:y=710,"
            
            # Fantasy points
            f"drawtext=text='2024_Fantasy_Points_{fantasy_points}':"
            "fontsize=32:fontcolor=black:x=400:y=760,"
            
            # Rank badge - red circle
            "drawbox=x=1400:y=230:w=120:h=120:color=red:t=fill,"
            f"drawtext=text='{rank}':"
            "fontsize=48:fontcolor=white:x=(1400+60-text_w/2):y=270"
        ),
        '-frames:v', '1',
        '-y',
        output_file
    ]
    
    try:
        print(f"Creating simple nice intro for {player_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Success! Created: {output_file}")
            return True
        else:
            print(f"✗ Error occurred")
            print("STDERR:", result.stderr[:1000])  # First 1000 chars
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False

def main():
    # Test with Ja'Marr Chase data
    success = create_simple_nice_intro(
        'video_clips/simple_nice_intro_test.png',
        "Ja'Marr Chase",
        'CIN',
        '276.0',
        '1'
    )
    
    if success:
        print(f"\n✓ Simple nice intro created!")
        print(f"Check: video_clips/simple_nice_intro_test.png")
    else:
        print("\n✗ Failed to create intro.")

if __name__ == "__main__":
    main()