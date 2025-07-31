import subprocess
import os

def create_improved_intro(output_file, player_name, team, fantasy_points, rank, silhouette_path):
    """Create improved modern intro with position next to rank and curved edges"""
    
    # Clean player name
    player_name_clean = player_name.replace("'", "").replace(" ", " ")
    
    # Check if silhouette exists
    if not os.path.exists(silhouette_path):
        print(f"Warning: Silhouette not found at {silhouette_path}")
        create_without_silhouette = True
    else:
        create_without_silhouette = False
        print(f"Using silhouette from: {silhouette_path}")
    
    if create_without_silhouette:
        # Modern design without silhouette
        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', 'color=color=black@0.0:size=1080x1920:duration=1',
            '-vf', (
                # Gradient background overlay (subtle, maintains transparency)
                "drawbox=x=0:y=0:w=1080:h=1920:color=0x0f172a@0.8:t=fill,"
                
                # Ultra-modern card with rounded corners simulation
                "drawbox=x=60:y=480:w=960:h=940:color=0xffffff:t=fill,"
                "drawbox=x=65:y=485:w=950:h=930:color=0xffffff:t=fill,"
                "drawbox=x=70:y=490:w=940:h=920:color=0xffffff:t=fill,"
                "drawbox=x=75:y=495:w=930:h=910:color=0xffffff:t=fill,"
                "drawbox=x=80:y=500:w=920:h=900:color=0xffffff:t=fill,"
                
                # Pure white background for silhouette area
                "drawbox=x=90:y=510:w=900:h=450:color=white:t=fill,"
                
                # Silhouette placeholder
                "drawbox=x=400:y=600:w=280:h=280:color=0xe2e8f0:t=fill,"
                "drawtext=text='PLAYER SILHOUETTE':"
                "fontsize=24:fontcolor=0x64748b:x=(w-text_w)/2:y=750,"
                
                # Modern divider line
                "drawbox=x=120:y=960:w=840:h=3:color=0x6366f1:t=fill,"
                
                # Player name
                f"drawtext=text='{player_name_clean}':"
                "fontsize=72:fontcolor=0x0f172a:x=120:y=1000,"
                
                # Team and position side by side
                f"drawtext=text='{team}':"
                "fontsize=36:fontcolor=0x6366f1:x=120:y=1090,"
                "drawtext=text='WR':"  # Position next to team
                "fontsize=36:fontcolor=0x64748b:x=200:y=1090,"
                
                # Fantasy points
                f"drawtext=text='2024 Fantasy Points':"
                "fontsize=32:fontcolor=0x64748b:x=120:y=1150,"
                f"drawtext=text='{fantasy_points}':"
                "fontsize=48:fontcolor=0x059669:x=120:y=1190,"
                
                # Modern rank badge with position - curved design
                "drawbox=x=820:y=510:w=180:h=80:color=0x0f172a:t=fill,"
                "drawbox=x=823:y=513:w=174:h=74:color=0x1e293b:t=fill,"
                "drawbox=x=826:y=516:w=168:h=68:color=0x334155:t=fill,"
                "drawbox=x=829:y=519:w=162:h=62:color=0x475569:t=fill,"
                f"drawtext=text='#{rank} WR':"
                "fontsize=32:fontcolor=white:x=(820+90-text_w/2):y=540,"
                
                # Top title
                "drawbox=x=0:y=200:w=1080:h=80:color=0x1e293b:t=fill,"
                "drawtext=text='TOP 100 FANTASY WRs 2024':"
                "fontsize=36:fontcolor=white:x=(w-text_w)/2:y=225"
            ),
            '-frames:v', '1',
            '-pix_fmt', 'rgba',
            '-y',
            output_file
        ]
    else:
        # Modern design with silhouette
        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', 'color=color=black@0.0:size=1080x1920:duration=1',
            '-i', silhouette_path,
            '-filter_complex', (
                # Scale and prepare silhouette
                "[1:v]scale=320:320,format=rgba[silhouette];"
                "[0:v]"
                # Modern gradient background (with transparency)
                "drawbox=x=0:y=0:w=1080:h=1920:color=0x0f172a@0.8:t=fill,"
                
                # Ultra-modern card with rounded corners simulation
                "drawbox=x=60:y=480:w=960:h=940:color=0xffffff:t=fill,"
                "drawbox=x=65:y=485:w=950:h=930:color=0xffffff:t=fill,"
                "drawbox=x=70:y=490:w=940:h=920:color=0xffffff:t=fill,"
                "drawbox=x=75:y=495:w=930:h=910:color=0xffffff:t=fill,"
                "drawbox=x=80:y=500:w=920:h=900:color=0xffffff:t=fill,"
                
                # Pure white background for silhouette area
                "drawbox=x=90:y=510:w=900:h=450:color=white:t=fill,"
                
                # Ultra-thin modern divider
                "drawbox=x=100:y=970:w=880:h=1:color=0xe2e8f0:t=fill,"
                "drawbox=x=100:y=971:w=880:h=1:color=0x6366f1@0.2:t=fill,"
                
                # Player name with ultra-modern typography
                f"drawtext=text='{player_name_clean}':"
                "fontsize=64:fontcolor=0x111827:x=100:y=990,"
                
                # Team with modern styling
                f"drawtext=text='{team}':"
                "fontsize=36:fontcolor=0x6366f1:x=100:y=1070,"
                
                # Stats section with modern layout
                f"drawtext=text='2024 Fantasy Points':"
                "fontsize=24:fontcolor=0x9ca3af:x=100:y=1130,"
                f"drawtext=text='{fantasy_points}':"
                "fontsize=48:fontcolor=0x10b981:x=100:y=1160,"
                
                # Modern rank badge with position - curved design
                "drawbox=x=820:y=510:w=180:h=80:color=0x0f172a:t=fill,"
                "drawbox=x=823:y=513:w=174:h=74:color=0x1e293b:t=fill,"
                "drawbox=x=826:y=516:w=168:h=68:color=0x334155:t=fill,"
                "drawbox=x=829:y=519:w=162:h=62:color=0x475569:t=fill,"
                f"drawtext=text='#{rank} WR':"
                "fontsize=32:fontcolor=white:x=(820+90-text_w/2):y=540,"
                
                # Ultra-modern top banner
                "drawbox=x=0:y=160:w=1080:h=120:color=0x0f172a:t=fill,"
                "drawbox=x=0:y=160:w=1080:h=120:color=0x6366f1@0.1:t=fill,"
                "drawtext=text='TOP 100 FANTASY WRs 2024':"
                "fontsize=32:fontcolor=0xf8fafc:x=(w-text_w)/2:y=205,"
                
                # Subtle modern card shadow effect
                "drawbox=x=60:y=480:w=960:h=2:color=0xe2e8f0:t=fill,"
                "drawbox=x=60:y=1418:w=960:h=2:color=0xe2e8f0:t=fill[bg];"
                
                # Overlay silhouette in clean white area
                "[bg][silhouette]overlay=380:590"
            ),
            '-frames:v', '1',
            '-pix_fmt', 'rgba',
            '-y',
            output_file
        ]
    
    try:
        print(f"Creating improved intro for {player_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success! Created: {output_file}")
            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / 1024
                print(f"  📏 File size: {size:.1f} KB")
                print(f"  🎨 Improvements:")
                print(f"     • Position (WR) next to team")
                print(f"     • Curved edges with layered boxes")
                print(f"     • Pure white silhouette background")
                print(f"     • Enhanced rank badge depth")
            return True
        else:
            print(f"❌ Error occurred")
            print("STDERR:", result.stderr[:1000])
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    # Test with improved design
    success = create_improved_intro(
        'video_clips/improved_intro_test.png',
        "Ja'Marr Chase",
        'CIN',
        '276.0',
        '1',
        '/Users/nickfrische/Desktop/Fantasy project/wr_sillouette.avif'
    )
    
    if success:
        print(f"\n🎉 Improved modern intro created!")
        print(f"📁 Check: video_clips/improved_intro_test.png")
    else:
        print("\n❌ Failed to create improved intro.")

if __name__ == "__main__":
    main()