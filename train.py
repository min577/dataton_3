"""
AI Hub 한식 이미지 데이터셋으로 ResNet50 학습
Image Classification (not Object Detection)
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
from pathlib import Path
import json
from tqdm import tqdm
import numpy as np


class KoreanFoodDataset(Dataset):
    """한식 이미지 데이터셋"""
    
    def __init__(self, data_dir: str, transform=None, split='train'):
        """
        Args:
            data_dir: AI Hub 데이터 경로
                구조: data_dir/대분류/소분류/이미지들
            transform: 이미지 전처리
            split: 'train', 'val', 'test'
        """
        self.data_dir = Path(data_dir)
        self.transform = transform
        self.split = split
        
        # 클래스 매핑 생성
        self.class_to_idx = {}
        self.idx_to_class = {}
        self.images = []
        
        self._build_dataset()
    
    def _build_dataset(self):
        """데이터셋 구조 파싱"""
        class_idx = 0
        
        # 대분류 폴더 순회
        for major_category in sorted(self.data_dir.iterdir()):
            if not major_category.is_dir():
                continue
            
            # 소분류 폴더 순회 (150개)
            for sub_category in sorted(major_category.iterdir()):
                if not sub_category.is_dir():
                    continue
                
                # 클래스 매핑
                class_name = sub_category.name
                self.class_to_idx[class_name] = class_idx
                self.idx_to_class[class_idx] = class_name
                
                # 이미지 파일 수집
                image_files = list(sub_category.glob('*.jpg')) + \
                             list(sub_category.glob('*.png'))
                
                # Train/Val/Test 분할 (70/15/15)
                np.random.seed(42)
                np.random.shuffle(image_files)
                
                n_train = int(len(image_files) * 0.7)
                n_val = int(len(image_files) * 0.15)
                
                if self.split == 'train':
                    selected_images = image_files[:n_train]
                elif self.split == 'val':
                    selected_images = image_files[n_train:n_train+n_val]
                else:  # test
                    selected_images = image_files[n_train+n_val:]
                
                # 이미지 경로와 레이블 저장
                for img_path in selected_images:
                    self.images.append((img_path, class_idx))
                
                class_idx += 1
        
        print(f"{self.split} set: {len(self.images)} images, {class_idx} classes")
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path, label = self.images[idx]
        
        # 이미지 로드
        image = Image.open(img_path).convert('RGB')
        
        # 전처리
        if self.transform:
            image = self.transform(image)
        
        return image, label
    
    def save_class_mapping(self, save_path: str):
        """클래스 매핑 저장"""
        mapping = {
            'class_to_idx': self.class_to_idx,
            'idx_to_class': self.idx_to_class
        }
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)


class KoreanFoodClassifier(nn.Module):
    """한식 분류 모델 (ResNet50 기반)"""
    
    def __init__(self, num_classes=150, pretrained=True):
        super().__init__()
        
        # ResNet50 backbone
        self.backbone = models.resnet50(pretrained=pretrained)
        
        # 마지막 FC layer 교체
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(in_features, num_classes)
        )
    
    def forward(self, x):
        return self.backbone(x)


def train_model(data_dir: str, 
                output_dir: str,
                num_epochs: int = 30,
                batch_size: int = 32,
                learning_rate: float = 0.001):
    """
    모델 학습
    
    Args:
        data_dir: AI Hub 데이터 경로
        output_dir: 모델 저장 경로
        num_epochs: 학습 에포크 수
        batch_size: 배치 크기
        learning_rate: 학습률
    """
    
    # 디바이스 설정
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # 데이터 전처리
    train_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomCrop((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    # 데이터셋 로드
    train_dataset = KoreanFoodDataset(data_dir, transform=train_transform, split='train')
    val_dataset = KoreanFoodDataset(data_dir, transform=val_transform, split='val')
    
    # 클래스 매핑 저장
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    train_dataset.save_class_mapping(output_path / 'class_mapping.json')
    
    # 데이터로더
    train_loader = DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )
    
    # 모델 초기화
    num_classes = len(train_dataset.class_to_idx)
    model = KoreanFoodClassifier(num_classes=num_classes, pretrained=True)
    model = model.to(device)
    
    # Loss & Optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', patience=3, factor=0.5
    )
    
    # 학습
    best_val_acc = 0.0
    
    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch+1}/{num_epochs}")
        print("-" * 50)
        
        # Training phase
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for images, labels in tqdm(train_loader, desc="Training"):
            images = images.to(device)
            labels = labels.to(device)
            
            # Forward
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Backward
            loss.backward()
            optimizer.step()
            
            # Statistics
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            train_total += labels.size(0)
            train_correct += predicted.eq(labels).sum().item()
        
        train_acc = 100. * train_correct / train_total
        avg_train_loss = train_loss / len(train_loader)
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for images, labels in tqdm(val_loader, desc="Validation"):
                images = images.to(device)
                labels = labels.to(device)
                
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()
        
        val_acc = 100. * val_correct / val_total
        avg_val_loss = val_loss / len(val_loader)
        
        # Learning rate scheduling
        scheduler.step(val_acc)
        
        # 결과 출력
        print(f"Train Loss: {avg_train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        
        # Best model 저장
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'num_classes': num_classes
            }, output_path / 'best_model.pth')
            print(f"✅ Best model saved! Val Acc: {val_acc:.2f}%")
    
    print(f"\n🎉 Training completed! Best Val Acc: {best_val_acc:.2f}%")


def evaluate_model(model_path: str, 
                   data_dir: str,
                   class_mapping_path: str):
    """모델 평가"""
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 클래스 매핑 로드
    with open(class_mapping_path, 'r', encoding='utf-8') as f:
        class_mapping = json.load(f)
    
    num_classes = len(class_mapping['class_to_idx'])
    
    # 모델 로드
    model = KoreanFoodClassifier(num_classes=num_classes, pretrained=False)
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()
    
    # 테스트 데이터셋
    test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    test_dataset = KoreanFoodDataset(data_dir, transform=test_transform, split='test')
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    # 평가
    correct = 0
    total = 0
    top5_correct = 0
    
    with torch.no_grad():
        for images, labels in tqdm(test_loader, desc="Testing"):
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            
            # Top-1 accuracy
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            # Top-5 accuracy
            _, top5_pred = outputs.topk(5, 1, largest=True, sorted=True)
            top5_correct += sum([labels[i] in top5_pred[i] for i in range(len(labels))])
    
    top1_acc = 100. * correct / total
    top5_acc = 100. * top5_correct / total
    
    print(f"\n📊 Test Results:")
    print(f"Top-1 Accuracy: {top1_acc:.2f}%")
    print(f"Top-5 Accuracy: {top5_acc:.2f}%")


if __name__ == '__main__':
    # 학습 실행
    train_model(
        data_dir='/path/to/DATATON/korean_food',
        output_dir='./models',
        num_epochs=30,
        batch_size=32,
        learning_rate=0.001
    )
    
    # 평가 실행
    evaluate_model(
        model_path='./models/best_model.pth',
        data_dir='/path/to/DATATON/korean_food',
        class_mapping_path='./models/class_mapping.json'
    )