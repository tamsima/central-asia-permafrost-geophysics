# Geophysical Data Repository for Central Asian Mountain Permafrost

This repository hosts open-access Electrical Resistivity Tomography (ERT) and Refraction Seismic Tomography (RST) datasets collected between 2021 and 2025 across key mountain permafrost sites in the Tien Shan and Pamir ranges of Kyrgyzstan and Tajikistan. The profiles support quantitative characterization of subsurface ice heterogeneity in data-scarce high-altitude environments of different landforms.

This dataset is licensed under a [Creative Commons Attribution 4.0 International License (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/).

---

## 📁 Data Structure & Formats

`data/geophysics/raw/001_ERT` contains ERT data in different formats:

* **`002_dat/`**: Contains raw `.dat` binary/text files exported directly from **Iris Instruments ProSys II** (collected using a Syscal Pro resistivity meter).
* **`003_udf/`**: Contains unified data format (`*_rhoa.txt`) files required for inversion with `pyGIMLi`. Specifications for this format can be found at [resistivity.net/bert/data_format.html](http://resistivity.net/bert/data_format.html).

---

## 🚀 Usage

An example demonstrating how to load and invert the ERT data in `003_udf` using `pyGIMLi` is provided in:

`scripts/notebooks/plot_ERT_inversion.ipynb`




