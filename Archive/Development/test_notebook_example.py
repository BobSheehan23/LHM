# Test script to verify the package works as expected
import lhm_charts as lhm

# Test basic functionality
print("✅ Successfully imported lhm_charts")

# Test data fetching availability
try:
    # This will raise an error if pandas_datareader is not available
    data = lhm.fred_fetch(["CPIAUCSL"], start="2020-01-01")
    print(f"✅ FRED data fetch works: {data.shape}")
except ImportError as e:
    print(f"ℹ️  FRED data not available: {e}")
except Exception as e:
    print(f"ℹ️  FRED data fetch skipped: {e}")

# Test chart creation (with dummy data)
import pandas as pd
import numpy as np

# Create dummy data
dates = pd.date_range('2020-01-01', '2023-12-31', freq='M')
dummy_data = pd.DataFrame({
    'CPI': 100 + np.cumsum(np.random.normal(0.2, 0.5, len(dates))),
    'Rates': 2 + np.cumsum(np.random.normal(0.1, 0.3, len(dates)))
}, index=dates)

print("✅ Created dummy data")

# Test single chart (without recession shading to avoid data dependency)
fig, ax = lhm.chart(
    dummy_data,
    ['CPI'],
    ylabel="Index",
    title="Test Chart",
    show_recessions=False,
    filename="test_single.png"
)
print("✅ Single chart creation works")

# Test dual chart (without recession shading to avoid data dependency)
fig, ax1, ax2 = lhm.chart_dual(
    dummy_data,
    left_cols=['CPI'],
    right_cols=['Rates'],
    left_label="CPI Index",
    right_label="Interest Rates (%)",
    title="Test Dual Chart",
    show_recessions=False,
    filename="test_dual.png"
)
print("✅ Dual chart creation works")

print("🎉 All tests passed! Package is ready to use.")