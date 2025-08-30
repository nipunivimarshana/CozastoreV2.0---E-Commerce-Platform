import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import json

class Command(BaseCommand):
    help = 'Generates product recommendations based on content similarity'

    def handle(self, *args, **options):
        self.stdout.write("Fetching all available products...")
        
        # We can use the safe, Python-based filter here too
        all_products = Product.objects.all()
        products = [p for p in all_products if p.is_available]

        if len(products) < 2:
            self.stdout.write(self.style.WARNING("Not enough products to generate recommendations."))
            return

        # Create a pandas DataFrame for easier data manipulation
        product_data = {
            'id': [p.id for p in products],
            'description': [p.description for p in products]
        }
        df = pd.DataFrame(product_data)

        # --- THIS IS THE REAL SCIKIT-LEARN INTEGRATION ---
        
        # 1. Initialize the TF-IDF Vectorizer. This object turns text into numbers.
        #    `stop_words='english'` removes common words like "the", "a", "is".
        tfidf = TfidfVectorizer(stop_words='english')
        
        # Replace any empty descriptions with an empty string to avoid errors
        df['description'] = df['description'].fillna('')
        
        # 2. Create the TF-IDF matrix by analyzing all descriptions.
        tfidf_matrix = tfidf.fit_transform(df['description'])
        
        # 3. Compute the cosine similarity matrix. This creates a giant table where
        #    every product is compared to every other product based on its description.
        #    The value will be 1.0 for identical descriptions and 0.0 for completely different ones.
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        
        # --- END OF INTEGRATION ---

        # Now, build the final recommendations dictionary from the similarity matrix
        recommendations = {}
        indices = pd.Series(df.index, index=df['id']).drop_duplicates()

        for product_id in df['id']:
            idx = indices[product_id]
            # Get the similarity scores of all products with this one
            sim_scores = list(enumerate(cosine_sim[idx]))
            # Sort the products based on the similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            # Get the scores of the top 4 most similar products (index 0 is the product itself)
            sim_scores = sim_scores[1:5]
            # Get the indices of those products
            product_indices = [i[0] for i in sim_scores]
            # Get the actual IDs of those products
            recommended_ids = df['id'].iloc[product_indices].tolist()
            recommendations[str(product_id)] = recommended_ids
        
        # Save the new, intelligent recommendations to the file
        with open('recommendations.json', 'w') as f:
            json.dump(recommendations, f)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully generated content-based recommendations for {len(products)} products.'))
        