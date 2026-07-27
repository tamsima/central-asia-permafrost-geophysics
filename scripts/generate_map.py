# %% Generate Interactive Folium Map for GitHub Pages
import os
from pathlib import Path
import folium
from folium.plugins import Fullscreen, MeasureControl
import pandas as pd

# -------------------------------------------------------------
# 1. Locate Repository Root & Define Paths
# -------------------------------------------------------------
current_path = Path.cwd().resolve()
repo_root = None

for parent in [current_path] + list(current_path.parents):
    if (
        parent / ".git"
    ).exists() or parent.name == "central-asia-permafrost-geophysics":
        repo_root = parent
        break

if repo_root is None:
    raise FileNotFoundError("Could not locate repository root directory!")

csv_path = (
    repo_root
    / "data"
    / "geophysics"
    / "raw"
    / "profile_coordinates_topo"
    / "ALL_PROFILES_master.csv"
)

# Output directory MUST be 'docs' for GitHub Pages
docs_dir = repo_root / "docs"
docs_dir.mkdir(parents=True, exist_ok=True)
output_html = docs_dir / "index.html"

# -------------------------------------------------------------
# 2. Load Master CSV Data
# -------------------------------------------------------------
df = pd.read_csv(csv_path)

# Drop any rows missing coordinates
df = df.dropna(subset=["Latitude", "Longitude"]).copy()

# Calculate map center
center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()

print(f"Loaded {len(df)} coordinate points.")
print(f"Map Center: Lat {center_lat:.4f}, Lon {center_lon:.4f}")

# -------------------------------------------------------------
# 3. Initialize Folium Map with Multiple Basemaps
# -------------------------------------------------------------
m = folium.Map(
    location=[center_lat, center_lon], zoom_start=9, tiles=None  # We add custom tiles below
)

# Add Basemaps
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri World Imagery",
    name="Esri Satellite",
    overlay=False,
    control=True,
).add_to(m)

folium.TileLayer(
    tiles="OpenStreetMap", name="OpenStreetMap", overlay=False, control=True
).add_to(m)

folium.TileLayer(
    tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    attr="OpenTopoMap",
    name="OpenTopoMap (Terrain)",
    overlay=False,
    control=True,
).add_to(m)

# -------------------------------------------------------------
# 4. Add Points (Grouped by Sensor Type & Profile Name)
# -------------------------------------------------------------
# Create Feature Groups for Layer Control
electrodes_group = folium.FeatureGroup(name="Electrodes", show=True).add_to(m)
geophones_group = folium.FeatureGroup(name="Geophones", show=True).add_to(m)

for _, row in df.iterrows():
    lat = row["Latitude"]
    lon = row["Longitude"]
    profile_name = row.get("profile name", "Unknown Profile")
    elec_id = row.get("electrodes", "")
    geo_id = row.get("geophones", "")
    sensor_type = row.get("sensor_type", "")

    # Popup text details
    popup_text = f"""
    <b>Profile:</b> {profile_name}<br>
    <b>Type:</b> {sensor_type}<br>
    """
    if pd.notna(elec_id):
        popup_text += f"<b>Electrode ID:</b> {int(elec_id)}<br>"
    if pd.notna(geo_id):
        popup_text += f"<b>Geophone ID:</b> {int(geo_id)}<br>"
    if "Ellipsoidalheight" in row and pd.notna(row["Ellipsoidalheight"]):
        popup_text += f"<b>Elevation:</b> {row['Ellipsoidalheight']:.1f} m<br>"

    # Style by Sensor Type
    if sensor_type == "Geophone" or pd.notna(geo_id):
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color="#1f77b4",  # Blue
            fill=True,
            fill_color="#1f77b4",
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"{profile_name} - Geophone",
        ).add_to(geophones_group)
    else:  # Default to Electrode
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color="#d62728",  # Red
            fill=True,
            fill_color="#d62728",
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"{profile_name} - Electrode",
        ).add_to(electrodes_group)

# -------------------------------------------------------------
# 5. Add Map Controls & Save Output
# -------------------------------------------------------------
folium.LayerControl(collapsed=False).add_to(m)
Fullscreen(position="topleft").add_to(m)
MeasureControl(position="topright", primary_length_unit="meters").add_to(m)

m.save(str(output_html))
print(f"✓ Interactive map successfully generated -> {output_html}")