from typing import List, Dict


class ThematicAndSectorDeepDives:
    """
    Provides a data-driven perspective on crowded trades and identifies potential
    inflection points within market narratives across themes or sectors.
    """
    def __init__(self):
        self.objective: str = "To provide a unique, data-driven perspective on crowded trades and identify potential points of inflection within prevailing market narratives across specific themes or sectors."
        self.approach: str = "Apply a multi-factor threshold analysis using proprietary Orbisa data, which offers global coverage and daily updates, providing a significant advantage over publicly available, often delayed, data."
        self.key_equilend_metrics: List[str] = [
            "Utilizatin (percentage of lendable shares on loan, indicating supply-side tightness)",
            "Borrow Fee (Orbisa Rate) (annualized cost of borrowing, a direct signal of short-seller conviction)",
            "Days to Cover (DTC) (measures the liquidity risk for short sellers and the potential impact of covering activity)",
            "Surprise in Short Interest (captures rapid changes in shorting activity)"
        ]
        self.dynamic_thresholds_concept: str = "Develop dynamic thresholds for these metrics that adapt to a security's historical behavior and its sector peers (e.g., using standard deviations from a security's 1-year average utilization as a trigger)."
        self.integration_with_macro_data: str = "Align analysis with current hot-button themes (e.g., Artificial Intelligence, Commercial Real Estate, EV manufacturers) or specific GICS sectors. Analyze the entire value chain to observe where short sellers are concentrating their bets."
        self.client_value: str = "Provides clients with an early warning system and unique sentiment overlay for their thematic or sector-specific investments, helping them identify emerging risks or opportunities that might not be visible through traditional fundamental or price-based indicators."

    def summarize(self):
        """Prints a formatted summary of the model's attributes."""
        print(f"Model: Thematic & Sector Deep Dives")
        print(f"Objective: {self.objective}")
        print(f"Approach: {self.approach}")
        print(f"Key Metrics: {', '.join(self.key_equilend_metrics)}")
        print(f"Dynamic Thresholds: {self.dynamic_thresholds_concept}")
        print(f"Macro Integration: {self.integration_with_macro_data}")
        print(f"Client Value: {self.client_value}\n")

class CorporateAndMarketEventsAnalysis:
    """
    Demonstrates how real-time securities lending data provides an informational
    edge around discrete, catalyst-driven events.
    """
    def __init__(self):
        self.objective: str = "To demonstrate how our real-time securities lending data provides a crucial informational edge around discrete, catalyst-driven events."
        self.approach: str = "Analyze patterns in our real-time Orbisa securities lending data, specifically focusing on the behavior of Short Interest, Utilization, and Borrow Costs in the days leading up to and following significant corporate and market events."
        self.event_specific_analysis: Dict[str, str] = {
            "Earnings Announcements": "Examine shifts in borrow demand and cost before and after earnings releases to highlight informed trading activity.",
            "Mergers & Acquisitions (M&A) Deals": "Track short interest around M&A news to reveal market sentiment regarding deal success, potential counter-bids, or the prospects of the combined entity.",
            "Index Inclusion/Exclusion": "Changes in data can signal market positioning ahead of index rebalances, which often drive significant flows and impact liquidity.",
            "Major Regulatory Changes": "Observe how shorting activity and borrowing dynamics react to new regulations, providing insights into potential impacts."
        }
        self.timeliness_advantage: str = "Our daily data frequency provides a significant advantage over lagging public data, allowing for timely identification of market movements related to these events."
        self.client_value: str = "Offers tactical trading insights, allowing portfolio managers and analysts to anticipate or react to informed trading around specific catalysts, thereby optimizing entry and exit points or managing event-driven risk."

    def summarize(self):
        """Prints a formatted summary of the model's attributes."""
        print(f"Model: Corporate & Market Events Analysis")
        print(f"Objective: {self.objective}")
        print(f"Approach: {self.approach}")
        print("Event-Specific Analysis:")
        for event, desc in self.event_specific_analysis.items():
            print(f"  - {event}: {desc}")
        print(f"Timeliness Advantage: {self.timeliness_advantage}")
        print(f"Client Value: {self.client_value}\n")

