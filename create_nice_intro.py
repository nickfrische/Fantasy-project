import subprocess
import os

def create_nice_intro_image(output_file, player_name, team, fantasy_points, rank, silhouette_path):
    """Create a nice intro image with silhouette and stats"""
    
    # Clean player name
    player_name_clean = player_name.replace("'", "")
    
    # Check if silhouette exists
    if not os.path.exists(silhouette_path):
        print(f"Warning: Silhouette not found at {silhouette_path}")
        # Create without silhouette first
        create_without_silhouette = True
    else:
        create_without_silhouette = False
    
    if create_without_silhouette:
        # Create without silhouette
        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', 'color=black:size=1920x1080:duration=1',
            '-vf', (
                # Main background box
                "drawbox=x=360:y=200:w=1200:h=680:color=white@0.9:t=fill,"
                "drawbox=x=360:y=200:w=1200:h=680:color=blue:t=4,"
                
                # Top section for silhouette placeholder
                "drawbox=x=370:y=210:w=1180:h=400:color=gray@0.3:t=fill,"
                "drawtext=text='PLAYER SILHOUETTE':"
                "fontsize=30:fontcolor=white:x=(w-text_w)/2:y=410,"
                
                # Divider line
                "drawbox=x=370:y=620:w=1180:h=4:color=blue:t=fill,"
                
                # Player name
                f"drawtext=text='{player_name_clean}':"
                "fontsize=48:fontcolor=black:x=390:y=650,"
                
                # Team
                f"drawtext=text='{team}':"
                "fontsize=36:fontcolor=gray:x=390:y=710,"
                
                # Fantasy points
                f"drawtext=text='2024 Fantasy Points: {fantasy_points}':"
                "fontsize=36:fontcolor=black:x=390:y=760,"
                
                # Rank overlay
                f"drawbox=x=1400:y=220:w=140:h=140:color=red:t=fill,"
                f"drawtext=text='#{rank}':"
                "fontsize=48:fontcolor=white:x=1420:y=270"
            ),
            '-frames:v', '1',
            '-y',
            output_file
        ]
    else:
        # Create with silhouette
        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', 'color=black:size=1920x1080:duration=1',
            '-i', silhouette_path,
            '-filter_complex', (
                # Scale and position silhouette
                "[1:v]scale=400:400[silhouette];"
                "[0:v]"
                # Main background box
                "drawbox=x=360:y=200:w=1200:h=680:color=white@0.9:t=fill,"
                "drawbox=x=360:y=200:w=1200:h=680:color=blue:t=4,"
                
                # Divider line
                "drawbox=x=370:y=620:w=1180:h=4:color=blue:t=fill,"
                
                # Player name
                f"drawtext=text='{player_name_clean}':"
                "fontsize=48:fontcolor=black:x=390:y=650,"
                
                # Team
                f"drawtext=text='{team}':"
                "fontsize=36:fontcolor=gray:x=390:y=710,"
                
                # Fantasy points
                f"drawtext=text='2024 Fantasy Points: {fantasy_points}':"
                "fontsize=36:fontcolor=black:x=390:y=760,"
                
                # Rank overlay
                f"drawbox=x=1400:y=220:w=140:h=140:color=red:t=fill,"
                f"drawtext=text='#{rank}':"
                "fontsize=48:fontcolor=white:x=1420:y=270[bg];"
                
                # Overlay silhouette
                "[bg][silhouette]overlay=760:250"
            ),
            '-frames:v', '1',
            '-y',
            output_file
        ]
    
    try:
        print(f"Creating nice intro image for {player_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Success! Created: {output_file}")
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"  File size: {size} bytes")
            return True
        else:
            print(f"✗ Error occurred")
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False

def main():
    # Test with Ja'Marr Chase data
    test_image = {
        'output': 'video_clips/nice_intro_test.png',
        'name': "Ja'Marr Chase",
        'team': 'CIN',
        'points': '276.0',
        'rank': 1,
        'silhouette': '/Users/nickfrische/Desktop/Fantasy project/wr_sillouette.avif'
    }
    
    print("Creating nice intro design...\n")
    
    success = create_nice_intro_image(
        test_image['output'],
        test_image['name'],
        test_image['team'],
        test_image['points'],
        test_image['rank'],
        test_image['silhouette']
    )
    
    if success:
        print(f"\n✓ Nice intro image created!")
        print(f"Check the file: {test_image['output']}")
        print("This shows the new layout with player stats and design.")
    else:
        print("\n✗ Image creation failed.")

if __name__ == "__main__":
    main()