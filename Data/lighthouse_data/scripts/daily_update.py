import sys
import os

# Add project root to python path so we can import lighthouse_data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lighthouse_data.orchestration.daily_flows import DailyFlow

if __name__ == "__main__":
    DailyFlow().run_all()
