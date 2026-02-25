# Russell's Circumplex Model of Affect Visualizer

## Overview
A Streamlit web application that visualizes Russell's Circumplex Model of Affect as a 10×10 emotion grid using AI-generated facial expression photographs.

## Structure
- `app.py` - Main Streamlit application
- `assets/emotions/` - 100 AI-generated facial expression images (named `r{row}_c{col}_{emotion}.png`)
- `.streamlit/config.toml` - Streamlit server configuration

## Key Features
- 10×10 grid mapping 100 emotions across Valence (x-axis) and Arousal (y-axis)
- Each cell contains an AI-generated portrait photograph showing the labeled emotion
- Hover effect zooms into individual cells for detail
- Axis labels for arousal levels and valence levels
- Expandable "About" section explaining the model

## Dependencies
- Python 3.11
- streamlit
- pillow

## Running
```bash
streamlit run app.py --server.port 5000
```
