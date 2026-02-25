import streamlit as st
from pathlib import Path
import base64
import json

st.set_page_config(
    page_title="Russell's Circumplex Model of Affect",
    page_icon="🧠",
    layout="wide",
)

EMOTIONS = [
    ["Enraged", "Furious", "Panicked", "Alarmed", "Tense", "Alert", "Excited", "Thrilled", "Ecstatic", "Euphoric"],
    ["Hostile", "Angry", "Frightened", "Anxious", "Nervous", "Energized", "Enthusiastic", "Elated", "Joyful", "Overjoyed"],
    ["Hateful", "Aggressive", "Distressed", "Worried", "Uneasy", "Stimulated", "Amused", "Cheerful", "Delighted", "Blissful"],
    ["Disgusted", "Annoyed", "Frustrated", "Irritated", "Restless", "Interested", "Pleased", "Happy", "Glad", "Exhilarated"],
    ["Miserable", "Displeased", "Unhappy", "Dissatisfied", "Indifferent", "Neutral", "Satisfied", "Content", "Hopeful", "Proud"],
    ["Gloomy", "Melancholic", "Glum", "Pensive", "Apathetic", "Mellow", "At Ease", "Comfortable", "Warm", "Fulfilled"],
    ["Despondent", "Sorrowful", "Sad", "Down", "Bored", "Calm", "Relaxed", "Serene", "Peaceful", "Grateful"],
    ["Depressed", "Hopeless", "Dejected", "Drained", "Lethargic", "Tranquil", "Restful", "Soothed", "Placid", "Contented"],
    ["Despairing", "Anguished", "Weary", "Fatigued", "Sluggish", "Still", "Drowsy", "Cozy", "Laid-back", "Carefree"],
    ["Devastated", "Grief-stricken", "Exhausted", "Tired", "Sleepy", "Passive", "Idle", "Dreamy", "Zen", "Asleep"],
]

AROUSAL_LABELS = [
    "Very High", "High", "Moderate-High", "Moderate+",
    "Moderate", "Moderate-", "Moderate-Low", "Low", "Very Low", "Lowest"
]

VALENCE_LABELS = [
    "Very\nUnpleasant", "Unpleasant", "Moderately\nUnpleasant", "Slightly\nUnpleasant",
    "Mildly\nUnpleasant", "Mildly\nPleasant", "Slightly\nPleasant", "Moderately\nPleasant",
    "Pleasant", "Very\nPleasant"
]


def get_cell_color(row, col):
    valence = col / 9.0
    arousal = 1.0 - row / 9.0

    r = int(255 * (1 - valence) * 0.6 + 80)
    g = int(255 * valence * 0.5 + 80)
    b = int(255 * arousal * 0.3 + 80)

    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))

    return f"#{r:02x}{g:02x}{b:02x}"


def get_image_path(row, col):
    emotion = EMOTIONS[row][col].lower().replace(" ", "_")
    return Path(f"assets/emotions/r{row}_c{col}_{emotion}.png")


