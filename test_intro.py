import subprocess
import os

def create_intro_with_text(input_file, output_file, player_name, rank):
    """Create intro with guaranteed visible text"""
    
    # Clean player name
    player_name_clean = player_name.replace("'", "")
    
    # Create a complex filter that ensures text is visible
    filter_complex = [
        # Create a black color source for 2 seconds
        "[0:v]split[main][copy];",
        "[copy]trim=duration=2,geq=0:128:128[black];",
        
        # Add text to the black background
        "[black]",
        "drawtext=text='COUNTING DOWN THE TOP 100':fontsize=45:fontcolor=white:x=(w-text_w)/2:y=h/2-180:enable='between(t,0,2)',",
        "drawtext=text='FANTASY WRs OF 2024':fontsize=45:fontcolor=white:x=(w-text_w)/2:y=h/2-120:enable='between(t,0,2)',",
        f"drawtext=text='{player_name_clean}':fontsize=70:fontcolor=yellow:x=(w-text_w)/2:y=h/2:enable='between(t,0,2)',",
        f"drawtext=text='NUMBER {rank}':fontsize=55:fontcolor=white:x=(w-text_w)/2:y=h/2+100:enable='between(t,0,2)'",
        "[intro];",
        
        # Overlay the intro on the main video for first 2 seconds
        "[main][intro]overlay=enable='between(t,0,2)'"
    ]
    
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-filter_complex', ''.join(filter_complex),
        '-c:v', 'libx264',
        '-preset', 'fast', 
        '-crf', '23',
        '-c:a', 'copy',
        '-y',
        output_file
    ]
    
    print(f"Processing {player_name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Successfully created: {output_file}")
    else:
        print(f"✗ Error: {result.stderr}")
        # Try simpler approach
        print("\nTrying simpler approach...")
        simple_intro(input_file, output_file, player_name, rank)

def simple_intro(input_file, output_file, player_name, rank):
    """Simpler approach with basic text overlay"""
    
    player_name_clean = player_name.replace("'", "")
    
    # Very simple command
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', (
            f"drawtext=text='TOP 100 FANTASY WRs 2024':fontsize=50:fontcolor=white:box=1:boxcolor=black@0.8:boxborderw=10:x=(w-text_w)/2:y=100:enable='between(t,0,2)',"
            f"drawtext=text='{player_name_clean}':fontsize=70:fontcolor=yellow:box=1:boxcolor=black@0.8:boxborderw=10:x=(w-text_w)/2:y=h/2-50:enable='between(t,0,2)',"
            f"drawtext=text='NUMBER {rank}':fontsize=60:fontcolor=white:box=1:boxcolor=black@0.8:boxborderw=10:x=(w-text_w)/2:y=h/2+50:enable='between(t,0,2)'"
        ),
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23', 
        '-c:a', 'copy',
        '-y',
        output_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Simple approach worked: {output_file}")
    else:
        print(f"✗ Simple approach also failed: {result.stderr}")

# Test with one video
print("Testing intro creation...\n")

video = {
    'input': 'video_clips/JaMarr_Chase_highlights.mp4.webm',
    'output': 'video_clips/JaMarr_Chase_intro_test.mp4',
    'name': "Ja'Marr Chase",
    'rank': 1
}

if os.path.exists(video['input']):
    create_intro_with_text(video['input'], video['output'], video['name'], video['rank'])
else:
    print(f"Input file not found: {video['input']}")