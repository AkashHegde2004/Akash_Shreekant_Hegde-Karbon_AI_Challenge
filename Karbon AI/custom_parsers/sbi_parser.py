import pandas as pd
import pdfplumber
import re

def parse(file_path: str) -> pd.DataFrame:
    """
    Parse SBI bank PDF/CSV file and return a pandas DataFrame.
    
    Parameters:
    file_path (str): Path to the PDF/CSV file.
    
    Returns:
    pd.DataFrame: A pandas DataFrame containing the parsed data.
    """
    
    # Check if file is a PDF or CSV
    if file_path.endswith('.pdf'):
        # Extract text from PDF
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        
        # Split text into lines
        lines = text.split('\n')
        
        # Remove empty lines
        lines = [line for line in lines if line.strip()]
        
        # Split lines into columns
        columns = lines[0].split(',')
        data = []
        for line in lines[1:]:
            data.append(line.split(','))
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=columns)
    else:
        # Load CSV file
        df = pd.read_csv(file_path)
    
    # Handle repeated headers
    df.columns = df.columns.astype(str)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(r'\s+', ' ', regex=True)
    df.columns = df.columns.str.strip()
    
    # Remove empty rows
    df = df.dropna(how='all')
    
    # Clean numeric columns
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0.0)
    
    # Replace NaN in non-numeric columns with ""
    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna("")
    
    return df