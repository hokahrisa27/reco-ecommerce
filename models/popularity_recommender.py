import pandas as pd

df = pd.read_csv(r'C:\Users\ahmed\reco-ecommerce\data\events.csv')

weights = {
    'view': 1,
    'add_to_cart': 3,
    'transaction': 5
}

df['score'] = df['event'].map(weights)

df = df[df['score'].notna()]

item_popularity = df.groupby('itemid')['score'].sum()

top_items = item_popularity.sort_values(ascending=False).index.tolist()

def recommend_popular(user_id, k=10):
    return top_items[:k]
