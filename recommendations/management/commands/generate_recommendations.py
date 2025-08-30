import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import json

#for PyTorch 
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# It's good practice to have the helper function outside the class
def get_image_embedding(image_path, model, preprocess):
    """
    Takes an image file path, a PyTorch model, and a preprocessing pipeline.
    Returns a feature vector (embedding) for the image.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_t = preprocess(img)
        batch_t = torch.unsqueeze(img_t, 0)
        with torch.no_grad():
            embedding = model(batch_t)
        return embedding.numpy().flatten()
    except Exception as e:
        print(f"Warning: Could not process image {image_path}. Error: {e}")
        return None


class Command(BaseCommand):
    help = 'Generates both content-based and visual product recommendations'

    def handle(self, *args, **options):
        # ===================================================================
        # PART 1: CONTENT-BASED RECOMMENDATIONS (Your existing, working code)
        # ===================================================================
        self.stdout.write("Starting content-based recommendation generation...")
        
        all_products = Product.objects.all()
        products = [p for p in all_products if p.is_available]

        if len(products) < 2:
            self.stdout.write(self.style.WARNING("Not enough products to generate content recommendations."))
            # We don't return here, so the visual part can still run
        else:
            product_data = {
                'id': [p.id for p in products],
                'description': [p.description for p in products]
            }
            df = pd.DataFrame(product_data)
            tfidf = TfidfVectorizer(stop_words='english')
            df['description'] = df['description'].fillna('')
            tfidf_matrix = tfidf.fit_transform(df['description'])
            cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
            
            recommendations = {}
            indices = pd.Series(df.index, index=df['id']).drop_duplicates()

            for product_id in df['id']:
                idx = indices[product_id]
                sim_scores = list(enumerate(cosine_sim[idx]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = sim_scores[1:5]
                product_indices = [i[0] for i in sim_scores]
                recommended_ids = df['id'].iloc[product_indices].tolist()
                recommendations[str(product_id)] = recommended_ids
            
            with open('recommendations.json', 'w') as f:
                json.dump(recommendations, f)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully generated content-based recommendations for {len(products)} products.'))
        
        self.stdout.write('---') # Separator
        
        # ===================================================================
        # PART 2: VISUAL RECOMMENDATIONS (The new code)
        # ===================================================================
        self.stdout.write("Starting visual recommendation generation...")

        products_with_images = [p for p in products if p.image]

        if len(products_with_images) < 2:
            self.stdout.write(self.style.WARNING("Not enough products with images to generate visual recommendations."))
            return

        # 1. Load a pre-trained ResNet-50 model
        model = models.resnet50(pretrained=True)
        # Remove the final classification layer to get the feature vector
        model = torch.nn.Sequential(*(list(model.children())[:-1]))
        model.eval()

        # 2. Define the image preprocessing pipeline
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        # 3. Generate an embedding for each product image
        embeddings = []
        product_ids_with_images = []
        for product in products_with_images:
            embedding = get_image_embedding(product.image.path, model, preprocess)
            if embedding is not None:
                embeddings.append(embedding)
                product_ids_with_images.append(product.id)

        if not embeddings:
            self.stdout.write(self.style.ERROR("Could not generate any image embeddings."))
            return

        # 4. Compute the cosine similarity between all image embeddings
        cosine_sim_visual = cosine_similarity(np.array(embeddings))

        # 5. Build the recommendations dictionary
        visual_recommendations = {}
        df_visual = pd.DataFrame({'id': product_ids_with_images})
        indices_visual = pd.Series(df_visual.index, index=df_visual['id'])

        for prod_id in df_visual['id']:
            idx = indices_visual[prod_id]
            sim_scores = list(enumerate(cosine_sim_visual[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:5]
            product_indices = [i[0] for i in sim_scores]
            recommended_ids = df_visual['id'].iloc[product_indices].tolist()
            visual_recommendations[str(prod_id)] = recommended_ids

        # 6. Save the results to a NEW file
        with open('visual_recommendations.json', 'w') as f:
            json.dump(visual_recommendations, f)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully generated visual recommendations for {len(products_with_images)} products.'))