import pandas as pd
import pypdf

def parse_pdf_boq_to_df(file_buffer):
    """Extracts text/tables from a PDF BOQ and converts it into a DataFrame."""
    try:
        reader = pypdf.PdfReader(file_buffer)
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
                
        lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]
        rows = []
        for line in lines:
            parts = line.split(',') if ',' in line else line.split('\t')
            if len(parts) >= 5:
                rows.append(parts[:5])
                
        if rows:
            return pd.DataFrame(rows[1:], columns=rows[0])
    except Exception:
        pass
        
    return pd.DataFrame(columns=['item_id', 'description', 'unit', 'rate', 'current_qty'])

def load_boq_data(file_path_or_buffer):
    """
    Reads CSV, Excel (XLSX), or PDF BOQ files into a normalized Pandas DataFrame.
    """
    try:
        file_name = file_path_or_buffer.name if hasattr(file_path_or_buffer, 'name') else str(file_path_or_buffer)
        
        if file_name.endswith('.csv'):
            df = pd.read_csv(file_path_or_buffer)
        elif file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path_or_buffer)
        elif file_name.endswith('.pdf'):
            df = parse_pdf_boq_to_df(file_path_or_buffer)
        else:
            raise ValueError("Unsupported file format.")
                
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Ensure all required keys exist to prevent downstream KeyError bugs
        required_cols = ['item_id', 'description', 'unit', 'rate', 'current_qty']
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0.0 if col in ['rate', 'current_qty'] else "N/A"
                
        df['rate'] = pd.to_numeric(df['rate'], errors='coerce').fillna(0.0)
        df['current_qty'] = pd.to_numeric(df['current_qty'], errors='coerce').fillna(0.0)
        
        return df
    except Exception as e:
        raise Exception(f"Failed to parse BOQ file: {str(e)}")

def get_boq_summary_list(df):
    """Returns a simplified list of items for LLM prompt context."""
    items = []
    if df is not None and not df.empty:
        for _, row in df.iterrows():
            items.append({
                "item_id": str(row.get('item_id', '')),
                "description": str(row.get('description', '')),
                "unit": str(row.get('unit', '')),
                "rate": float(row.get('rate', 0.0))
            })
    return items
