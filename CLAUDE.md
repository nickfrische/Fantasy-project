# Fantasy Football WR Instagram Video Generator

## Production Status ✅ FULLY OPERATIONAL

**Complete automated system for generating Instagram-ready WR videos with stacked blur effects and text overlays.**

---

## Quick Start (Copy & Paste)

```bash
cd "/Users/nickfrische/Desktop/Fantasy project"
source venv/bin/activate
python3 create_stacked_blur_final.py
```

**That's it!** The script will automatically process the next unposted WR from the top 75 rankings.

---

## What The System Does

### 🎬 Complete Video Creation Pipeline

1. **Finds Next Player**: Automatically selects the highest-ranked unposted WR from the top 75
2. **Creates Geometric Intro**: 2-second minimal design with player stats and ranking
3. **Downloads YouTube Highlights**: 90 seconds of actual game footage
4. **Creates Stacked Blur Effect**: Professional video effect with text overlays
5. **Combines Everything**: Intro + stacked blur highlights into final Instagram video
6. **Updates Tracking**: Marks player as posted in CSV to prevent duplicates
7. **Cleans Up**: Removes intermediate files, keeps only final output

### 📊 Text Overlays Include
- **WR Rank** (e.g., "WR #65")
- **Player Name** (e.g., "AMARI COOPER")
- **Team** (e.g., "2TM")
- **Fantasy Points** (e.g., "79 FANTASY POINTS")

### 🎥 Final Output
- **Duration**: ~92 seconds (2s intro + 90s highlights)
- **Format**: 1080x1920 Instagram/TikTok ready
- **Quality**: Professional with audio
- **Location**: `output/[RANK]_[PLAYER_NAME]_FINAL_STACKED_WITH_INTRO.mp4`

---

## File Structure

```
Fantasy project/
├── create_stacked_blur_final.py      # Main script - RUN THIS
├── create_wr_instagram_video.py      # Helper functions
├── wr_top100_with_links.csv          # Player data & YouTube links
├── venv/                             # Python virtual environment
├── output/                           # Generated videos appear here
└── CLAUDE.md                         # This documentation
```

---

## How It Handles Errors (Seamlessly)

### Common Issue: YouTube Download Failures
**What happens**: The `--download-sections` parameter sometimes fails with streaming format errors.

**How it's handled**: The script automatically:
1. Downloads the full YouTube video
2. Trims it to exactly 90 seconds using FFmpeg
3. Continues with the workflow

**No manual intervention needed** - it's all automated in the error handling.

---

## Step-by-Step Process Breakdown

### 1. Virtual Environment Activation
```bash
cd "/Users/nickfrische/Desktop/Fantasy project"
source venv/bin/activate
```
**Why**: Ensures all Python dependencies (yt-dlp, etc.) are available.

### 2. Player Selection
- Script reads `wr_top100_with_links.csv`
- Finds highest-ranked player where `Posted=False` in top 75
- Example: "Processing #65 Amari Cooper (2TM) - 79 points"

### 3. Intro Creation (2 seconds)
- White background with black geometric elements
- Circle outline around rank number
- Player name in HelveticaNeue font
- Team and fantasy points in minimal frames
- Saves as: `output/[RANK]_[PLAYER]_intro.mp4`

### 4. YouTube Download & Trim (90 seconds)
**Primary method** (with fallback):
```bash
yt-dlp --download-sections '*0-90' [YouTube_URL]
```

**Fallback method** (when primary fails):
```bash
# Download full video
yt-dlp [YouTube_URL]
# Trim to 90 seconds  
ffmpeg -i full_video.mp4 -t 90 trimmed_video.mp4
```

### 5. Stacked Blur Creation
- **Top/Bottom**: Blurred sections (640px each, 30 sigma blur)
- **Middle**: Original video zoomed 130% (640px height)
- **Text Overlays**: White text with black stroke
  - WR rank at y=280
  - Player name at y=1420  
  - Team at y=1500
  - Fantasy points at y=1580

### 6. Video Concatenation
- Combines intro + stacked blur using FFmpeg filter graph
- Maintains audio sync throughout
- Outputs final video: `[RANK]_[PLAYER]_FINAL_STACKED_WITH_INTRO.mp4`

### 7. Database Update & Cleanup
- Updates CSV: `Posted=False` → `Posted=True`
- Removes intermediate files (intro, raw download, blur-only)
- Keeps only final output video

---

## Troubleshooting

### "No unposted players found in top 75"
**Cause**: All top 75 WRs have been processed.
**Solution**: Check CSV for any players you want to re-process by changing `True` back to `False`.

### "Error opening input file"
**Cause**: Intermediate file missing (usually intro).
**Solution**: Run the complete script `python3 create_stacked_blur_final.py` - don't run partial workflows.

### YouTube download fails completely
**Cause**: Video URL changed or restricted.
**Solution**: Update the YouTube URL in `wr_top100_with_links.csv` for that player.

### Dependencies missing
**Cause**: Virtual environment not activated or missing packages.
**Solution**: 
```bash
source venv/bin/activate
pip install yt-dlp
# FFmpeg should already be installed system-wide
```

---

## Recent Successful Runs

✅ **Xavier Legette** (#67 WR, CAR, 76 points)
✅ **Michael Wilson** (#66 WR, ARI, 78 points)

Both completed successfully with the YouTube download fallback method.

---

## Next Steps for Scaling

### 1. Process All Remaining WRs (Currently ~65 left in top 75)
```bash
# Run multiple times until complete
while true; do
    python3 create_stacked_blur_final.py
    sleep 5  # Brief pause between videos
done
```

### 2. Multi-Position Support
- Extend to QBs using `qb_top100_with_links.csv`
- Extend to RBs using `rb_top100_with_links.csv` 
- Extend to TEs using `te_top100.csv`

### 3. Batch Processing Options
- Modify script to accept argument: `python3 create_stacked_blur_final.py --count 10`
- Process multiple players in one run

---

## Dependencies Confirmed Working

- **Python 3** with virtual environment
- **yt-dlp** for YouTube downloads (latest version)
- **FFmpeg** for video processing (v7.1.1)
- **CSV module** for data management (built-in)

---

## Key Configuration

- **YouTube Duration**: 90 seconds (optimal for Instagram)
- **Blur Intensity**: 30 sigma (Gaussian blur)
- **Zoom Factor**: 130% for middle video section
- **Text Font**: Arial Bold with stroke borders
- **Output Quality**: CRF 23-25 for balanced size/quality

---

*Last Updated: August 2025*
*Status: ✅ FULLY OPERATIONAL*
*Next Player: Automatically selected from CSV (Amari Cooper #65 expected)*

---

**💡 Pro Tip**: The system is designed to be fire-and-forget. Just run the command and let it work!