import streamlit as st
from pathlib import Path
import base64
import json
import io
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(
    page_title="Russell's Circumplex Model of Affect",
    page_icon="🧠",
    layout="wide",
)

EMOTIONS = [
    ["Enraged", "Furious", "Panicked", "Alarmed", "Tense", "Surprised", "Excited", "Thrilled", "Ecstatic", "Euphoric"],
    ["Hostile", "Angry", "Frightened", "Anxious", "Nervous", "Energized", "Enthusiastic", "Elated", "Joyful", "Overjoyed"],
    ["Hateful", "Aggressive", "Distressed", "Worried", "Uneasy", "Stimulated", "Amused", "Cheerful", "Delighted", "Blissful"],
    ["Disgusted", "Annoyed", "Frustrated", "Irritated", "Restless", "Interested", "Pleased", "Happy", "Glad", "Exhilarated"],
    ["Miserable", "Displeased", "Unhappy", "Dissatisfied", "Indifferent", "Neutral", "Satisfied", "Content", "Hopeful", "Proud"],
    ["Gloomy", "Melancholic", "Glum", "Pensive", "Apathetic", "Mellow", "At Ease", "Comfortable", "Warm", "Fulfilled"],
    ["Despondent", "Sorrowful", "Sad", "Down", "Bored", "Calm", "Relaxed", "Serene", "Peaceful", "Grateful"],
    ["Depressed", "Hopeless", "Dejected", "Drained", "Lethargic", "Tranquil", "Restful", "Soothed", "Placid", "Contented"],
    ["Despairing", "Anguished", "Weary", "Fatigued", "Sluggish", "Still", "Drowsy", "Cozy", "Laid-back", "Carefree"],
    ["Devastated", "Grief-stricken", "Exhausted", "Tired", "Sleepy", "Passive", "Idle", "Dreamy", "Zen", "Serene"],
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
        .axis-line-h {{
            position: absolute;
            left: 0;
            right: 0;
            height: 3px;
            background: rgba(255, 255, 255, 0.85);
            box-shadow: 0 0 6px rgba(0,0,0,0.5);
            z-index: 50;
            pointer-events: none;
        }}
        .axis-line-v {{
            position: absolute;
            top: 0;
            bottom: 0;
            width: 3px;
            background: rgba(255, 255, 255, 0.85);
            box-shadow: 0 0 6px rgba(0,0,0,0.5);
            z-index: 50;
            pointer-events: none;
        }}
        .quadrant-label {{
            position: absolute;
            z-index: 51;
            font-size: 13px;
            font-weight: 700;
            color: #fff;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            text-shadow: 0 1px 4px rgba(0,0,0,0.7), 0 0 10px rgba(0,0,0,0.5);
            pointer-events: none;
            text-align: center;
            line-height: 1.3;
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

    mid_pos = 5 * (cell_size + 2)

    html += f'<div class="axis-line-h" style="top:{mid_pos - 1}px;"></div>'
    html += f'<div class="axis-line-v" style="left:{mid_pos - 1}px;"></div>'

    q_pad_x = cell_size * 1.2
    q_pad_y = cell_size * 1.0


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


@st.cache_data
def generate_grid_image():
    cell_px = 150
    gap = 3
    margin_left = 120
    margin_top = 80
    margin_bottom = 50
    margin_right = 20
    grid_w = 10 * cell_px + 9 * gap
    grid_h = 10 * cell_px + 9 * gap
    img_w = margin_left + grid_w + margin_right
    img_h = margin_top + grid_h + margin_bottom

    canvas = Image.new("RGB", (img_w, img_h), "#ffffff")
    draw = ImageDraw.Draw(canvas)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        axis_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        quad_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
    except OSError:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        axis_font = ImageFont.load_default()
        quad_font = ImageFont.load_default()

    title = "Russell's Circumplex Model of Affect"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((img_w - tw) // 2, 10), title, fill="#222222", font=title_font)

    draw.text((margin_left + grid_w // 2 - 30, margin_top - 22), "Valence →", fill="#444", font=axis_font)

    arousal_text = "← Arousal"
    temp_img = Image.new("RGBA", (200, 30), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), arousal_text, fill="#444", font=axis_font)
    rotated = temp_img.rotate(90, expand=True)
    canvas.paste(rotated, (5, margin_top + grid_h // 2 - 50), rotated)

    draw.rectangle(
        [margin_left - 1, margin_top - 1, margin_left + grid_w + 1, margin_top + grid_h + 1],
        outline="#333333", width=2
    )

    for row in range(10):
        for col in range(10):
            x = margin_left + col * (cell_px + gap)
            y = margin_top + row * (cell_px + gap)

            emotion = EMOTIONS[row][col]
            img_path = get_image_path(row, col)

            if img_path.exists():
                face = Image.open(img_path).resize((cell_px, cell_px), Image.LANCZOS)
                canvas.paste(face, (x, y))
            else:
                color = get_cell_color(row, col)
                draw.rectangle([x, y, x + cell_px, y + cell_px], fill=color)

            label_y = y + cell_px - 20
            draw.rectangle([x, label_y, x + cell_px, y + cell_px], fill=(0, 0, 0, 180))
            overlay = Image.new("RGBA", (cell_px, 20), (0, 0, 0, 180))
            canvas.paste(Image.alpha_composite(
                Image.new("RGBA", (cell_px, 20), (0, 0, 0, 0)), overlay
            ), (x, label_y))
            lbbox = draw.textbbox((0, 0), emotion, font=label_font)
            lw = lbbox[2] - lbbox[0]
            draw.text((x + (cell_px - lw) // 2, label_y + 3), emotion, fill="white", font=label_font)

    for row in range(10):
        y = margin_top + row * (cell_px + gap) + cell_px // 2 - 6
        draw.text((25, y), AROUSAL_LABELS[row], fill="#555", font=label_font)

    for col in range(10):
        x = margin_left + col * (cell_px + gap)
        vlabel = VALENCE_LABELS[col].replace("\n", " ")
        vbbox = draw.textbbox((0, 0), vlabel, font=label_font)
        vw = vbbox[2] - vbbox[0]
        draw.text((x + (cell_px - vw) // 2, margin_top - 16), vlabel, fill="#555", font=label_font)

    mid_x = margin_left + 5 * (cell_px + gap) - gap // 2
    mid_y = margin_top + 5 * (cell_px + gap) - gap // 2
    draw.line([(margin_left, mid_y), (margin_left + grid_w, mid_y)], fill="#ffffff", width=3)
    draw.line([(mid_x, margin_top), (mid_x, margin_top + grid_h)], fill="#ffffff", width=3)

    quad_labels = [
        ("High Arousal / Unpleasant", margin_left + cell_px, margin_top + cell_px),
        ("High Arousal / Pleasant", margin_left + grid_w - cell_px * 3, margin_top + cell_px),
        ("Low Arousal / Unpleasant", margin_left + cell_px, margin_top + grid_h - cell_px * 2),
        ("Low Arousal / Pleasant", margin_left + grid_w - cell_px * 3, margin_top + grid_h - cell_px * 2),
    ]
    for text, qx, qy in quad_labels:
        draw.text((qx, qy), text, fill="white", font=quad_font,
                  stroke_width=2, stroke_fill="black")

    buf = io.BytesIO()
    canvas.save(buf, format="PNG", quality=95)
    buf.seek(0)
    return buf.getvalue()


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

dl_col1, dl_col2, dl_col3 = st.columns([4, 2, 4])
with dl_col2:
    png_data = generate_grid_image()
    st.download_button(
        label="Download Grid as Image",
        data=png_data,
        file_name="russells_circumplex_model.png",
        mime="image/png",
        use_container_width=True,
    )

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
