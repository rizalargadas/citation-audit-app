import pandas as pd
import numpy as np

def parse_gsc_combined_excel(file):
    """
    Parses a single Excel file that contains 'Pages' and 'Queries' tabs.
    Returns a tuple of (df_pages, df_queries).
    """
    try:
        # Load the whole Excel workbook
        xls = pd.ExcelFile(file)
        sheet_names = xls.sheet_names

        # Identify the right tabs based on common GSC names
        pages_sheet = next((s for s in sheet_names if 'pages' in s.lower() or 'página' in s.lower()), None)
        queries_sheet = next((s for s in sheet_names if 'queries' in s.lower() or 'consulta' in s.lower()), None)

        if not pages_sheet or not queries_sheet:
            # Fallback: if names differ wildly, try to find sheets by common keywords
            raise ValueError(f"Could not find 'Pages' and 'Queries' tabs. Found: {sheet_names}")

        # Parse Pages
        df_pages = pd.read_excel(xls, sheet_name=pages_sheet)
        df_pages = normalize_columns(df_pages)
        df_pages = clean_gsc_data(df_pages)

        # Parse Queries
        df_queries = pd.read_excel(xls, sheet_name=queries_sheet)
        df_queries = normalize_columns(df_queries)
        df_queries = clean_gsc_data(df_queries)

        return df_pages, df_queries
    except Exception as e:
        raise ValueError(f"Error parsing combined Excel: {e}")

def normalize_columns(df):
    """
    Standardize common GSC column variants to Page, Query, Clicks, Impressions, CTR.
    """
    # Mapping of common GSC export column names (Spanish, English variants, etc.)
    # Expand this dictionary as needed for other languages or exports
    column_map = {
        'Top pages': 'Page',
        'Address': 'Page',
        'URL': 'Page',
        'Página': 'Page',
        'Top queries': 'Query',
        'Queries': 'Query',
        'Consulta': 'Query',
        'Clicks': 'Clicks',
        'Clics': 'Clicks',
        'Impressions': 'Impressions',
        'Impresiones': 'Impressions',
        'CTR': 'CTR',
        'Click-through rate': 'CTR',
        'Average position': 'Position',
        'Posición media': 'Position'
    }

    # Rename columns that exist in the map
    df = df.rename(columns=column_map)

    # Detect if we should have Page or Query
    has_page = 'Page' in df.columns
    has_query = 'Query' in df.columns

    # Ensure expected numeric columns are present, even if empty
    required_numeric = ['Clicks', 'Impressions', 'CTR']
    for col in required_numeric:
        if col not in df.columns:
            df[col] = np.nan

    return df

def clean_gsc_data(df):
    """
    Standardize types, handle CTR, and remove invalid rows.
    """
    # 1. Drop rows where essential identifiers (Page or Query) are missing
    if 'Page' in df.columns:
        df = df.dropna(subset=['Page'])
    elif 'Query' in df.columns:
        df = df.dropna(subset=['Query'])

    # 2. Convert numeric columns and handle malformed data
    numeric_cols = ['Clicks', 'Impressions', 'CTR']
    for col in numeric_cols:
        if col in df.columns:
            # Convert to numeric, turning errors (like strings in numeric cols) into NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Standardize CTR to percentage (0.05 -> 5.0)
    # GSC exports sometimes use decimals (0.05) and sometimes percentages (5.0 or "5%")
    # If the max value is <= 1.0, it's likely a decimal based CTR
    if df['CTR'].max() <= 1.0 and df['CTR'].notna().any():
        df['CTR'] = df['CTR'] * 100

    # 4. Remove rows that couldn't be converted to numbers for essential stats
    df = df.dropna(subset=['Clicks', 'Impressions'])

    # 5. Clean URLs or Queries
    if 'Page' in df.columns:
        df['Page'] = df['Page'].astype(str).str.strip()
    elif 'Query' in df.columns:
        df['Query'] = df['Query'].astype(str).str.strip()

    return df