class EnhancedShortSqueezePrediction:
    """
    Improves short squeeze detection by integrating additional factors and
    developing a more dynamic, regime-aware framework.
    """
    def __init__(self):
        self.objective: str = "To improve the efficacy of existing short squeeze detection by integrating additional factors and developing a more dynamic, regime-aware framework."
        self.approach: str = "Enhance the existing Short Squeeze Score (SSS) by incorporating advanced factor refinement and dynamic modeling techniques."
        self.squeeze_signal_refinements: Dict[str, str] = {
            "On-Loan Stability": "Measures the percentage of loans from 'stable' funds. Low stability suggests shorts are held by tactical traders, who might cover quicker.",
            "Re-rate Percentage & Direction": "Capturing daily repricing activity. A high percentage of 'hotter' re-rates indicates escalating borrowing costs.",
            "Surprise in Short Interest": "A Z-score measuring current short interest relative to its historical mean and standard deviation, signaling rapid sentiment deterioration."
        }
        self.dynamic_regime_aware_model: str = "Apply the 'Spark' model framework to adapt the SSS to changing market conditions (Oversold, Range-Bound, Overbought) by using an ensemble of sub-models or a rules-based system to adjust factor weights."
        self.client_value: str = "Offers a more sophisticated and resilient short squeeze signal that provides context-aware, actionable intelligence for capitalizing on opportunities or managing risks."

    def summarize(self):
        """Prints a formatted summary of the model's attributes."""
        print(f"Model: Enhanced Short Squeeze Prediction and Management")
        print(f"Objective: {self.objective}")
        print(f"Approach: {self.approach}")
        print("Squeeze Signal Refinements:")
        for signal, desc in self.squeeze_signal_refinements.items():
            print(f"  - {signal}: {desc}")
        print(f"Dynamic Regime-Aware Model: {self.dynamic_regime_aware_model}")
        print(f"Client Value: {self.client_value}\n")

class CostOfBorrowAsSentimentIndicator:
    """
    Provides a sophisticated understanding of borrowing costs as a sentiment indicator,
    focusing on how much short sellers are willing to pay.
    """
    def __init__(self):
        self.objective: str = "To provide a sophisticated understanding of borrowing costs, moving beyond 'how many' shares are shorted to 'how much are short sellers willing to pay'."
        self.approach: str = "Focus exclusively on the dynamics and predictive power of proprietary borrowing cost data (Orbisa Rate)."
        self.analysis_points: Dict[str, str] = {
            "Driving Factors Analysis": "Analyze what drives Borrow Costs higher, distinguishing between 'general collateral' and 'special' stocks.",
            "Conviction Signal": "Explore how the magnitude and rate of change in borrow costs correlate with future stock performance.",
            "Integration with Macro & Market Data": "Contextualize borrow costs within the broader market environment (e.g., impact of interest rates and volatility)."
        }
        self.client_value: str = "Provides a nuanced signal of the 'price of pessimism,' offering deeper insights into the conviction behind short positions, crucial for assessing downside risk or identifying opportunities."

    def summarize(self):
        """Prints a formatted summary of the model's attributes."""
        print(f"Model: Cost of Borrow as a Sentiment Indicator")
        print(f"Objective: {self.objective}")
        print(f"Approach: {self.approach}")
        print("Analysis Points:")
        for point, desc in self.analysis_points.items():
            print(f"  - {point}: {desc}")
        print(f"Client Value: {self.client_value}\n")

class CrossAssetSentimentAggregation:
    """
    Develops a holistic view of investor sentiment across a company's capital
    structure by combining data from multiple asset classes.
    """
    def __init__(self):
        self.objective: str = "To develop a holistic view of investor sentiment across a company's entire capital structure by combining securities lending data with information from related asset classes."
        self.approach: str = "Look for confirmation of negative sentiment across a company's equity, bond, and credit derivatives markets."
        self.methodology: str = "Build powerful composite indicators by combining multiple, partially-correlated signals. For example, averaging the percentile ranks of Equity Utilization, Bond Utilization, and 5-year CDS spreads."
        self.economic_rationale: str = "When negative signals appear simultaneously across asset classes, it represents a high-conviction, consensus view of distress among sophisticated investors, filtering out noise and isolating a stronger signal of fundamental deterioration."
        self.client_value: str = "Provides a more robust and holistic perspective on investor sentiment, offering a more reliable and less noisy indicator for enhancing long-term investment and risk management strategies."

    def summarize(self):
        """Prints a formatted summary of the model's attributes."""
        print(f"Model: Cross-Asset Sentiment Aggregation")
        print(f"Objective: {self.objective}")
        print(f"Approach: {self.approach}")
        print(f"Methodology: {self.methodology}")
        print(f"Economic Rationale: {self.economic_rationale}")
        print(f"Client Value: {self.client_value}\n")

if __name__ == '__main__':
    # Example of how to instantiate and use the classes
    thematic_model = ThematicAndSectorDeepDives()
    thematic_model.summarize()

    events_model = CorporateAndMarketEventsAnalysis()
    events_model.summarize()

    squeeze_model = EnhancedShortSqueezePrediction()
    squeeze_model.summarize()

    cost_model = CostOfBorrowAsSentimentIndicator()
    cost_model.summarize()

    cross_asset_model = CrossAssetSentimentAggregation()
    cross_asset_model.summarize()
