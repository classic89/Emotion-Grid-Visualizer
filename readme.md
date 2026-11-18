# Russell's Circumplex Model of Affect

This project is a Streamlit app that visualizes Russell's Circumplex Model of Affect as a 10×10 grid of emotions. Each grid cell pairs an emotion label with a bundled facial-expression image.

- **Horizontal axis — Valence:** unpleasant on the left, pleasant on the right.
- **Vertical axis — Arousal:** high activation at the top, low activation at the bottom.
- Divider lines mark the four broad domains: high/low arousal crossed with pleasant/unpleasant valence.

Hover over a cell in the app to enlarge it. Use **Download Grid as Image** to save a PNG of the grid. The expandable “About” section in the app describes the model and cites Russell's 1980 paper.

## Requirements

- Python 3.11 or newer
- Git, if you plan to clone the project
- The included `assets/emotions/` directory. It contains the 100 PNG images used in the grid.

## Set up on another computer

### 1. Get the project files

Clone the repository and enter its directory:

```bash
git clone <repository-url>
cd <repository-directory>
```

Or download and extract the project files. Keep `assets/emotions/` alongside `app.py`; the app expects the images at those paths.

### 2. Install dependencies

This project includes `pyproject.toml` and `uv.lock` to install the pinned dependencies with [uv](https://docs.astral.sh/uv/):

```bash
python -m pip install uv
uv sync --locked --no-install-project
```

Alternatively, use Python's built-in virtual environment and install the dependencies directly:

```bash
python -m venv .venv
```

Activate it, then install Streamlit and Pillow:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell (use this instead of the line above)
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install "streamlit>=1.54.0" "pillow>=12.1.1"
```

### 3. Start the app

From the project directory, run:

```bash
streamlit run app.py --server.port 5000
```

Streamlit prints a local URL in the terminal (usually `http://localhost:5000`). Open it in a browser. Stop the app with `Ctrl+C`.

If you used `uv sync`, activate the environment first:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

## Project files

- `app.py` — Streamlit interface, emotion grid, and PNG download generation.
- `assets/emotions/` — the 100 facial-expression PNGs displayed in the grid.
- `pyproject.toml` and `uv.lock` — Python dependency declarations and locked versions.
- `.streamlit/config.toml` — Streamlit server settings.

## Reference

Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, 39(6), 1161–1178.
