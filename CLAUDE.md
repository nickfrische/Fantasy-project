# Fantasy Football WR Instagram Video Generator

## Production Status ✅ FULLY OPERATIONAL & PERFECTED

**Complete automated system for generating Instagram-ready WR videos with stacked blur effects and text overlays.**

---

## Quick Start (Copy & Paste)

```bash
cd "/Users/nickfrische/Desktop/Fantasy project"
source venv/bin/activate
python3 create_stacked_blur_final.py
```

**That's it!** The script will automatically process the next unposted WR from the top 75 rankings.

**Processing Time**: ~2-5 minutes per video depending on download speed

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

### YouTube Download with Automatic Fallback
**Primary Method**: Uses `--download-sections` to download only the first 90 seconds
**Fallback Method**: If primary fails, automatically downloads full video and trims to 90 seconds

**The script handles this automatically** - no manual intervention needed. The fallback method has been successfully used for:
- Amari Cooper (#65)
- Kayshon Boutte (#64) 
- Ray-Ray McCloud (#63)

All videos created perfectly with this automatic error handling.

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
The script **automatically handles this with built-in fallback**:

**Primary method** (attempted first):
```bash
yt-dlp --download-sections '*0-90' [YouTube_URL]
```

**Automatic fallback** (triggers on primary failure):
```bash
# Downloads full video
yt-dlp [YouTube_URL] -o temp_full.mp4
# Trims to 90 seconds  
ffmpeg -i temp_full.mp4 -t 90 -c copy final.mp4
# Removes temp file
```

**You don't need to do anything** - the script handles both methods automatically!

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

## Recent Successful Runs (All Using Perfected Process)

✅ **Ray-Ray McCloud** (#63 WR, ATL, 79 points) - August 25, 2025
✅ **Kayshon Boutte** (#64 WR, NWE, 79 points) - August 23, 2025
✅ **Amari Cooper** (#65 WR, 2TM, 79 points) - August 23, 2025
✅ **Michael Wilson** (#66 WR, ARI, 78 points)
✅ **Xavier Legette** (#67 WR, CAR, 76 points)

All completed flawlessly with automatic YouTube download fallback.

---

## Next Steps for Scaling

### 1. Process All Remaining WRs (Currently ~62 left in top 75)
```bash
# Run multiple times until complete
while true; do
    python3 create_stacked_blur_final.py
    sleep 5  # Brief pause between videos
done
```

### Quick Processing Multiple Players
Just run the command multiple times:
```bash
cd "/Users/nickfrische/Desktop/Fantasy project"
source venv/bin/activate
python3 create_stacked_blur_final.py  # Player 1
python3 create_stacked_blur_final.py  # Player 2
python3 create_stacked_blur_final.py  # Player 3
# etc...
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

*Last Updated: August 25, 2025*
*Status: ✅ FULLY OPERATIONAL & PERFECTED*
*Next Player: Automatically selected from CSV (Tre Tucker #62 expected)*
*Videos Created Today: 3 (Ray-Ray McCloud, Kayshon Boutte, Amari Cooper)*

---

**💡 Pro Tip**: The system is designed to be fire-and-forget. Just run the command and let it work!