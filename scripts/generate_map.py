# %% Generate Interactive Folium Map for GitHub Pages with Country Outlines
import os
from pathlib import Path
import urllib.request
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

# Add Basemaps (Satellite & Standard OSM only)
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
# 4. Add Country Boundaries for Kyrgyzstan & Tajikistan
# -------------------------------------------------------------
country_group = folium.FeatureGroup(
    name="Country Boundaries (KG & TJ)", show=True
).add_to(m)

boundary_urls = {
    "Kyrgyzstan": "https://raw.githubusercontent.com/wmgeolab/geoBoundaries/main/releaseData/gbOpen/KGZ/ADM0/geoBoundaries-KGZ-ADM0.geojson",
    "Tajikistan": "https://raw.githubusercontent.com/wmgeolab/geoBoundaries/main/releaseData/gbOpen/TJK/ADM0/geoBoundaries-TJK-ADM0.geojson",
}

style_function = lambda feature: {
    "fillColor": "#none",
    "color": "#ffff00",  # Bright yellow outline
    "weight": 2.5,
    "dashArray": "5, 5",
    "fillOpacity": 0.0,
}

for country_name, url in boundary_urls.items():
    try:
        folium.GeoJson(
            url,
            name=country_name,
            style_function=style_function,
            tooltip=country_name,
        ).add_to(country_group)
        print(f"✓ Successfully fetched boundary for {country_name}")
    except Exception as e:
        print(f"⚠️ Could not load boundary for {country_name}: {e}")

# -------------------------------------------------------------
# 5. Add Points (Electrodes & Geophones)
# -------------------------------------------------------------
electrodes_group = folium.FeatureGroup(name="Electrodes", show=True).add_to(m)
geophones_group = folium.FeatureGroup(name="Geophones", show=True).add_to(m)

for _, row in df.iterrows():
    lat = row["Latitude"]
    lon = row["Longitude"]
    profile_name = row.get("profile name", "Unknown Profile")
    elec_id = row.get("electrodes", "")
    geo_id = row.get("geophones", "")
    sensor_type = row.get("sensor_type", "")

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
    else:
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
# 6. Add Map Controls & Save Output
# -------------------------------------------------------------
folium.LayerControl(collapsed=False).add_to(m)
Fullscreen(position="topleft").add_to(m)
MeasureControl(position="topright", primary_length_unit="meters").add_to(m)

m.save(str(output_html))
print(f"✓ Interactive map successfully generated -> {output_html}")