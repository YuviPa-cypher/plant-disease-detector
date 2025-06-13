import os
import shutil
from sklearn.model_selection import train_test_split

# Paths
source_dir = 'raw_dataset/PlantVillage'
train_dir = 'dataset/train'
test_dir = 'dataset/test'

# 80% train, 20% test
split_ratio = 0.8

# Create destination folders if not exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Loop through each class (folder)
for class_name in os.listdir(source_dir):
    class_path = os.path.join(source_dir, class_name)
    if not os.path.isdir(class_path):
        continue

    images = os.listdir(class_path)
    train_imgs, test_imgs = train_test_split(images, train_size=split_ratio, random_state=42)

    # Create class folders in train/test dirs
    os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
    os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)

    # Copy training images
    for img in train_imgs:
        src = os.path.join(class_path, img)
        dst = os.path.join(train_dir, class_name, img)
        shutil.copy(src, dst)

    # Copy testing images
    for img in test_imgs:
        src = os.path.join(class_path, img)
        dst = os.path.join(test_dir, class_name, img)
        shutil.copy(src, dst)

print("✅ Dataset split into training and testing folders.")

