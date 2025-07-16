# Aave V2 DeFi Credit Scoring

This project assigns a credit score between 0 and 1000 to wallets interacting with the Aave V2 protocol, based on their historical transaction behavior. Higher scores indicate more trustworthy and responsible users, while lower scores suggest risky or potentially exploitative behavior.

---

## 📌 Problem Statement

Given 100K transaction-level records from Aave V2, the goal is to build a machine learning system that evaluates the historical activity of wallets and generates a credit score for each. The model must run in one step from a JSON file and generate interpretable results.

---

## 🧠 Approach

1. **Data Loading**: We load raw transaction data from `user_transactions.json`.
2. **Feature Engineering**: We extract wallet-level behavior metrics like transaction counts, borrow/repay ratios, total volume, and duration of activity.
3. **Risk Indicators**: Wallets are evaluated based on how often they borrow without repaying, how frequently they’re liquidated, and how long they’ve been active.
4. **Scoring**: Features are scaled and weighted to produce a final credit score on a scale of 0–1000.

---

## 🛠️ Technologies Used

- Python
- Pandas
- Scikit-learn (for feature scaling)
- NumPy

---

## 🧾 Features Used for Scoring

| Feature | Description |
|--------|-------------|
| `num_transactions` | Total number of transactions |
| `total_amount_usd` | Total volume transacted in USD |
| `active_days` | Days between first and last transaction |
| `borrow_ratio` | Proportion of borrow actions |
| `repay_ratio` | Repays divided by borrows (higher = good) |
| `redeem_ratio` | Redeems divided by deposits |
| `liquidation_flag` | 1 if liquidated at least once, else 0 |

All features are normalized and used in a weighted scoring formula.

---

## 📊 Scoring Formula

The final credit score is calculated using a weighted combination of normalized features:

```text
score = (0.15 * activity) + 
        (0.15 * amount) +
        (0.1 * active_days) +
        (0.2 * repay_ratio) +
        (0.1 * redeem_ratio) +
        (0.1 * borrow_ratio) -
        (0.2 * liquidation_flag)
This score is then scaled to fit the range 0–1000.

⚙️ How to Run
Make sure you have the required packages installed:

pip install pandas scikit-learn
Place the user_transactions.json file in the same folder.

Run the scoring script:

python score_wallets.py
Output will be saved as wallet_scores.csv containing:

userWallet,credit_score
0x123..., 734
0x456..., 901
...
