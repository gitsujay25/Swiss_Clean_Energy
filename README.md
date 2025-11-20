# 🇨🇭 Renewable Energy Visualization Dashboard  
*A Streamlit-based analytical tool for exploring Switzerland’s renewable energy landscape*

## 📌 Overview  
This project provides an interactive dashboard to explore, analyze, and visualize renewable energy sources across Switzerland.  
Using **Streamlit**, **Plotly**, **Seaborn**, and **GeoJSON** data, the app offers a clear understanding of spatial distribution, production capacity, energy mix, and temporal trends of renewable energy sources.

The dashboard is organized into several tabs, each highlighting a different aspect of the data.

---

## 🚀 Features  

### 🗺️ **1. Overview**  
- Interactive choropleth maps of Swiss cantons   
- Filters for energy category  
- Hover tooltips with information about the energy sources in the canton
- Barplot for comparative study among cantons.

### 📍 **2. Source Location**  
- Visual exploration of installation locations
- Scatter overlays showing individual renewable energy installations 
- Ability to filter by canton and energy type  
- Hover popups showing municipality, type and address
- Pie charts illustrating energy-type contribution  

### 📊 **3. Summary & Statistics**  
Includes multiple statistical views:
- Violin plots (with option to remove outliers)  
- Production-to-capacity efficiency analysis  
- Median-based efficiency threshold lines   
- Time-series charts showing growth of renewable installations, production, and capacity  

---

## 📁 Project Structure  
```text
project/
│
├── app.py                # Main Streamlit application
├── utils.py              # Helper functions (loading cleaning)
├── plotting.py           # Helper functions for plotting
├── requirement.txt       # File containing the required packages
│
├── data/
│   ├── swiss_clean_energy.csv
│   ├── georef-switzerland-kanton.geojson
│
├── images/               # Saved figures, icons, screenshots
│   └── example.png
│
└── README.md             # Documentation
```

## 🛠️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/gitsujay25/Swiss_Clean_Energy.git
cd Swiss_Clean_Energy
conda create -n energy_vis python=3.10
conda activate energy_vis
pip install -r requirements.txt
```

### ▶️ Run the Application

```bash
streamlit run app.py
````
The dashboard will open automatically in your browser at: http://localhost:8501/

## 📦 Data

The project uses:

- Swiss geo-boundaries (canton-level GeoJSON)  
- Clean energy installation dataset with attributes such as (Data Source: https://data.open-power-system-data.org/renewable_power_plants/2020-08-25):
  - **production** (MWh)  
  - **electrical_capacity** (MW)  
  - Geographic coordinates (`lat`, `lon`)  
  - **energy_source_level_2** (e.g., Solar, Hydro, Bioenergy, Wind)  
  - `technology`, `company`, `canton_name`, `municipality` etc.

---

## 📈 Key Visual Components

The application includes the following interactive visualizations:

- **Choropleth maps** — canton-level shading showing counts, production, or capacity  
- **Scatter maps** — point locations of installations with detailed hover info  
- **Bar charts** — sorted and annotated bars for cantons and energy types  
- **Donut / Pie charts** — energy-type distributions with central numeric labels  
- **Violin + KDE plots** — distribution of production/capacity with optional outlier removal  
- **Scatter plots** - for analysis of production efficiency 
- **Time-series line plots** — cumulative growth of sources, production, and capacity  
- **Combined subplot layouts** — side-by-side visuals for comparison

---

## ✨ Customization Options

You can customize many aspects of the dashboard:

- **Color schemes:** modify Plotly's `color_discrete_map` or `color_discrete_sequence`  
- **Hover info:** update `hovertemplate` or `hover_data`  
- **Layout:** control fonts, margins, grids with `fig.update_layout()`    
- **Widgets:** add sliders / dropdowns / radio buttons to control filtering  
- **Exports:** enable CSV or image download buttons in Streamlit

---

## 🧰 Development Tips

- Keep reusable functions in `utils.py`  
- Use `@st.cache_data` for expensive operations   
- Pin versions in `requirements.txt` for reproducibility  

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repository, open issues, or submit pull requests.

## 📬 Contact
For questions or suggestions:
- Author: Sujay Ray
- GitHub: https://github.com/gitsujay25
- Linkdin: https://www.linkedin.com/in/sujayray92/