def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def build_grid_html():
    cell_size = 120
    label_width = 80
    header_height = 60
    grid_width = cell_size * 10 + label_width + 20
    grid_height = cell_size * 10 + header_height + 80

    html = f"""
    <style>
        .circumplex-container {{
            position: relative;
            width: {grid_width}px;
            margin: 0 auto;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .grid-wrapper {{
            position: relative;
            margin-left: {label_width}px;
            margin-top: {header_height}px;
        }}
        .emotion-grid {{
            display: grid;
            grid-template-columns: repeat(10, {cell_size}px);
            grid-template-rows: repeat(10, {cell_size}px);
            gap: 2px;
            border: 2px solid #333;
            background: #333;
        }}
        .emotion-cell {{
            position: relative;
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.2s, z-index 0.2s, box-shadow 0.2s;
        }}
        .emotion-cell:hover {{
            transform: scale(1.8);
            z-index: 100;
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
            border-radius: 4px;
        }}
        .emotion-cell img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}
        .emotion-label {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.85));
            color: white;
            text-align: center;
            font-size: 9px;
            font-weight: 600;
            padding: 12px 2px 3px;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}
        .emotion-cell:hover .emotion-label {{
            font-size: 11px;
            padding: 16px 4px 6px;
        }}
        .arousal-label {{
            position: absolute;
            left: 0;
            width: {label_width - 10}px;
            text-align: right;
            font-size: 10px;
            font-weight: 500;
            color: #555;
            line-height: 1.2;
        }}
        .valence-label {{
            position: absolute;
            text-align: center;
            font-size: 10px;
            font-weight: 500;
            color: #555;
            width: {cell_size}px;
            line-height: 1.2;
        }}
        .axis-title {{
            font-size: 14px;
            font-weight: 700;
            color: #333;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .axis-arrow {{
            position: absolute;
            color: #666;
            font-size: 13px;
            font-weight: 600;
        }}
    </style>
    <div class="circumplex-container">
        <div class="axis-title" style="position:absolute; left:{label_width + cell_size*5 - 60}px; top:0; text-align:center;">
            Valence →
        </div>
        <div class="axis-title" style="position:absolute; left:0; top:{header_height + cell_size*5 - 10}px; transform:rotate(-90deg); transform-origin:center;">
            ← Arousal
        </div>
    """

    for col in range(10):
        x = label_width + col * (cell_size + 2)
        label = VALENCE_LABELS[col].replace("\n", "<br>")
        html += f'<div class="valence-label" style="left:{x}px; top:{header_height - 30}px;">{label}</div>'

    html += '<div class="grid-wrapper">'

    for row in range(10):
        y = row * (cell_size + 2)
        html += f'<div class="arousal-label" style="top:{y + cell_size//2 - 10}px; left:-{label_width}px;">{AROUSAL_LABELS[row]}</div>'

    html += '<div class="emotion-grid">'

    for row in range(10):
        for col in range(10):
            emotion = EMOTIONS[row][col]
            img_path = get_image_path(row, col)
            color = get_cell_color(row, col)

            if img_path.exists():
                b64 = image_to_base64(img_path)
                img_html = f'<img src="data:image/png;base64,{b64}" alt="{emotion}">'
            else:
                img_html = f'<div style="width:100%;height:100%;background:{color};display:flex;align-items:center;justify-content:center;font-size:24px;">😶</div>'

            html += f"""
            <div class="emotion-cell" title="{emotion} (Arousal: {AROUSAL_LABELS[row]}, Valence: {VALENCE_LABELS[col].replace(chr(10), ' ')})">
                {img_html}
                <div class="emotion-label">{emotion}</div>
            </div>
            """

    html += '</div></div></div>'
    return html


st.markdown("""
<h1 style="text-align:center; margin-bottom:0;">Russell's Circumplex Model of Affect</h1>
<p style="text-align:center; color:#666; margin-top:4px; margin-bottom:20px;">
    A 10×10 emotion grid mapping facial expressions across <b>Valence</b> (pleasant–unpleasant) and <b>Arousal</b> (activated–deactivated)
</p>
""", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 10, 1])

with col_center:
    grid_html = build_grid_html()
    st.components.v1.html(grid_html, height=1420, scrolling=True)

st.markdown("---")

with st.expander("About Russell's Circumplex Model"):
    st.markdown("""
**Russell's Circumplex Model of Affect** (1980) is a foundational framework in affective psychology
that organizes emotions along two primary dimensions:

- **Valence** (horizontal axis): Ranges from highly unpleasant (left) to highly pleasant (right).
  This dimension captures the intrinsic attractiveness or averseness of an emotion.

- **Arousal** (vertical axis): Ranges from low activation/deactivated (bottom) to high activation/activated (top).
  This dimension captures the level of physiological activation associated with an emotion.

Every emotional state can be mapped to a point in this two-dimensional space. For example:
- **Excited** = high arousal + positive valence (top-right)
- **Calm** = low arousal + positive valence (bottom-right)
- **Angry** = high arousal + negative valence (top-left)
- **Sad** = low arousal + negative valence (bottom-left)

This 10×10 grid provides a granular view with 100 distinct emotional states, each illustrated
with a representative facial expression photograph.

**Reference:** Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, 39(6), 1161–1178.
""")
