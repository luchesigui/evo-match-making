#!/usr/bin/env python3
"""
Script to filter clientes.xlsx based on CONTRATO column and export ID, NOME, and CONTRATO
Creates two files:
- alunos.xlsx: entries that do NOT contain WELLHUB, TOTALPASS, VIP or empty
- agregadores.xlsx: entries that contain WELLHUB or TOTALPASS
"""

import pandas as pd
import os
import sys
from datetime import datetime

def load_excel_file(file_path):
    """Load Excel file and return DataFrame"""
    try:
        df = pd.read_excel(file_path)
        print(f"✓ Loaded {file_path}: {len(df)} rows, {len(df.columns)} columns")
        return df
    except FileNotFoundError:
        print(f"✗ Error: File {file_path} not found")
        return None
    except Exception as e:
        print(f"✗ Error reading {file_path}: {str(e)}")
        return None

def display_file_structure(df, file_name):
    """Display the structure of the DataFrame"""
    print(f"\n--- Structure of {file_name} ---")
    print(f"Columns: {list(df.columns)}")
    print(f"Shape: {df.shape}")
    print(f"Data types:")
    print(df.dtypes)
    print(f"\nFirst 3 rows:")
    print(df.head(3))

def filter_alunos_by_contrato(df):
    """Filter alunos DataFrame based on CONTRATO column"""
    
    # Check if required columns exist
    required_columns = ['ID', 'NOME', 'CONTRATO']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"✗ Missing required columns: {missing_columns}")
        return None, None
    
    print("🔍 Filtering based on CONTRATO column...")
    
    # Define the filter criteria
    filter_keywords = ['WELLHUB', 'TOTALPASS', 'VIP']
    agregadores_keywords = ['WELLHUB', 'TOTALPASS']
    
    # Create filter conditions
    conditions = []
    
    # Check for empty/null values
    empty_condition = df['CONTRATO'].isna() | (df['CONTRATO'] == '') | (df['CONTRATO'].str.strip() == '')
    conditions.append(empty_condition)
    
    # Check for keywords in CONTRATO column
    for keyword in filter_keywords:
        keyword_condition = df['CONTRATO'].str.contains(keyword, case=False, na=False)
        conditions.append(keyword_condition)
    
    # Combine all conditions with OR for general filter
    final_condition = conditions[0]
    for condition in conditions[1:]:
        final_condition = final_condition | condition
    
    # Apply filter for alunos.xlsx (INVERT - entries that DON'T have the keywords)
    filtered_df = df[~final_condition]  # Use NOT operator (~) to invert the condition
    result_df = filtered_df[['ID', 'NOME', 'CONTRATO']].copy()
    
    # Create agregadores filter (only WELLHUB and TOTALPASS)
    agregadores_conditions = []
    for keyword in agregadores_keywords:
        keyword_condition = df['CONTRATO'].str.contains(keyword, case=False, na=False)
        agregadores_conditions.append(keyword_condition)
    
    # Combine agregadores conditions with OR
    agregadores_final_condition = agregadores_conditions[0]
    for condition in agregadores_conditions[1:]:
        agregadores_final_condition = agregadores_final_condition | condition
    
    # Apply filter for agregadores.xlsx
    agregadores_df = df[agregadores_final_condition]
    agregadores_result_df = agregadores_df[['ID', 'NOME', 'CONTRATO']].copy()
    
    print(f"📊 Original alunos entries: {len(df)}")
    print(f"📊 Filtered entries (NOT containing keywords): {len(result_df)}")
    print(f"📊 Agregadores entries (WELLHUB + TOTALPASS): {len(agregadores_result_df)}")
    
    # Show breakdown by filter criteria
    print(f"\n📈 Breakdown of entries with keywords (excluded from alunos):")
    empty_count = len(df[empty_condition])
    print(f"   Empty/null CONTRATO: {empty_count}")
    
    for keyword in filter_keywords:
        keyword_condition = df['CONTRATO'].str.contains(keyword, case=False, na=False)
        keyword_count = len(df[keyword_condition])
        print(f"   Contains '{keyword}': {keyword_count}")
    
    print(f"\n📈 Entries in alunos.xlsx: {len(result_df)} (NOT containing WELLHUB, TOTALPASS, VIP, or empty)")
    
    return result_df, agregadores_result_df

def generate_output_filename(file_type):
    """
    Generate output filename based on current date
    Format: 2025-{month}-{period}-acessos-{type}.xlsx
    
    Args:
        file_type: 'alunos' or 'agregadores'
    
    Returns:
        Formatted filename
    """
    now = datetime.now()
    
    # Month names in Portuguese (3 letters)
    months = {
        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr',
        5: 'mai', 6: 'jun', 7: 'jul', 8: 'ago',
        9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
    }
    
    month = months[now.month]
    
    # Determine period based on day
    period = "1-3" if now.day < 20 else "4-7"
    
    # Format: 2025-{month}-{period}-acessos-{type}.xlsx
    filename = f"2025-{month}-{period}-acessos-{file_type}.xlsx"
    
    return filename

def main():
    """Main function"""
    print("🔄 Starting alunos filtering process...")
    
    # File paths
    clientes_file = "FREQUENCIA.xlsx"
    output_file = generate_output_filename("alunos")
    agregadores_file = generate_output_filename("agregadores")
    
    # Check if file exists
    if not os.path.exists(clientes_file):
        print(f"✗ Error: {clientes_file} not found")
        sys.exit(1)
    
    # Load Excel file
    print(f"📖 Loading {clientes_file}...")
    clientes_file = load_excel_file(clientes_file)
    
    if clientes_file is None:
        print("✗ Failed to load file")
        sys.exit(1)
    
    # Display file structure
    display_file_structure(clientes_file, clientes_file)
    
    # Filter the data
    print(f"\n🔄 Filtering alunos...")
    filtered_df, agregadores_df = filter_alunos_by_contrato(clientes_file)
    
    if filtered_df is None or agregadores_df is None:
        print("✗ Failed to filter data")
        sys.exit(1)
    
    # Display sample of filtered data
    print(f"\n📋 Sample of filtered data (NOT containing keywords):")
    print(filtered_df.head(10))
    
    print(f"\n📋 Sample of agregadores data (WELLHUB + TOTALPASS):")
    print(agregadores_df.head(10))
    
    # Save the results
    print(f"\n💾 Saving results...")
    
    # Save alunos.xlsx
    try:
        filtered_df.to_excel(output_file, index=False)
        print(f"✓ Successfully saved {output_file}")
        print(f"✓ Exported {len(filtered_df)} entries NOT containing keywords with ID, NOME, CONTRATO columns")
    except Exception as e:
        print(f"✗ Error saving {output_file}: {str(e)}")
        sys.exit(1)
    
    # Save agregadores.xlsx
    try:
        agregadores_df.to_excel(agregadores_file, index=False)
        print(f"✓ Successfully saved {agregadores_file}")
        print(f"✓ Exported {len(agregadores_df)} entries with WELLHUB/TOTALPASS with ID, NOME, CONTRATO columns")
    except Exception as e:
        print(f"✗ Error saving {agregadores_file}: {str(e)}")
        sys.exit(1)
    
    print(f"\n✨ Process completed successfully!")
    print(f"   Original alunos entries: {len(clientes_file)}")
    print(f"   Filtered entries (NOT containing keywords): {len(filtered_df)}")
    print(f"   Agregadores entries (WELLHUB + TOTALPASS): {len(agregadores_df)}")
    print(f"   Output files: {output_file}, {agregadores_file}")
    print(f"   Columns in output: ID, NOME, CONTRATO")

if __name__ == "__main__":
    main() 