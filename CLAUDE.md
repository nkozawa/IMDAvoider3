# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a frequency segment optimization tool for drone avoidance systems (IMD - Intermodulation Distortion Avoider). The project finds optimal frequency combinations within specified ranges while avoiding interference patterns.

## Key Architecture

### Core Components

1. **imd.py** - Rating calculation module
   - Calculates intermodulation distortion ratings for frequency combinations
   - Uses a third-order intermodulation formula (2*f1 - f2)
   - Valid frequency range: 5100-6099 MHz
   - Rating system: 0-100 (higher is better)

2. **app.py** - Main application
   - Finds non-overlapping frequency segments within defined ranges
   - Current ranges: (5690-5724), (5730-5754), (5770-5809) MHz
   - Segment width: 17 MHz with 1 MHz minimum gap
   - Visualizes top-rated combinations using matplotlib

### Algorithm Flow
1. Generate all possible center frequencies within ranges
2. Find all valid non-overlapping combinations of 4 segments
3. Calculate IMD ratings for each combination
4. Sort by rating and display top 10 results with visualization

## Development Commands

### Setup with uv
```bash
# Install dependencies
uv sync

# Run the application
uv run python app.py
```

### Alternative: Manual Setup
If not using uv, install matplotlib directly:
```bash
pip install matplotlib
python3 app.py
```

## Project-Specific Notes

- Frequency values are in MHz
- Segments are defined by their center frequency
- The rating algorithm penalizes combinations where intermodulation products fall near existing frequencies
- Lower total interference score results in higher rating (100 - normalized_score)