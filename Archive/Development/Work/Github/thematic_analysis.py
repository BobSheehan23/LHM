import pandas as pd
import numpy as np

# --- Configuration ---
DATA_FILE_PATH = 'Daily_Data_Dispatch_2025-06-17_bsheehan.csv'

# --- Model 1: Thematic & Sector Deep Dives ---

def load_data(file_path):
    """Loads and prepares the data for analysis."""
    try:
        df = pd.read_csv(file_path)
        # Basic data cleaning and renaming can be done here
        df.rename(columns={
            'Utilization (%)': 'Utilization_Pct',
            'Average Fee': 'AvgFee',
            'Days to Cover': 'DaysToCover',
            'Short Interest Indicator': 'ShortInterestPct'
        }, inplace=True, errors='ignore')
        return df
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}")
        return None

def define_themes_and_sectors(df):
    """Placeholder function to define thematic and sector groups.
       This could be based on GICS sectors or custom logic.
    """
    # Example: This could be a mapping from Ticker to Theme/Sector
    # In a real scenario, this might come from another file or API
    df['Theme'] = 'Tech' # Placeholder
    return df

def calculate_dynamic_thresholds(df, group_by_col='Theme'):
    """Calculates dynamic thresholds based on historical data for each group."""
    # Example: Calculate 1-year rolling average and standard deviation for Utilization
    # This is a simplified example. A real implementation would need historical data.
    
    # Placeholder for dynamic thresholds
    thresholds = df.groupby(group_by_col)['Utilization_Pct'].agg(['mean', 'std']).reset_index()
    thresholds.rename(columns={'mean': 'utilization_mean', 'std': 'utilization_std'}, inplace=True)
    
    df = pd.merge(df, thresholds, on=group_by_col, how='left')
    
    # Define threshold as mean + 1 standard deviation
    df['utilization_threshold'] = df['utilization_mean'] + df['utilization_std']
    
    return df

def apply_thematic_analysis(df):
    """Applies the multi-factor threshold analysis to identify crowded trades."""
    
    # Apply dynamic threshold for Utilization
    df['crowded_trade_flag'] = df['Utilization_Pct'] > df['utilization_threshold']
    
    # Add other conditions based on other metrics like AvgFee, DaysToCover, etc.
    # For example:
    df['crowded_trade_flag'] = df['crowded_trade_flag'] & (df['AvgFee'] > 100) # Example threshold for AvgFee in bps
    df['crowded_trade_flag'] = df['crowded_trade_flag'] & (df['DaysToCover'] > 5) # Example threshold for DTC
    
    return df[df['crowded_trade_flag']]

# --- Main Execution ---
if __name__ == "__main__":
    print("Running Thematic & Sector Deep Dive Analysis...")
    
    # 1. Load data
    main_df = load_data(DATA_FILE_PATH)
    
    if main_df is not None:
        # 2. Define themes and sectors
        themed_df = define_themes_and_sectors(main_df)
        
        # 3. Calculate dynamic thresholds
        df_with_thresholds = calculate_dynamic_thresholds(themed_df)
        
        # 4. Apply the analysis
        crowded_trades_df = apply_thematic_analysis(df_with_thresholds)
        
        print("\nAnalysis Complete.")
        print(f"Found {len(crowded_trades_df)} potential crowded trades.")
        
        if not crowded_trades_df.empty:
            print("\n--- Crowded Trades --- ")
            print(crowded_trades_df[['Ticker', 'Theme', 'Utilization_Pct', 'AvgFee', 'DaysToCover']].head())