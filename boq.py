import pandas as pd
import pypdf

def extract_raw_text_from_pdf(file_buffer):
    """Extracts all raw text page-by-page from a PDF buffer."""
    extracted_text = ""
    try:
        if hasattr(file_buffer, 'seek'):
            file_buffer.seek(0)
        reader = pypdf.PdfReader(file_buffer)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    except Exception as e:
        extracted_text = f"Error reading PDF text: {str(e)}"
    finally:
        if hasattr(file_buffer, 'seek'):
            file_buffer.seek(0)
    return extracted_text.strip()

def parse_pdf_boq_to_df(file_buffer):
    """Attempts structured tabular extraction from PDF, falling back gracefully."""
    try:
        raw_text = extract_raw_text_from_pdf(file_buffer)
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        rows = []
        
        for line in lines:
            # Try comma or tab splitting
            parts = line.split(',') if ',' in line else line.split('\t')
            # Fallback to multi-space alignment splitting for standard BOQ layouts
            if len(parts) < 3:
                parts = [p.strip() for p in line.split('  ') if p.strip()]
            
            if len(parts) >= 3:
                rows.append(parts)
                
        if len(rows) > 1:
            headers = ['item_id', 'description', 'unit', 'rate', 'current_qty']
            df = pd.DataFrame(rows[1:], columns=headers[:len(rows[0])])
            return df
    except Exception:
        pass
        
    return pd.DataFrame(columns=['item_id', 'description', 'unit', 'rate', 'current_qty'])

def load_boq_data(file_path_or_buffer):
    """
    Reads CSV, Excel (XLSX), or PDF BOQ files into a normalized Pandas DataFrame.
    """
    try:
        file_name = file_path_or_buffer.name if hasattr(file_path_or_buffer, 'name') else str(file_path_or_buffer)
        
        if hasattr(file_path_or_buffer, 'seek'):
            file_path_or_buffer.seek(0)
            
        if file_name.lower().endswith('.csv'):
            df = pd.read_csv(file_path_or_buffer)
        elif file_name.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path_or_buffer)
        elif file_name.lower().endswith('.pdf'):
            df = parse_pdf_boq_to_df(file_path_or_buffer)
        else:
            raise ValueError("Unsupported file format.")
                
        df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')
        
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

def compare_boq_pdfs(old_boq_file, new_boq_file):
    """
    Extracts raw context strings and structured DataFrames from old and new BOQs.
    Handles CSV, XLSX, and PDF natively.
    """
    old_df = load_boq_data(old_boq_file)
    new_df = load_boq_data(new_boq_file)
    
    # Extract raw text if files are PDFs; otherwise use stringified DataFrame representation
    old_name = getattr(old_boq_file, 'name', '').lower()
    new_name = getattr(new_boq_file, 'name', '').lower()

    if old_name.endswith('.pdf'):
        old_text = extract_raw_text_from_pdf(old_boq_file)
    else:
        old_text = old_df.to_string(index=False)

    if new_name.endswith('.pdf'):
        new_text = extract_raw_text_from_pdf(new_boq_file)
    else:
        new_text = new_df.to_string(index=False)
        
    return {
        "old_text": old_text,
        "new_text": new_text,
        "old_df": old_df,
        "new_df": new_df
    }
