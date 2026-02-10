# 🧠 Smart Inventory AI 
**AI-Powered Demand Forecasting & Inventory Optimization for Retailers**

---

## 🌟 Executive Summary  

Retailers face a persistent challenge: **balancing inventory**.  
- Overstocking ties up capital and increases storage costs.  
- Stockouts lead to lost sales, frustrated customers, and damaged reputation.  
- Manual forecasting (Excel sheets, gut-feel decisions) is error-prone and reactive.  

**Smart Inventory AI Pro** solves this problem with a **modular, explainable AI system** that delivers:  
- 📈 Accurate demand forecasts  
- 📦 Optimized reorder points and safety stock  
- 🔍 Anomaly detection for unusual sales patterns  
- 💡 Business-friendly insights that drive smarter decisions  

The impact: **higher profitability, reduced waste, and improved customer satisfaction** — all in a lightweight, plug-and-play solution.

---

## 🛒 The Retail Inventory Problem  

Retail shop owners often struggle with:  
- **Overstocking** → Capital locked in unsold goods  
- **Stockouts** → Lost revenue and customer churn  
- **Manual Forecasting** → Time-consuming, error-prone spreadsheets  
- **Complex ERP Systems** → Expensive, hard to implement, overkill for small shops  
- **Basic Dashboards** → Show past sales but lack predictive intelligence  

---

## 🚀 How Smart Inventory AI Pro is Different  

| Existing Solutions | Limitations | Smart Inventory AI Pro Advantage |
|--------------------|-------------|----------------------------------|
| Excel sheets | Manual, error-prone | Automated AI forecasting |
| ERP systems | Costly, complex | Lightweight, modular, easy to deploy |
| Sales dashboards | Historical only | Predictive + prescriptive insights |

**Key Differentiators:**  
- 🧠 **AI-Powered Forecasting** (ensemble methods for robust accuracy)  
- 💡 **Explainable Insights** (business-friendly recommendations)  
- ⚡ **Lightweight Deployment** (Streamlit-based, runs locally or in cloud)  
- 📂 **Plug-and-Play CSV Upload** (no complex integrations required)  
- 🧩 **Modular Architecture** (easy to extend, customize, and scale)  

---

## 💼 Why This Matters  

- **Profitability Boost**: Reduce capital lock-in and avoid costly stockouts.  
- **Operational Efficiency**: Automate forecasting and inventory planning.  
- **Accessibility**: Designed for small and medium retailers, not just enterprises.  
- **Scalability**: Works for single shops or multi-store chains.  

---

## 🏗️ System Architecture  

Smart Inventory AI Pro follows a **modular, layered design**:  

- **Frontend (Streamlit)** → Interactive dashboards and visualizations  
- **Models Layer** → Forecasting, anomaly detection, inventory optimization  
- **Explainability Layer** → Business insights and recommendations  
- **Utilities Layer** → Data loaders, helpers, validation  
- **Config Layer** → Themes, styling, customization  

This separation of concerns ensures **maintainability, extensibility, and clean interfaces**.

---

## 🤖 AI & ML Techniques  

- **Ensemble Forecasting**: EWMA, Linear Regression, Seasonal Decomposition  
- **Anomaly Detection**: Statistical + IQR-based methods with severity scoring  
- **Safety Stock Optimization**: Dynamic calculations based on demand volatility  
- **Reorder Point Logic**: Lead time + demand variability for smarter replenishment  

---

## 🎯 For Retailers (Simple Value Proposition)  

- No more guessing stock levels.  
- No more losing sales because of empty shelves.  
- No more wasting money on excess inventory.  

👉 Just upload your sales CSV, and let Smart Inventory AI Pro tell you **what to order, when, and how much**.

---

## 📂 Dataset Usage  

To make testing and evaluation easier, a ready-to-use kaggle dataset is included in the **`dataset/`** folder.  

This dataset allows you to:  
- Instantly explore forecasting features  
- Test anomaly detection  
- Validate inventory optimization logic  
- Understand dashboard visualizations  

You can either:  
1. Use the built-in AI-generated sample data inside the app  
2. Upload the provided dataset from the `dataset/` folder  
3. Upload your own retail sales CSV file  

### 📑 Expected CSV Format  

```csv
date,product_id,units_sold
2024-01-01,PROD001,45
2024-01-02,PROD002,52
2024-01-03,PROD003,48
```

---

## 📊 Project Structure  

```plaintext
smart_inventory_ai/
│
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── config/
│   └── theme.py            # CSS styling and theme configuration
│
├── data/
│   └── sample_generator.py # Sample data generation
│
├── models/
│   ├── forecasting.py      # Forecasting engine with ensemble methods
│   ├── anomaly.py          # Anomaly detection algorithms
│   ├── inventory.py        # Inventory optimization logic
│   └── explainability.py   # Business insights generation
│
├── dashboard/
│   ├── charts.py           # Plotly chart generation
│   ├── metrics.py          # Metric card components
│   └── layout.py           # UI layout and components
│
├── utils/
│   ├── data_loader.py      # Data loading and validation
│   └── helpers.py          # Helper utility functions
│
└── assets/
    ├── sia_logo.jpeg       # SIA Logo
    └── styles.css          # Additional CSS styles
```

---

## 🖥️ Live Demo  

🔗 **https://smart-inventory-ai.streamlit.app/**

---

## 📽️ Video Link

🔗 **https://drive.google.com/file/d/1LqqKrBUPrDJuQnh20z9ohztSg4OZNlcq/view?usp=drivesdk**

---

## 🔮 Future Roadmap  

- 📡 **API Integration** with POS systems  
- 📱 **Mobile App** for shop owners  
- 🧾 **Multi-Product Forecasting** with portfolio optimization  
- 🌍 **Cloud Deployment** for scalability  
- 🛒 **Retail-Specific Modules** (perishables, seasonal goods, promotions)  

---

## 🛠️ Quick Start  

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

Upload your CSV (`date, product_id, units_sold`) and start optimizing inventory instantly.

---

## 📈 Model Performance  

Validated with walk-forward testing:  
- **MAE** → Average prediction error in units  
- **MAPE** → Percentage-based accuracy measure  

Typical accuracy:  
- ><10% → Excellent  
- >10–20% → Good  
- >20% → Fair  

---

## 🤝 Contributing  

We welcome contributions, feature requests, and collaborations.  
Open an issue or submit a pull request to join the project.  

---

## 📧 Support  

For questions or support, please open an issue in this repository.  

---

**Built with ❤️ by Team Eureka Fourge**  

**Team Information**  
- Himanshu Jadhav *(Team Leader)*  
- Yash Bhongale  
- Ritesh Gaike  
- Onkar Kharat  

---
