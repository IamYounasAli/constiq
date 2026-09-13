import pandas as pd
import pypdf

def extract_text_from_pdf(pdf_file) -> str:
    """Extracts raw text content from an uploaded PDF BOQ."""
    reader = pypdf.PdfReader(pdf_file)
    extracted_text = ""
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            extracted_text += f"\n--- Page {idx + 1} ---\n" + text
    return extracted_text

def parse_pdf_boq_to_df(pdf_file) -> pd.DataFrame:
    """Parses BOQ PDF text into a structured Pandas DataFrame."""
    raw_text = extract_text_from_pdf(pdf_file)
    lines = raw_text.splitlines()
    
    records = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 4:
            try:
                qty = float(parts[-1].replace(',', ''))
                rate = float(parts[-2].replace(',', ''))
                unit = parts[-3]
                item_id = parts[0]
                description = " ".join(parts[1:-3])
                if description:
                    records.append({
                        "item_id": item_id,
                        "description": description,
                        "unit": unit,
                        "rate": rate,
                        "current_qty": qty
                    })
            except (ValueError, IndexError):
                continue
                
    if records:
        return pd.DataFrame(records)
    
    return pd.DataFrame(columns=["item_id", "description", "unit", "rate", "current_qty"])

def load_boq_data(uploaded_file) -> pd.DataFrame:
    """Loads BOQ from CSV, Excel, or PDF."""
    filename = uploaded_file.name.lower()
    if filename.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif filename.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(uploaded_file)
    elif filename.endswith('.pdf'):
        df = parse_pdf_boq_to_df(uploaded_file)
    else:
        raise ValueError("Unsupported file format.")
    
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def compare_boq_pdfs(old_pdf, new_pdf):
    """Parses both Old and New PDF BOQs and extracts their content."""
    old_df = load_boq_data(old_pdf)
    new_df = load_boq_data(new_pdf)
    
    old_text = extract_text_from_pdf(old_pdf)
    new_text = extract_text_from_pdf(new_pdf)
    
    return {
        "old_df": old_df,
        "new_df": new_df,
        "old_text": old_text,
        "new_text": new_text
    }
