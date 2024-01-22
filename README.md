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
- [OCR for Latex](https://snip.mathpix.com/)

## information
- [twitter for new papers](https://twitter.com/_akhaliq)
- [papers with code](https://paperswithcode.com/)

# Zero to Mastery Learn PyTorch for Deep Learning
- Common Layer Types
    - Linear Layers
    - Convolutional Layers
    - Recurrent Layers
    - Transformers

## CNN
[CNN explainer](https://poloclub.github.io/cnn-explainer/)  

### Vision Transformer (ViT)
Layers - takes an input, performs an operation or function on the input, produces an output.  
Blocks - a collection of layers, which in turn also takes an input and produces an output.

- Patch + Position Embedding (inputs)
- Linear projection of flattened patches (Embedded Patches)
- LayerNorm
- Multi-Headed Self-Attention
- MLP (or Multilayer perceptron)
- Transformer Encoder Block
- MLP Head (outputs)

```
x_input = [class_token, image_patch_1, image_patch_2, ..., image_patch_n] + [class_token_pos, image_patch_1_pos, image_patch_2_pos, ..., image_patch_n_pos]
x_output_MSA_block = MSA_layer(LN_layer(x_input)) + x_input
x_output_MLP_block = MLP_layer(LN_layer(x_output_MSA_block)) + x_output_MSA_block
y_output = Linear_layer(LN_layer(x_output_MLP_block))
```

## Modular
```
python modular/train.py --model MODEL_NAME --batch_size BATCH_SIZE --lr LEARNING_RATE --num_epochs NUM_EPOCHS
```
File structure :
```
data_setup.py - a file to prepare and download data if needed.
engine.py - a file containing various training functions.
model_builder.py or model.py - a file to create a PyTorch model.
train.py - a file to leverage all other files and train a target PyTorch model.
utils.py - a file dedicated to helpful utility functions.
```

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

