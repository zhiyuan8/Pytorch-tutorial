# Learning resources
- [Deeplearning AI](https://www.deeplearning.ai/courses/)
- [Pytorch book](https://www.learnpytorch.io/)
- [PyTorch for Deep Learning Bootcamp](https://www.udemy.com/course/pytorch-for-deep-learning/)
- [Pytorch popular transfomers](https://pytorch.org/hub/huggingface_pytorch-transformers/)
- [Pytorch AlexNet](https://pytorch.org/hub/pytorch_vision_alexnet/)
- [ResNet](https://pytorch.org/hub/nvidia_deeplearningexamples_resnet50/)

# Zero to Mastery Learn PyTorch for Deep Learning
- Examples at [Pytorch book](https://www.learnpytorch.io/)  
    1. [CNN]

1. DataLoader
```
from torch.utils.data import DataLoader

train_dataloader = DataLoader(train_data, # dataset to turn into iterable
    batch_size=BATCH_SIZE, # how many samples per batch? 
    shuffle=True # shuffle data every epoch?
)
train_features_batch, train_labels_batch = next(iter(train_dataloader))
```

