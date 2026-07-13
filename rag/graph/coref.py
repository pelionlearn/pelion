from fastcoref import FCoref

# Initialize the lightweight F-Coref model (GPU is supported if you add device='cuda:0')
model = FCoref(model_name_or_path="lingmess")

texts = ["Alice goes down the rabbit hole. There, she discovers a new reality."]

# Predict coreference clusters
preds = model.predict(texts=texts, use_fast=False)

# Get clusters
print(preds[0].get_clusters())

# Get text with resolved mentions (e.g., replaces "she" with "Alice")
print(preds[0].get_resolved_text())
