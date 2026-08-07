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
    / "profile_coordinates_topo"
    / "ALL_PROFILES_master.csv"
)

docs_dir = repo_root / "docs"
docs_dir.mkdir(parents=True, exist_ok=True)
output_html = docs_dir / "index.html"

# -------------------------------------------------------------
# 2. Load Master CSV Data
# -------------------------------------------------------------
df = pd.read_csv(csv_path)
df = df.dropna(subset=["Latitude", "Longitude"]).copy()

center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()

print(f"Loaded {len(df)} coordinate points.")
print(f"Map Center: Lat {center_lat:.4f}, Lon {center_lon:.4f}")

# -------------------------------------------------------------
# 3. Initialize Folium Map
# -------------------------------------------------------------
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles=None)

# Add Basemaps (Esri Satellite & OpenStreetMap)
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

# -------------------------------------------------------------
# 4. Add Sensor Layers (Independent Stacking)
# -------------------------------------------------------------
# Both layers default to active so co-located points render both markers
electrodes_group = folium.FeatureGroup(name="Electrodes", show=True).add_to(m)
geophones_group = folium.FeatureGroup(name="Geophones", show=True).add_to(m)

for _, row in df.iterrows():
    lat = row["Latitude"]
    lon = row["Longitude"]
    profile_name = row.get("profile name", "Unknown Profile")
    elec_id = row.get("electrodes", "")
    geo_id = row.get("geophones", "")
    sensor_type = row.get("sensor_type", "")

    has_electrode = pd.notna(elec_id) or sensor_type == "Electrode"
    has_geophone = pd.notna(geo_id) or sensor_type == "Geophone"

    # Base popup information
    popup_info = f"<b>Profile:</b> {profile_name}<br>"
    if pd.notna(elec_id):
        popup_info += f"<b>Electrode ID:</b> {int(elec_id)}<br>"
    if pd.notna(geo_id):
        popup_info += f"<b>Geophone ID:</b> {int(geo_id)}<br>"
    if "Ellipsoidalheight" in row and pd.notna(row["Ellipsoidalheight"]):
        popup_info += f"<b>Elevation:</b> {row['Ellipsoidalheight']:.1f} m<br>"

    # 1. Add Geophone Marker (Blue, radius=5)
    if has_geophone:
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color="#1f77b4",  # Dark Blue border
            fill=True,
            fill_color="#1f77b4",  # Blue fill
            fill_opacity=0.6,
            popup=folium.Popup(
                f"{popup_info}<b>Sensor:</b> Geophone", max_width=250
            ),
            tooltip=f"{profile_name} - Geophone "
            + (f"#{int(geo_id)}" if pd.notna(geo_id) else ""),
        ).add_to(geophones_group)

    # 2. Add Electrode Marker (Red, radius=3 sits inside blue geophone ring when co-located)
    if has_electrode:
        folium.CircleMarker(
            location=[lat, lon],
            radius=3,
            color="#d62728",  # Red border
            fill=True,
            fill_color="#d62728",  # Red fill
            fill_opacity=0.9,
            popup=folium.Popup(
                f"{popup_info}<b>Sensor:</b> Electrode", max_width=250
            ),
            tooltip=f"{profile_name} - Electrode "
            + (f"#{int(elec_id)}" if pd.notna(elec_id) else ""),
        ).add_to(electrodes_group)

# -------------------------------------------------------------
# 5. Add Map Controls & Save Output
# -------------------------------------------------------------
folium.LayerControl(collapsed=False).add_to(m)
Fullscreen(position="topleft").add_to(m)
MeasureControl(position="topright", primary_length_unit="meters").add_to(m)

m.save(str(output_html))
print(f"✓ Interactive map successfully generated -> {output_html}")