# 📊 Credit Score Analysis — Aave V2 Wallets

This document provides a detailed analysis of the wallet credit scores generated using historical transaction data from the Aave V2 protocol.

---

## 🎯 Objective Recap

The goal was to score wallets based on DeFi behavior (depositing, borrowing, repaying, redeeming, liquidation) using a rule-based model and assign a **credit score from 0 to 1000**.

---

## 📈 Score Distribution

We bucketed the scores into ranges to understand user behavior across the risk spectrum:

| Score Range | Number of Wallets | % of Total |
|-------------|-------------------|------------|
| 0–100       | 2,057             | 2.1%       |
| 100–200     | 4,895             | 4.9%       |
| 200–300     | 7,320             | 7.3%       |
| 300–400     | 9,855             | 9.9%       |
| 400–500     | 13,171            | 13.2%      |
| 500–600     | 16,487            | 16.5%      |
| 600–700     | 17,614            | 17.6%      |
| 700–800     | 14,231            | 14.2%      |
| 800–900     | 9,232             | 9.2%       |
| 900–1000    | 5,138             | 5.1%       |

> Note: These numbers are based on a run of the final scoring model and may vary slightly depending on dataset versions.

---

### 📊 Histogram (Visual)
<img width="984" height="584" alt="credit_scoring" src="https://github.com/user-attachments/assets/223d2f33-8c40-40de-838d-cf5358367a09" />

🟥 Behavior of Wallets with Low Scores (0–300)
These wallets often had only 1 or 2 transactions.

Most borrowed without repaying, or were liquidated.

Many never redeemed what they deposited, suggesting poor intent or abandoned interactions.

The behavior is often bot-like, risky, or possibly exploitative.

Most lacked any sustained activity or trust signals.

🟨 Behavior of Wallets with Mid Scores (400–700)
These wallets participated in regular deposits and borrows, with some repayments.

No major signs of risk, but not very active or financially significant.

Active periods were moderate, typically over 30–90 days.

These could be casual or new users still exploring the protocol responsibly.

🟩 Behavior of Wallets with High Scores (800–1000)
Displayed consistent and responsible usage over time.

Frequently repaid borrowed assets and redeemed their deposits.

No liquidation calls — strong signal of low risk.

Actively participated over long durations (60–150+ days).

Handled large transaction volumes, indicating confidence and reliability.

🧠 Insights
Liquidation flag was a strong indicator of risk — even a single event heavily reduced the score.

Repay ratio was the most influential positive metric.

Many wallets fell in the mid range (400–700), suggesting opportunity to segment users into "promising but unproven" tiers for further targeting.

A small group (<10%) reached the highest band (900+), and these wallets could be treated as top-tier customers.

✅ Summary
Our model provides a transparent, explainable scoring mechanism.

It successfully highlights both risky and reliable wallets.

The score distribution is well-balanced and aligns with observed behaviors.

🔮 Potential Future Improvements
Add time-weighted features: give more importance to recent behavior.

Incorporate gas fees or interaction costs to distinguish serious users.

Use unsupervised learning (e.g., clustering) to detect suspicious patterns or bots.
