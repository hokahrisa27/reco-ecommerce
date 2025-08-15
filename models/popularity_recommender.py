{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "42bda8ae",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[187946, 461686, 5411, 370653, 219512, 257040, 298009, 309778, 96924, 384302]\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "\n",
    "df = pd.read_csv(r'C:\\Users\\ahmed\\reco-ecommerce\\data\\events.csv')\n",
    "\n",
    "weights = {\n",
    "    'view': 1,\n",
    "    'add_to_cart': 3,\n",
    "    'transaction': 5\n",
    "}\n",
    "\n",
    "df['score'] = df['event'].map(weights)\n",
    "\n",
    "df = df[df['score'].notna()]\n",
    "\n",
    "item_popularity = df.groupby('itemid')['score'].sum()\n",
    "\n",
    "top_items = item_popularity.sort_values(ascending=False).index.tolist()\n",
    "\n",
    "def recommend_popular(user_id, k=10):\n",
    "    return top_items[:k]\n",
    "\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "env",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
