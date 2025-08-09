import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



events = pd.read_csv(r"C:/Users/ahmed/reco-ecommerce/data/events.csv")
cat_tree = pd.read_csv(r"C:/Users/ahmed/reco-ecommerce/data/category_tree.csv")
prop1 = pd.read_csv(r"C:/Users/ahmed/reco-ecommerce/data/item_properties_part1.csv")
prop2 = pd.read_csv(r"C:/Users/ahmed/reco-ecommerce/data/item_properties_part2.csv")

props = pd.concat([prop1, prop2], ignore_index=True)

events['datetime'] = pd.to_datetime(events['timestamp'], unit='ms')
props['datetime'] = pd.to_datetime(props['timestamp'], unit='ms')

cat_props = props[props['property'] == 'categoryid'][['itemid', 'value']].drop_duplicates()
cat_props.rename(columns={'value': 'categoryid'}, inplace=True)

cat_props['categoryid'] = cat_props['categoryid'].astype(int)
cat_tree['categoryid'] = cat_tree['categoryid'].astype(int)
events['itemid'] = events['itemid'].astype(int)
cat_props['itemid'] = cat_props['itemid'].astype(int)

events = events.merge(cat_props, on='itemid', how='left')

events = events.merge(cat_tree, on='categoryid', how='left')

print(events.head())

print(f"Nombre d'utilisateurs uniques : {events['visitorid'].nunique()}")
print(f"Nombre d'items uniques : {events['itemid'].nunique()}")
print(f"Nombre total d'interactions : {len(events)}")

density = len(events) / (events['visitorid'].nunique() * events['itemid'].nunique())
print(f"Densité de la matrice user-item : {density:.6f}")

interactions_per_user = events.groupby('visitorid').size()
print(interactions_per_user.describe())

interactions_per_item = events.groupby('itemid').size()
print(interactions_per_item.describe())

print(f"Nombre d'utilisateurs uniques : {events['visitorid'].nunique()}")
print(f"Nombre d'items uniques : {events['itemid'].nunique()}")
print(f"Nombre total d'interactions : {len(events)}")
density = len(events) / (events['visitorid'].nunique() * events['itemid'].nunique())
print(f"Densité matrice user-item : {density:.6f}")

interactions_per_user = events.groupby('visitorid').size()
print(interactions_per_user.describe())

interactions_per_item = events.groupby('itemid').size()
print(interactions_per_item.describe())

plt.figure(figsize=(12,5))
sns.histplot(interactions_per_user, bins=50, log_scale=True)
plt.title("Distribution des interactions par utilisateur (log scale)")
plt.xlabel("Nombre d'interactions")
plt.ylabel("Nombre d'utilisateurs")
plt.show()

plt.figure(figsize=(12,5))
sns.histplot(interactions_per_item, bins=50, log_scale=True)
plt.title("Distribution des interactions par item (log scale)")
plt.xlabel("Nombre d'interactions")
plt.ylabel("Nombre d'items")
plt.show()

events = events.sort_values('datetime')

first_month = events['datetime'].min() + pd.Timedelta(days=30)
new_users = events[events['datetime'] <= first_month]['visitorid'].nunique()
total_users = events['visitorid'].nunique()
cold_start_user_rate = new_users / total_users
print(f"Taux cold-start utilisateurs (premier mois): {cold_start_user_rate:.2%}")

new_items = events[events['datetime'] <= first_month]['itemid'].nunique()
total_items = events['itemid'].nunique()
cold_start_item_rate = new_items / total_items
print(f"Taux cold-start items (premier mois): {cold_start_item_rate:.2%}")


events['session_gap'] = events.groupby('visitorid')['datetime'].diff().dt.total_seconds() / 60
events['new_session'] = (events['session_gap'] > 30) | (events['session_gap'].isna())
events['session_id'] = events.groupby('visitorid')['new_session'].cumsum()

sessions_count = events.groupby('visitorid')['session_id'].nunique()
print(f"Sessions moyennes par utilisateur: {sessions_count.mean():.2f}")

purchase_events = events[events['event'] == 'transaction']
purchase_rate = len(purchase_events) / len(events)
print(f"Fréquence d'achat globale: {purchase_rate:.2%}")
