import os
import pickle
from functools import lru_cache

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

@lru_cache(maxsize=1)
def load_bundle():
    pkl_path = os.path.join(settings.BASE_DIR, 'recommender', 'ml', 'bundle.pkl')

    if not os.path.exists(pkl_path):
        raise ImproperlyConfigured(f"Bundle file not found at {pkl_path}")
    
    with open(pkl_path, 'rb') as f:
        bundle = pickle.load(f)

    assert "model" in bundle and "feature_cols" in  bundle, "Bundle must contain 'model' and 'feature_cols' keys."
    return bundle

def predict_crop(feature_dict):
    bundle = load_bundle()
    model = bundle['model']
    order = bundle['feature_cols']

    X = [[float(feature_dict[c]) for c in order]]
    pred = model.predict(X)

    return pred[0]
