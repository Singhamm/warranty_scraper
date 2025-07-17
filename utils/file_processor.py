import pandas as pd

def process_uploaded_file(file):
    """Handle CSV/Excel uploads and validate structure"""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file, engine='openpyxl')
        
        # Validate required column
        if "Serial Number" not in df.columns:
            raise ValueError("File must contain 'Serial Number' column")
        
        return df
    
    except Exception as e:
        raise ValueError(f"File processing error: {str(e)}")