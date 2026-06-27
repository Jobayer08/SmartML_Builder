import os
import joblib
import numpy as np
from PIL import Image

import torch
from torchvision import models, transforms
from torchvision.models import ResNet18_Weights
from mlops.versioning import get_versioned_model_path, register_model

from sklearn.ensemble import RandomForestClassifier


MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

cnn = models.resnet18(weights=ResNet18_Weights.DEFAULT)
cnn.fc = torch.nn.Identity()
cnn.eval()


def extract_features(img_path):
    try:
        img = Image.open(img_path).convert("RGB")
        img = transform(img).unsqueeze(0)

        with torch.no_grad():
            feat = cnn(img)

        return feat.squeeze().cpu().numpy().astype(np.float32)

    except:
        return None



def detect_image_dataset_type(dataset_path):
    subfolders = [
        f for f in os.listdir(dataset_path)
        if os.path.isdir(os.path.join(dataset_path, f))
    ]
    return "labeled" if len(subfolders) > 0 else "unlabeled"



def train_labeled_images(dataset_path, model_name="image_classifier", user_dir=None):

    X, y, classes = [], [], []

    
    def find_label_folders(start_path, depth=0, max_depth=5):
        
        if depth > max_depth:
            return None
        
        try:
            items = os.listdir(start_path)
        except:
            return None
        
        subfolders = [
            os.path.join(start_path, item)
            for item in items
            if os.path.isdir(os.path.join(start_path, item))
        ]
        
        if not subfolders:
            return None
        
        
        for folder in subfolders:
            try:
                image_files = [
                    f for f in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, f)) and 
                       f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))
                ]
                if image_files: 
                    return start_path
            except:
                pass
        
        
        for folder in subfolders:
            result = find_label_folders(folder, depth + 1, max_depth)
            if result is not None:
                return result
        
        
        return None
    
    
    search_path = find_label_folders(dataset_path)
    if search_path is None:
        search_path = dataset_path

    for label in os.listdir(search_path):

        label_path = os.path.join(search_path, label)
        if not os.path.isdir(label_path):
            continue

        classes.append(label)

        for img in os.listdir(label_path):
            img_path = os.path.join(label_path, img)
            feat = extract_features(img_path)

            if feat is not None:
                X.append(feat)
                y.append(label)

    if len(X) == 0:
        return {"error": "No valid images found"}

    X = np.array(X, dtype=np.float32)

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X, y)

    if user_dir:
        os.makedirs(user_dir, exist_ok=True)
        
        model_path, version = get_versioned_model_path(model_name, user_dir=user_dir)
    else:
        model_path, version = get_versioned_model_path(model_name)

    joblib.dump({
        "model": clf,
        "classes": classes
    }, model_path)

    register_model(
        model_name=model_name,
        model_type="image",
        version=version
    )

    return {
        "task": "image_classification",
        "classes": classes,
        "total_images": len(X),
        "model_saved": model_path,
        "version": version,
        "status": "Image classification model trained"
    }