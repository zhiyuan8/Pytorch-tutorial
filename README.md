# Learning resources
- [Deeplearning AI](https://www.deeplearning.ai/courses/)
- [Pytorch book](https://www.learnpytorch.io/)
    - [NN explanation](https://playground.tensorflow.org/#activation=tanh&batchSize=10&dataset=circle&regDataset=reg-plane&learningRate=0.03&regularizationRate=0&noise=0&networkShape=4,2&seed=0.33975&showTestData=false&discretize=false&percTrainData=50&x=true&y=true&xTimesY=false&xSquared=false&ySquared=false&cosX=false&sinX=false&cosY=false&sinY=false&collectStats=false&problem=classification&initZero=false&hideText=false)
    - [CNN explainer](https://poloclub.github.io/cnn-explainer/)
    - [Github source code](https://github.com/mrdbourke/pytorch-deep-learning)
- [PyTorch for Deep Learning Bootcamp](https://www.udemy.com/course/pytorch-for-deep-learning/)
- [Pytorch popular transfomers](https://pytorch.org/hub/huggingface_pytorch-transformers/)
- [Pytorch AlexNet](https://pytorch.org/hub/pytorch_vision_alexnet/)
- [ResNet](https://pytorch.org/hub/nvidia_deeplearningexamples_resnet50/)

# Zero to Mastery Learn PyTorch for Deep Learning

## CNN
[CNN explainer](https://poloclub.github.io/cnn-explainer/)  
- CNN layers
    - Input Layer
    - Convolutional Layers
    - Pooling Layers
    - Fully Connected Layers

## Modular



## Pytorch highlights

1. DataLoader
```
from torch.utils.data import DataLoader

train_dataloader = DataLoader(train_data, # dataset to turn into iterable
    batch_size=BATCH_SIZE, # how many samples per batch? 
    shuffle=True # shuffle data every epoch?
)
train_features_batch, train_labels_batch = next(iter(train_dataloader))
```

