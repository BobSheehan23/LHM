import pandas as pd

# --- Configuration ---
DATA_FILE_PATH = 'Daily_Data_Dispatch_2025-06-17_bsheehan.csv'
EVENTS_FILE_PATH = 'corporate_events.csv' # Example file with event data

# --- Model 2: Corporate & Market Events Analysis ---

def load_data(file_path):
    """Loads and prepares the securities lending data."""
    try:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date']) # Assuming a 'Date' column exists
        return df
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}")
        return None

def load_events_data(file_path):
    """Loads corporate events data."""
    try:
        events_df = pd.read_csv(file_path)
        events_df['EventDate'] = pd.to_datetime(events_df['EventDate'])
        return events_df
    except FileNotFoundError:
        print(f"Error: Events file not found at {file_path}")
        return None

def analyze_events(data_df, events_df):
    """Analyzes securities lending data around corporate events."""
    
    if data_df is None or events_df is None:
        return

    for index, event in events_df.iterrows():
        ticker = event['Ticker']
        event_date = event['EventDate']
        event_type = event['EventType']
        
        # Define pre- and post-event windows
        pre_event_window_start = event_date - pd.Timedelta(days=30)
        post_event_window_end = event_date + pd.Timedelta(days=30)
        
        # Filter data for the specific ticker and window
        event_data = data_df[(data_df['Ticker'] == ticker) &
                             (data_df['Date'] >= pre_event_window_start) &
                             (data_df['Date'] <= post_event_window_end)]
        
        if not event_data.empty:
            # Example Analysis: Calculate the average utilization before and after the event
            pre_event_data = event_data[event_data['Date'] < event_date]
            post_event_data = event_data[event_data['Date'] > event_date]
            
            avg_util_pre = pre_event_data['Utilization_Pct'].mean()
            avg_util_post = post_event_data['Utilization_Pct'].mean()
            
            print(f"--- Analysis for {ticker} around {event_type} on {event_date.date()} ---")
            print(f"  Avg. Utilization (30d Pre-Event): {avg_util_pre:.2f}%")
            print(f"  Avg. Utilization (30d Post-Event): {avg_util_post:.2f}%")
            print("\n")

# --- Main Execution ---
if __name__ == "__main__":
    print("Running Corporate & Market Events Analysis...")
    
    # 1. Load securities lending data
    main_data_df = load_data(DATA_FILE_PATH)
    
    # 2. Load corporate events data
    # This is a placeholder. In a real scenario, you would create this file.
    # Example corporate_events.csv:
    # Ticker,EventType,EventDate
    # AAPL,Earnings,2025-07-28
    # GOOG,M&A,2025-08-15
    events_df = load_events_data(EVENTS_FILE_PATH)
    
    # 3. Analyze data around events
    analyze_events(main_data_df, events_df)
