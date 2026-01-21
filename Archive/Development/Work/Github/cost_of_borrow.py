import pandas as pd
import numpy as np

# --- Configuration ---
DATA_FILE_PATH = 'Daily_Data_Dispatch_2025-06-17_bsheehan.csv'

# --- Model 4: Cost of Borrow as a Sentiment Indicator ---

def load_data(file_path):
    """Loads and prepares the data for analysis."""
    try:
        df = pd.read_csv(file_path)
        df.rename(columns={
            'Average Fee': 'AvgFee',
            # Add other relevant columns here
        }, inplace=True, errors='ignore')
        return df
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}")
        return None

def analyze_borrow_costs(df):
    """Analyzes the drivers and predictive power of borrow costs."""
    
    if df is None:
        return

    # Distinguish between general collateral and special stocks
    df['StockType'] = np.where(df['AvgFee'] > 100, 'Special', 'General') # Example threshold: 100 bps
    
    print("--- Analysis of Borrow Costs ---")
    print("\nDistribution of Stock Types:")
    print(df['StockType'].value_counts())
    
    # Analyze the correlation between borrow cost and other factors
    correlation_matrix = df[['AvgFee', 'Utilization_Pct', 'DaysToCover']].corr()
    
    print("\nCorrelation Matrix:")
    print(correlation_matrix)
    
    # Identify stocks with high and rising borrow costs
    # This would typically involve time-series analysis, but for this example,
    # we'll just identify stocks with high fees.
    high_conviction_shorts = df[df['AvgFee'] > 300] # Example threshold for high conviction
    
    print("\n--- High Conviction Shorts (AvgFee > 300 bps) ---")
    if not high_conviction_shorts.empty:
        print(high_conviction_shorts[['Ticker', 'AvgFee', 'Utilization_Pct', 'DaysToCover']].head())
    else:
        print("No securities found with an average fee greater than 300 bps.")

# --- Main Execution ---
if __name__ == "__main__":
    print("Running Cost of Borrow Analysis...")
    
    # 1. Load data
    main_df = load_data(DATA_FILE_PATH)
    
    # 2. Perform analysis
    analyze_borrow_costs(main_df)