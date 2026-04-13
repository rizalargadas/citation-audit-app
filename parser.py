import pandas as pd
import numpy as np

def parse_gsc_export(file):
    """
    Main entry point for parsing GSC CSV or Excel files.
    """
    try:
        # Load the file based on its extension
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Start the cleaning process
        df = normalize_columns(df)
        df = clean_gsc_data(df)

        return df
    except Exception as e:
        raise ValueError(f"Error parsing file: {e}")

def normalize_columns(df):
    """
    Standardize common GSC column variants to Page, Clicks, Impressions, CTR.
    """
    # Mapping of common GSC export column names (Spanish, English variants, etc.)
    # Expand this dictionary as needed for other languages or exports
    column_map = {
        'Top pages': 'Page',
        'Address': 'Page',
        'URL': 'Page',
        'Página': 'Page',
        'Top queries': 'Query',
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

    # Ensure expected columns are present, even if empty
    required_cols = ['Page', 'Clicks', 'Impressions', 'CTR']
    for col in required_cols:
        if col not in df.columns:
            # Fallback if specific expected column wasn't found - helps avoid crashes
            # but we'll flag missing data later
            df[col] = np.nan

    return df

def clean_gsc_data(df):
    """
    Standardize types, handle CTR, and remove invalid rows.
    """
    # 1. Drop rows where essential identifiers (Page or Query) are missing
    if 'Page' in df.columns:
        df = df.dropna(subset=['Page'])

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

    # 5. Clean URLs: specifically for the Page/Query matching
    if 'Page' in df.columns:
        df['Page'] = df['Page'].astype(str).str.strip()

    return df
