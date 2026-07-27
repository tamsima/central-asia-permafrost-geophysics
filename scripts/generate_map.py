# %% Generate Interactive Folium Map 
import os
from pathlib import Path
import urllib.request
import folium
from folium.plugins import Fullscreen, MeasureControl
import pandas as pd

# Locate Repository Root & Define Paths

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

# Load Master CSV Data

df = pd.read_csv(csv_path)
df = df.dropna(subset=["Latitude", "Longitude"]).copy()

center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()

print(f"Loaded {len(df)} coordinate points.")
print(f"Map Center: Lat {center_lat:.4f}, Lon {center_lon:.4f}")

# Initialize Folium Map
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles=None)

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

# Add Country Boundaries for Kyrgyzstan & Tajikistan

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

# Add Points (Electrodes & Geophones)
# -------------------------------------------------------------
# 5. Add Points (Electrodes vs Geophones with Co-location Priority)
# -------------------------------------------------------------
electrodes_group = folium.FeatureGroup(name="Electrodes", show=True).add_to(m)
geophones_group = folium.FeatureGroup(
    name="Geophones (Standalone)", show=True
).add_to(m)

for _, row in df.iterrows():
    lat = row["Latitude"]
    lon = row["Longitude"]
    profile_name = row.get("profile name", "Unknown Profile")
    elec_id = row.get("electrodes", "")
    geo_id = row.get("geophones", "")
    sensor_type = row.get("sensor_type", "")

    # Check presence of both IDs
    has_electrode = pd.notna(elec_id)
    has_geophone = pd.notna(geo_id)

    # Determine display type
    if has_electrode and has_geophone:
        type_str = "Electrode & Geophone (Co-located)"
    elif has_electrode:
        type_str = "Electrode"
    elif has_geophone:
        type_str = "Geophone"
    else:
        type_str = sensor_type

    # Build popup text
    popup_text = f"""
    <b>Profile:</b> {profile_name}<br>
    <b>Type:</b> {type_str}<br>
    """
    if has_electrode:
        popup_text += f"<b>Electrode ID:</b> {int(elec_id)}<br>"
    if has_geophone:
        popup_text += f"<b>Geophone ID:</b> {int(geo_id)}<br>"
    if "Ellipsoidalheight" in row and pd.notna(row["Ellipsoidalheight"]):
        popup_text += f"<b>Elevation:</b> {row['Ellipsoidalheight']:.1f} m<br>"

    # --- Plotting Logic ---
    # Priority: If an electrode exists (standalone OR co-located with a geophone),
    # plot it as an Electrode (Red)
    if has_electrode or sensor_type == "Electrode":
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color="#d62728",  # Red
            fill=True,
            fill_color="#d62728",
            fill_opacity=0.85,
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"{profile_name} - {type_str}",
        ).add_to(electrodes_group)

    # Only plot as standalone Geophone (Blue) if NO electrode is present at this location
    else:
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color="#1f77b4",  # Blue
            fill=True,
            fill_color="#1f77b4",
            fill_opacity=0.85,
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"{profile_name} - Geophone",
        ).add_to(geophones_group)

# -------------------------------------------------------------
# 6. Add Map Controls & Save Output
# -------------------------------------------------------------
folium.LayerControl(collapsed=False).add_to(m)
Fullscreen(position="topleft").add_to(m)
MeasureControl(position="topright", primary_length_unit="meters").add_to(m)

m.save(str(output_html))
print(f"✓ Interactive map successfully generated -> {output_html}")