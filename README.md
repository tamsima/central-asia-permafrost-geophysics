# Geophysical Data Repository for Central Asian Mountain Permafrost

This repository hosts open-access Electrical Resistivity Tomography (ERT) and Refraction Seismic Tomography (RST) datasets collected between 2021 and 2025 across key mountain permafrost sites in the Tien Shan and Pamir ranges of Kyrgyzstan and Tajikistan. The profiles support quantitative characterization of subsurface ice heterogeneity in data-scarce high-altitude environments of different landforms.

This dataset is licensed under a [Creative Commons Attribution 4.0 International License (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/).

---

## 📁 Data Structure & Formats

### Electrical Resistivity Tomography (`data/geophysics/raw/001_ERT/`)

* **`002_dat/`**: Raw `.dat` binary/text files exported directly from **Iris Instruments ProSys II** (collected using a Syscal Pro resistivity meter).
* **`003_udf/`**: Unified Data Format (`*_rhoa.txt`) files required for inversion with `pyGIMLi`. Specifications for this format can be found at [resistivity.net/bert/data_format.html](http://resistivity.net/bert/data_format.html).

### Refraction Seismic Tomography (`data/geophysics/raw/002_RST/`)

* **`001_raw/`**: Raw seismic data recorded using a 24-geophone Geode system, including `.tom` files with first-arrival picks processed in **ReflexW**.
* **`002_udf/`**: Unified Data Format (`*_tt.txt`) traveltime files formatted for `pyGIMLi` inversion.
* **`004_topo/`**: Topography data files (`*_topo.txt`) required for elevation correction during inversion and plotting in `pyGIMLi`.

###  Petrophysical Joint Inversion (PJI) Data

`data/geophysics/processed/PJI` contains the processed input and setup files required for running Petrophysical Joint Inversion (PJI) modeling as presented in [Mathys et al. (2025)](https://tc.copernicus.org/articles/19/6591/2025/):

* **`mesh/`**: Inversion meshes used.
* **`NPZ_files/`**: Compressed NumPy array files containing extracted Apparent Resistivity and Apparent Seismic Velocity data.
* **`rst_processes/`**: RST coverage data.
* **`settings_files/`**: Parameter configuration and petrophysical input settings for the PJI framework.
* **`zoi_coordinates/`**: Zone of Interest (ZOI) coordinates for the extraction of mean ground ice contents in a defined zone of each profile.

---

## 🚀 Usage

To run the inversion workflows, ensure you have `pyGIMLi` installed. For setup instructions, refer to the [pyGIMLi Installation Guide](https://www.pygimli.org/installation.html).

Examples demonstrating the inversion workflows are provided in the following notebooks:

* **ERT Inversion:** `scripts/notebooks/plot_ERT_inversion.ipynb`  
  Loads and inverts the Electrical Resistivity Tomography data in `data/geophysics/raw/001_ERT/003_udf`.

* **RST Inversion:** `scripts/notebooks/plot_RST_inversion.ipynb`  
  Loads and inverts the Refraction Seismic Tomography traveltime data in `data/geophysics/raw/002_RST/002_udf` using topography from `004_topo`.





