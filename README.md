```markdown
# 🏗️ CONSTRIQ | Smart Dual-BOQ PDF & Architectural Drawing Change Analyzer

**CONSTRIQ** is an AI-powered construction change analysis and risk management platform. Built with Python and Streamlit and powered by Groq’s high-speed LLM infrastructure (`gpt-oss-120b` and `qwen/qwen3.6-27b`), CONSTRIQ automates dual Bill of Quantities (BOQ) comparison, visual drawing diff inspections, financial variance calculations, and downstream risk synthesis.

---

## 🚀 Key Features

- **Multi-Format BOQ Parsing:** Normalizes and compares Old vs. New BOQs across **CSV**, **XLSX**, and **PDF** formats.
- **Architectural Drawing Vision Inspection:** Analyzes single or dual construction drawings (**PNG**, **JPG**, or **PDF**) using multimodal vision AI to detect structural modifications, spatial layout changes, and annotation revisions.
- **Deterministic Calculation Engine:** Evaluates non-deterministic AI extraction through an isolated mathematical variance engine to compute exact `Old Qty`, `New Qty`, `Delta Qty`, and net `Cost Impact`.
- **Downstream Ripple & Risk Synthesis:** Identifies multi-trade schedule impacts, supply chain lead-time risks, and actionable field mitigation steps.
- **Interactive Dashboard & CSV Export:** Visualizes risk metrics and metrics breakdowns, with one-click exporting to CSV.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **AI Models (via Groq API):**
  - **Text Processing & Delta Extraction:** `openai/gpt-oss-120b`
  - **Vision & Drawing Analysis:** `qwen/qwen3.6-27b`
- **Data Engine & Math:** Pandas
- **PDF & Document Processing:** `pypdf`, `pypdfium2`, `pillow`

---

## 📁 Repository Structure

```text
├── app.py              # Streamlit UI orchestrator and session state engine
├── config.py           # Environment secrets and Groq API client initialization
├── boq.py              # Multi-format BOQ reader and table extractor
├── ai.py               # Groq LLM extraction for BOQ changes & structural JSON output
├── vision.py           # PDF-to-image conversion and vision AI drawing comparison
├── calculations.py     # Deterministic financial and quantity variance engine
├── impact.py           # Downstream risk, schedule, and trade ripple analysis engine
├── report.py           # Dashboard layout, visual metrics, and CSV export logic
├── utils.py            # Utility functions (formatting, base64 encoding)
└── requirements.txt    # Production Python dependencies

```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/iamyounasali/constiq.git](https://github.com/iamyounasali/constiq.git)
cd constiq

```

### 2. Create and Activate Virtual Environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure API Keys

Add your Groq API Key inside `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "gsk_your_groq_api_key_here"

```

---

## 🏃 Running the Application

To launch CONSTRIQ locally:

```bash
streamlit run app.py

```

Access the app in your browser at `http://localhost:8501`.

---

## ☁️ Streamlit Cloud Deployment

1. Connect your repository (`iamyounasali/constiq`) to [Streamlit Cloud](https://share.streamlit.io/).
2. In **App Settings > Secrets**, paste your key:
```toml
GROQ_API_KEY = "gsk_your_groq_api_key_here"

```


3. Set main file path to `app.py` and click **Deploy**.

```

```
