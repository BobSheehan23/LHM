import pandas as pd
import statsmodels.api as sm

# --- Configuration ---
DATA_FILE_PATH = 'Daily_Data_Dispatch_2025-06-17_bsheehan.csv'

# --- Model 3: Factor Correlation Analysis & Multi-Factor Model Enhancement ---

def load_data(file_path):
    """Loads and prepares the data for analysis."""
    try:
        df = pd.read_csv(file_path)
        # Basic data cleaning and renaming can be done here
        df.rename(columns={
            'Utilization (%)': 'Utilization_Pct',
            'Average Fee': 'AvgFee',
            'Days to Cover': 'DaysToCover',
            # Add other factor columns here
        }, inplace=True, errors='ignore')
        return df
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}")
        return None

def factor_neutralization(df, factor_to_neutralize, control_factors):
    """Performs Fama-MacBeth regression to neutralize a factor."""
    
    if df is None or factor_to_neutralize not in df.columns or not all(c in df.columns for c in control_factors):
        print("Error: DataFrame is missing required columns for neutralization.")
        return None

    # Drop rows with missing values in the relevant columns
    df_cleaned = df.dropna(subset=[factor_to_neutralize] + control_factors)

    X = sm.add_constant(df_cleaned[control_factors])
    y = df_cleaned[factor_to_neutralize]
    
    model = sm.OLS(y, X).fit()
    
    residuals = model.resid
    
    neutralized_factor_name = f"{factor_to_neutralize}_neutralized"
    df_cleaned[neutralized_factor_name] = residuals
    
    return df_cleaned

# --- Main Execution ---
if __name__ == "__main__":
    print("Running Factor Correlation Analysis...")
    
    # 1. Load data
    main_df = load_data(DATA_FILE_PATH)
    
    if main_df is not None:
        # 2. Define control factors (e.g., from a fundamental data source)
        # For this example, we'll use placeholder columns.
        # In a real scenario, you would merge this data in.
        main_df['MarketCap'] = np.random.rand(len(main_df)) * 1e10
        main_df['Momentum'] = np.random.rand(len(main_df)) * 2 - 1

        control_factors = ['MarketCap', 'Momentum']
        factor_to_neutralize = 'Utilization_Pct'

        # 3. Perform factor neutralization
        neutralized_df = factor_neutralization(main_df, factor_to_neutralize, control_factors)
        
        if neutralized_df is not None:
            print("\nFactor Neutralization Complete.")
            print(f"Original {factor_to_neutralize} vs. Neutralized:")
            print(neutralized_df[[factor_to_neutralize, f"{factor_to_neutralize}_neutralized"]].head())