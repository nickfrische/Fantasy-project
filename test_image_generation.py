import subprocess
import os

def create_test_image(output_file, player_name, rank):
    """Create a test image with the intro text to verify it works"""
    
    # Clean player name
    player_name_clean = player_name.replace("'", "")
    
    # Create a 1920x1080 black image with text
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', 'color=black:size=1920x1080:duration=1',
        '-vf', (
            # Title text
            "drawtext=text='TOP 100 FANTASY WRs 2024':"
            "fontsize=45:"
            "fontcolor=white:"
            "box=1:"
            "boxcolor=red@0.8:"
            "boxborderw=15:"
            "x=(w-text_w)/2:"
            "y=h/2-150,"
            
            # Player name
            f"drawtext=text='{player_name_clean}':"
            "fontsize=65:"
            "fontcolor=yellow:"
            "box=1:"
            "boxcolor=blue@0.8:"
            "boxborderw=15:"
            "x=(w-text_w)/2:"
            "y=h/2-20,"
            
            # Rank
            f"drawtext=text='NUMBER {rank}':"
            "fontsize=50:"
            "fontcolor=white:"
            "box=1:"
            "boxcolor=green@0.8:"
            "boxborderw=15:"
            "x=(w-text_w)/2:"
            "y=h/2+80"
        ),
        '-frames:v', '1',
        '-y',
        output_file
    ]
    
    try:
        print(f"Creating test image for {player_name}...")
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
    # Test image creation
    test_image = {
        'output': 'video_clips/test_intro_image.png',
        'name': "Ja'Marr Chase",
        'rank': 1
    }
    
    print("Testing image generation with intro text...\n")
    
    success = create_test_image(
        test_image['output'],
        test_image['name'],
        test_image['rank']
    )
    
    if success:
        print(f"\n✓ Test image created successfully!")
        print(f"Check the file: {test_image['output']}")
        print("If you can see the text in the image, then we know the text rendering works.")
        print("The colored boxes (red, blue, green) help us see each text element.")
    else:
        print("\n✗ Image creation failed. Let's debug the issue.")

if __name__ == "__main__":
    main()