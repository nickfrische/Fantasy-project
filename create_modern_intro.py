import subprocess
import os

def create_modern_intro(output_file, player_name, team, fantasy_points, rank, silhouette_path):
    """Create a modern, sleek Instagram intro with contemporary design"""
    
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
            '-i', 'color=0x0a0a0a:size=1080x1920:duration=1',  # Dark background
            '-vf', (
                # Gradient background overlay
                "drawbox=x=0:y=0:w=1080:h=1920:color=0x6366f1@0.1:t=fill,"
                
                # Main card with rounded corners effect (simulate with multiple boxes)
                "drawbox=x=80:y=500:w=920:h=900:color=white@0.98:t=fill,"
                "drawbox=x=82:y=502:w=916:h=896:color=0x6366f1@0.05:t=fill,"
                
                # Top gradient section
                "drawbox=x=80:y=500:w=920:h=450:color=0xf8fafc:t=fill,"
                "drawbox=x=80:y=500:w=920:h=450:color=0x6366f1@0.03:t=fill,"
                
                # Silhouette placeholder with modern styling
                "drawbox=x=400:y=600:w=280:h=280:color=0xe2e8f0:t=fill,"
                "drawbox=x=405:y=605:w=270:h=270:color=0x94a3b8@0.3:t=fill,"
                "drawtext=text='PLAYER':"
                "fontsize=24:fontcolor=0x64748b:x=(w-text_w)/2:y=720,"
                "drawtext=text='SILHOUETTE':"
                "fontsize=24:fontcolor=0x64748b:x=(w-text_w)/2:y=750,"
                
                # Modern divider line with gradient effect
                "drawbox=x=120:y=950:w=840:h=3:color=0x6366f1:t=fill,"
                "drawbox=x=120:y=953:w=840:h=1:color=0x6366f1@0.3:t=fill,"
                
                # Player name with modern typography
                f"drawtext=text='{player_name_clean}':"
                "fontsize=72:fontcolor=0x0f172a:x=120:y=990,"
                
                # Team with accent color
                f"drawtext=text='{team}':"
                "fontsize=36:fontcolor=0x6366f1:x=120:y=1080,"
                
                # Fantasy points with modern styling
                f"drawtext=text='2024 Fantasy Points':"
                "fontsize=32:fontcolor=0x64748b:x=120:y=1140,"
                f"drawtext=text='{fantasy_points}':"
                "fontsize=48:fontcolor=0x059669:x=120:y=1180,"
                
                # Modern rank badge with shadow effect
                "drawbox=x=850:y=520:w=120:h=120:color=0x6366f1:t=fill,"
                "drawbox=x=853:y=523:w=114:h=114:color=0x4f46e5:t=fill,"
                f"drawtext=text='{rank}':"
                "fontsize=56:fontcolor=white:x=(850+60-text_w/2):y=560,"
                
                # Top title with modern gradient background
                "drawbox=x=0:y=200:w=1080:h=80:color=0x1e293b:t=fill,"
                "drawbox=x=0:y=200:w=1080:h=80:color=0x6366f1@0.1:t=fill,"
                "drawtext=text='TOP 100 FANTASY WRs 2024':"
                "fontsize=36:fontcolor=white:x=(w-text_w)/2:y=225,"
                
                # Subtle accent elements
                "drawbox=x=80:y=500:w=920:h=4:color=0x6366f1:t=fill,"
                "drawbox=x=80:y=1396:w=920:h=4:color=0x6366f1:t=fill"
            ),
            '-frames:v', '1',
            '-y',
            output_file
        ]
    else:
        # Modern design with silhouette
        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', 'color=0x0a0a0a:size=1080x1920:duration=1',
            '-i', silhouette_path,
            '-filter_complex', (
                # Scale and prepare silhouette with modern effects
                "[1:v]scale=320:320,format=rgba,colorchannelmixer=aa=0.8[silhouette];"
                "[0:v]"
                # Modern gradient background
                "drawbox=x=0:y=0:w=1080:h=1920:color=0x6366f1@0.05:t=fill,"
                
                # Main card with glassmorphism effect
                "drawbox=x=80:y=500:w=920:h=900:color=white@0.95:t=fill,"
                "drawbox=x=82:y=502:w=916:h=896:color=0x6366f1@0.08:t=fill,"
                
                # Top section with subtle gradient
                "drawbox=x=80:y=500:w=920:h=450:color=0xf8fafc:t=fill,"
                "drawbox=x=80:y=500:w=920:h=450:color=0x6366f1@0.02:t=fill,"
                
                # Modern divider with glow effect
                "drawbox=x=120:y=950:w=840:h=3:color=0x6366f1:t=fill,"
                "drawbox=x=120:y=953:w=840:h=1:color=0x6366f1@0.5:t=fill,"
                "drawbox=x=118:y=948:w=844:h=1:color=0x6366f1@0.2:t=fill,"
                
                # Player name with premium typography
                f"drawtext=text='{player_name_clean}':"
                "fontsize=72:fontcolor=0x0f172a:x=120:y=990,"
                
                # Team with brand color
                f"drawtext=text='{team}':"
                "fontsize=40:fontcolor=0x6366f1:x=120:y=1080,"
                
                # Stats section with modern hierarchy
                f"drawtext=text='2024 Fantasy Points':"
                "fontsize=28:fontcolor=0x64748b:x=120:y=1140,"
                f"drawtext=text='{fantasy_points}':"
                "fontsize=56:fontcolor=0x059669:x=120:y=1175,"
                
                # Premium rank badge with depth
                "drawbox=x=850:y=520:w=130:h=130:color=0x1e40af:t=fill,"
                "drawbox=x=855:y=525:w=120:h=120:color=0x3b82f6:t=fill,"
                "drawbox=x=860:y=530:w=110:h=110:color=0x6366f1:t=fill,"
                f"drawtext=text='#{rank}':"
                "fontsize=44:fontcolor=white:x=(850+65-text_w/2):y=570,"
                
                # Top banner with modern gradient
                "drawbox=x=0:y=180:w=1080:h=100:color=0x1e293b:t=fill,"
                "drawbox=x=0:y=180:w=1080:h=100:color=0x6366f1@0.15:t=fill,"
                "drawtext=text='TOP 100 FANTASY WRs 2024':"
                "fontsize=38:fontcolor=white:x=(w-text_w)/2:y=215,"
                
                # Accent lines and borders
                "drawbox=x=80:y=500:w=920:h=2:color=0x6366f1:t=fill,"
                "drawbox=x=80:y=1398:w=920:h=2:color=0x6366f1:t=fill,"
                "drawbox=x=(w-400)/2:y=1350:w=400:h=2:color=0x6366f1@0.3:t=fill[bg];"
                
                # Overlay silhouette with modern positioning
                "[bg][silhouette]overlay=380:590"
            ),
            '-frames:v', '1',
            '-y',
            output_file
        ]
    
    try:
        print(f"Creating modern intro for {player_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success! Created: {output_file}")
            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / 1024
                print(f"  📏 File size: {size:.1f} KB")
                print(f"  📱 Format: 1080x1920 (Instagram Reel)")
                print(f"  🎨 Style: Modern UI/Glassmorphism")
            return True
        else:
            print(f"❌ Error occurred")
            print("STDERR:", result.stderr[:1000])
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    # Test with modern design
    success = create_modern_intro(
        'video_clips/modern_intro_test.png',
        "Ja'Marr Chase",
        'CIN',
        '276.0',
        '1',
        '/Users/nickfrische/Desktop/Fantasy project/wr_sillouette.avif'
    )
    
    if success:
        print(f"\n🎉 Modern Instagram intro created!")
        print(f"🚀 Features:")
        print(f"   • Glassmorphism design")
        print(f"   • Modern color palette (indigo/slate)")
        print(f"   • Clean typography hierarchy")
        print(f"   • Subtle gradients and shadows")
        print(f"   • Contemporary UI elements")
        print(f"📁 Check: video_clips/modern_intro_test.png")
    else:
        print("\n❌ Failed to create modern intro.")

if __name__ == "__main__":
    main()