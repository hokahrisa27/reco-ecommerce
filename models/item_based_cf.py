import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

df = pd.read_csv(r'C:\Users\ahmed\reco-ecommerce\data\events.csv')

weights = {'view':1, 'add_to_cart':3, 'purchase':5}
df['score'] = df['event'].map(weights)
df = df[df['score'].notna()]

user_item_scores = df.groupby(['visitorid', 'itemid'])['score'].sum().reset_index()

user_ids = user_item_scores['visitorid'].astype('category')
item_ids = user_item_scores['itemid'].astype('category')
user_item_scores['user_idx'] = user_ids.cat.codes
user_item_scores['item_idx'] = item_ids.cat.codes

mat_sparse = csr_matrix(
    (user_item_scores['score'], (user_item_scores['item_idx'], user_item_scores['user_idx']))
)

sim_matrix = cosine_similarity(mat_sparse, dense_output=False)


def recommend_similar_items(item_id, k=10):
    if item_id not in item_ids.cat.categories:
        return []
    idx = item_ids.cat.categories.get_loc(item_id)
    
    sim_row = sim_matrix.getrow(idx).toarray().flatten()

    sim_row[idx] = 0
    
    top_k_idx = sim_row.argsort()[::-1][:k]

    return item_ids.cat.categories[top_k_idx].tolist()


