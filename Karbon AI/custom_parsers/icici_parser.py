import pandas as pd
import pdfplumber
import re

def parse(file_path: str) -> pd.DataFrame:
    """
    Parse ICICI bank PDF/CSV file and return a pandas DataFrame.
    
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
        columns = []
        for line in lines:
            columns.append(re.split(r'\s{2,}', line))
        
        # Transpose columns
        columns = list(map(list, zip(*columns)))
        
        # Create DataFrame
        df = pd.DataFrame(columns)
        
        # Remove empty rows
        df = df.dropna(how='all')
        
        # Remove repeated headers
        df = df.drop_duplicates(subset=0, keep='first')
        
        # Clean numeric columns
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(0.0)
        
        # Clean string columns
        for col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna('')
    
    elif file_path.endswith('.csv'):
        # Read CSV file
        df = pd.read_csv(file_path)
    
    else:
        raise ValueError('Unsupported file type')
    
    return df