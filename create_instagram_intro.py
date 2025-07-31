import subprocess
import os

def create_instagram_intro(output_file, player_name, team, fantasy_points, rank, silhouette_path):
    """Create Instagram Reel optimized intro (9:16 aspect ratio)"""
    
    # Clean player name
    player_name_clean = player_name.replace("'", "").replace(" ", "_")
    
    # Check if silhouette exists
    if not os.path.exists(silhouette_path):
        print(f"Warning: Silhouette not found at {silhouette_path}")
        print("Creating without silhouette...")
        create_without_silhouette = True
    else:
        create_without_silhouette = False
        print(f"Using silhouette from: {silhouette_path}")
    
    if create_without_silhouette:
        # Create without silhouette - Instagram Reel size (1080x1920)
        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', 'color=black:size=1080x1920:duration=1',
            '-vf', (
                # Main white background card
                "drawbox=x=100:y=400:w=880:h=1100:color=white@0.95:t=fill,"
                # Blue border
                "drawbox=x=100:y=400:w=880:h=1100:color=0x4169E1:t=8,"
                
                # Top section (silhouette placeholder)
                "drawbox=x=120:y=420:w=840:h=500:color=0xF0F0F0:t=fill,"
                "drawbox=x=120:y=420:w=840:h=500:color=0xCCCCCC:t=3,"
                
                # Placeholder text
                "drawtext=text='PLAYER_SILHOUETTE':"
                "fontsize=32:fontcolor=0x666666:x=(w-text_w)/2:y=650,"
                
                # Divider line
                "drawbox=x=120:y=930:w=840:h=6:color=0x4169E1:t=fill,"
                
                # Player name - large
                f"drawtext=text='{player_name_clean}':"
                "fontsize=64:fontcolor=black:x=140:y=970,"
                
                # Team abbreviation
                f"drawtext=text='{team}':"
                "fontsize=48:fontcolor=0x666666:x=140:y=1050,"
                
                # Fantasy points
                f"drawtext=text='2024_Fantasy_Points_{fantasy_points}':"
                "fontsize=40:fontcolor=black:x=140:y=1120,"
                
                # Rank badge - top right
                "drawbox=x=800:y=430:w=160:h=160:color=red:t=fill,"
                f"drawtext=text='{rank}':"
                "fontsize=72:fontcolor=white:x=(800+80-text_w/2):y=480,"
                
                # Title at top
                "drawtext=text='TOP_100_FANTASY_WRs_2024':"
                "fontsize=48:fontcolor=white:box=1:boxcolor=0x4169E1@0.8:boxborderw=20:"
                "x=(w-text_w)/2:y=200"
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
            '-i', 'color=black:size=1080x1920:duration=1',
            '-i', silhouette_path,
            '-filter_complex', (
                # Scale and prepare silhouette
                "[1:v]scale=400:400,format=rgba[silhouette];"
                "[0:v]"
                # Main card background
                "drawbox=x=100:y=400:w=880:h=1100:color=white@0.95:t=fill,"
                "drawbox=x=100:y=400:w=880:h=1100:color=0x4169E1:t=8,"
                
                # Divider line
                "drawbox=x=120:y=930:w=840:h=6:color=0x4169E1:t=fill,"
                
                # Player name
                f"drawtext=text='{player_name_clean}':"
                "fontsize=64:fontcolor=black:x=140:y=970,"
                
                # Team
                f"drawtext=text='{team}':"
                "fontsize=48:fontcolor=0x666666:x=140:y=1050,"
                
                # Fantasy points
                f"drawtext=text='2024_Fantasy_Points_{fantasy_points}':"
                "fontsize=40:fontcolor=black:x=140:y=1120,"
                
                # Rank badge
                "drawbox=x=800:y=430:w=160:h=160:color=red:t=fill,"
                f"drawtext=text='{rank}':"
                "fontsize=72:fontcolor=white:x=(800+80-text_w/2):y=480,"
                
                # Title at top
                "drawtext=text='TOP_100_FANTASY_WRs_2024':"
                "fontsize=48:fontcolor=white:box=1:boxcolor=0x4169E1@0.8:boxborderw=20:"
                "x=(w-text_w)/2:y=200[bg];"
                
                # Overlay silhouette in center of top section
                "[bg][silhouette]overlay=340:500"
            ),
            '-frames:v', '1',
            '-y',
            output_file
        ]
    
    try:
        print(f"Creating Instagram intro for {player_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Success! Created: {output_file}")
            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / 1024
                print(f"  File size: {size:.1f} KB")
                print(f"  Dimensions: 1080x1920 (Instagram Reel format)")
            return True
        else:
            print(f"✗ Error occurred")
            print("STDERR:", result.stderr[:1000])
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False

def main():
    # Test with silhouette
    success = create_instagram_intro(
        'video_clips/instagram_intro_test.png',
        "Ja'Marr Chase",
        'CIN',
        '276.0',
        '1',
        '/Users/nickfrische/Desktop/Fantasy project/wr_sillouette.avif'
    )
    
    if success:
        print(f"\n✅ Instagram Reel intro created!")
        print(f"📱 Perfect for social media posting")
        print(f"📁 Check: video_clips/instagram_intro_test.png")
    else:
        print("\n❌ Failed to create Instagram intro.")

if __name__ == "__main__":
    main()