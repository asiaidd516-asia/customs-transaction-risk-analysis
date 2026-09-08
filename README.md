# Customs Transaction Risk Analysis

An explainable data analytics prototype for identifying potentially unusual customs transactions and prioritizing shipments for further audit review.

## Project Overview

Customs authorities process large volumes of import transactions, making it difficult to review every shipment in depth.

This project develops a transaction-level risk analysis approach that combines valuation and statistical indicators to identify unusual shipment patterns and classify transactions into Low, Medium, and High risk categories.

The objective is not to determine whether a shipment involves fraud or tax evasion, but to demonstrate how data analytics can support risk-based customs auditing by helping prioritize transactions for further review.

## Key Objectives

- Examine the quality and structure of customs transaction data.
- Identify valuation and statistical indicators associated with unusual transactions.
- Combine multiple indicators into an explainable weighted risk score.
- Classify shipments into Low, Medium, and High risk categories.
- Analyse risk patterns across commodities.
- Identify limitations and opportunities for extending the approach with real customs data.

## Dataset

The analysis uses the **China–Africa Trade Monitoring Dataset** obtained from Kaggle and filtered to transactions where Tanzania is the import country.

The dataset contains **1,458 shipment records** across:

- Agricultural
- Electronics
- Machinery
- Minerals
- Textiles

Key variables include:

- Declared shipment value
- Contract value
- Market price per unit
- Quantity
- Commodity

The dataset is historical third-party trade data and is **not sourced from TRA's internal TANCIS records**. Therefore, the results should be interpreted as a methodological prototype rather than an assessment of actual TRA transactions.

## Risk Indicators

The analysis uses four transaction-level indicators:

| Risk Indicator | Weight |
|---|---:|
| Contract deviation | 35 |
| Market outlier | 30 |
| Benford rare digit | 20 |
| Round-number bias | 15 |

The indicators are combined into a weighted risk score.

Higher scores indicate that a shipment triggered more risk indicators.

## Results

The analysis classified the 1,458 shipments as:

| Risk Category | Shipments | Percentage |
|---|---:|---:|
| Low | 1,186 | 81.3% |
| Medium | 262 | 18.0% |
| High | 10 | 0.7% |

The high-risk group consisted of:

- Agricultural: 4 shipments
- Electronics: 4 shipments
- Minerals: 2 shipments

The high-risk transactions were identified for further review based on combinations of the analytical indicators.

## Dashboard

An interactive Streamlit dashboard was developed to allow users to:

- View overall shipment risk distribution
- Explore risk indicators
- Filter transactions by commodity
- Filter transactions by risk category
- Examine high-risk transactions
- Download filtered transactions
- Review the methodology and limitations

### Live Dashboard

**[Open the Customs Risk Analysis Dashboard](https://customs-transaction-risk-analysis.streamlit.app/)**

## Technologies

- Python
- Pandas
- Matplotlib
- Streamlit
- Jupyter Notebook
- Git & GitHub

## Limitations

This prototype has several limitations:

- The dataset is public third-party data rather than TRA/TANCIS data.
- HS-code classification checks were excluded because reliable tariff information was not available for the analysis.
- Transport-route consistency checks were excluded because the available transport data contained unreliable values.
- Market-price analysis uses relative comparisons within commodity groups because of unit-scale limitations.
- Transaction dates were not available, preventing time-based analysis.
- Risk indicators are screening signals and should not be interpreted as proof of fraud or tax evasion.
- The risk weights are prototype assumptions and would require validation using real customs audit outcomes.

## Future Improvements

With access to appropriate real-world customs data, the system could be extended to include:

- Historical audit outcomes
- Reliable HS-code and tariff information
- Transaction-level time-series analysis
- More advanced anomaly detection
- Model validation using historical audit results
- Integration with customs risk-management systems

## Data Source

China–Africa Trade Monitoring Dataset, published on Kaggle by Ziya.

The source dataset is released under **CC0: Public Domain**.
## Author

**Asia Iddi Abdalah**

BSc Data Science and Artificial Intelligence  
Ardhi University, Tanzania
