import pandas as pd

def load_boq_data(file_path_or_buffer):
    """
    Reads CSV or Excel BOQ file into a normalized Pandas DataFrame.
    Expected columns: item_id, description, unit, rate, current_qty
    """
    try:
        if hasattr(file_path_or_buffer, 'name'):
            if file_path_or_buffer.name.endswith('.csv'):
                df = pd.read_csv(file_path_or_buffer)
            else:
                df = pd.read_excel(file_path_or_buffer)
        else:
            if str(file_path_or_buffer).endswith('.csv'):
                df = pd.read_csv(file_path_or_buffer)
            else:
                df = pd.read_excel(file_path_or_buffer)
                
        # Column name normalization
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        required_cols = ['item_id', 'description', 'unit', 'rate', 'current_qty']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column in BOQ: '{col}'")
                
        df['rate'] = pd.to_numeric(df['rate'], errors='coerce').fillna(0.0)
        df['current_qty'] = pd.to_numeric(df['current_qty'], errors='coerce').fillna(0.0)
        
        return df
    except Exception as e:
        raise Exception(f"Failed to parse BOQ file: {str(e)}")

def get_boq_summary_list(df):
    """Returns a simplified list of items for LLM prompt context."""
    items = []
    for _, row in df.iterrows():
        items.append({
            "item_id": str(row['item_id']),
            "description": str(row['description']),
            "unit": str(row['unit']),
            "rate": float(row['rate'])
        })
    return items
