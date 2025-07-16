import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def score_wallets(json_path, output_csv="wallet_scores.csv"):
    # Load JSON
    with open(json_path, 'r') as f:
        data = json.load(f)
    df = pd.json_normalize(data)

    # Rename for clarity
    df.rename(columns={
        'actionData.amount': 'amount',
        'actionData.assetPriceUSD': 'asset_price_usd',
        'actionData.assetSymbol': 'asset_symbol',
        'createdAt.$date': 'created_at',
        'updatedAt.$date': 'updated_at'
    }, inplace=True)

    # Convert types
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['asset_price_usd'] = pd.to_numeric(df['asset_price_usd'], errors='coerce')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
    df['amount_usd'] = df['amount'] * df['asset_price_usd']

    # Aggregate per wallet
    stats = df.groupby('userWallet').agg(
        num_transactions=('action', 'count'),
        num_deposits=('action', lambda x: (x == 'deposit').sum()),
        num_borrows=('action', lambda x: (x == 'borrow').sum()),
        num_redeems=('action', lambda x: (x == 'redeemunderlying').sum()),
        num_repays=('action', lambda x: (x == 'repay').sum()),
        num_liquidations=('action', lambda x: (x == 'liquidationcall').sum()),
        total_amount_usd=('amount_usd', 'sum'),
        avg_amount_usd=('amount_usd', 'mean'),
        first_tx=('timestamp', 'min'),
        last_tx=('timestamp', 'max')
    ).reset_index()

    # Add behavioral features
    stats['active_days'] = (stats['last_tx'] - stats['first_tx']).dt.days
    stats['borrow_ratio'] = stats['num_borrows'] / stats['num_transactions']
    stats['repay_ratio'] = stats['num_repays'] / stats['num_borrows'].replace(0, 1)
    stats['redeem_ratio'] = stats['num_redeems'] / stats['num_deposits'].replace(0, 1)
    stats['liquidation_flag'] = (stats['num_liquidations'] > 0).astype(int)
    stats.fillna(0, inplace=True)

    # Normalize and score
    scaler = MinMaxScaler()
    features = stats[[
        'num_transactions',
        'total_amount_usd',
        'active_days',
        'repay_ratio',
        'redeem_ratio',
        'borrow_ratio',
        'liquidation_flag'
    ]]
    scaled = scaler.fit_transform(features)
    weights = np.array([0.15, 0.15, 0.1, 0.2, 0.1, 0.1, -0.2])
    scores = np.dot(scaled, weights)
    stats['credit_score'] = np.clip((scores - scores.min()) / (scores.max() - scores.min()) * 1000, 0, 1000).round()

    # Save to CSV
    stats[['userWallet', 'credit_score']].to_csv(output_csv, index=False)
    print(f"[✓] Saved {len(stats)} wallet scores to {output_csv}")

# Example usage:
# score_wallets("user_transactions.json")
if __name__ == "__main__":
    score_wallets("user_transactions.json", output_csv="wallet_scores.csv")
