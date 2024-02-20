# Learning resources

- [Deeplearning AI](https://www.deeplearning.ai/courses/)
- [Pytorch book](https://www.learnpytorch.io/)
    - [transformer explained](https://jalammar.github.io/illustrated-transformer/)
    - [NN explanation](https://playground.tensorflow.org/#activation=tanh&batchSize=10&dataset=circle&regDataset=reg-plane&learningRate=0.03&regularizationRate=0&noise=0&networkShape=4,2&seed=0.33975&showTestData=false&discretize=false&percTrainData=50&x=true&y=true&xTimesY=false&xSquared=false&ySquared=false&cosX=false&sinX=false&cosY=false&sinY=false&collectStats=false&problem=classification&initZero=false&hideText=false)
    - [CNN explainer](https://poloclub.github.io/cnn-explainer/)
    - [Github source code](https://github.com/mrdbourke/pytorch-deep-learning)
- [PyTorch for Deep Learning Bootcamp](https://www.udemy.com/course/pytorch-for-deep-learning/)
- [Pytorch popular transfomers](https://pytorch.org/hub/huggingface_pytorch-transformers/)
    - [AlexNet](https://pytorch.org/hub/pytorch_vision_alexnet/)
    - [ResNet](https://pytorch.org/hub/nvidia_deeplearningexamples_resnet50/)
- [OCR for Latex](https://snip.mathpix.com/)

## information
- [twitter for new papers](https://twitter.com/_akhaliq)
- [papers with code](https://paperswithcode.com/)

# Zero to Mastery Learn PyTorch for Deep Learning

## Pytorch model

PyTorch 4 most import modules:  `[torch.nn](https://pytorch.org/docs/stable/nn.html)`, `[torch.optim](https://pytorch.org/docs/stable/optim.html)`, `[torch.utils.data.Dataset](https://pytorch.org/docs/stable/data.html#torch.utils.data.Dataset)` and `[torch.utils.data.DataLoader](https://pytorch.org/docs/stable/data.html)`.

![Untitled](imgs/Pytorch%20Udemy%20Learning%20c1a27db215b44a018cf303392d263729/Untitled.png)

## Pytorch training loops

![Untitled](imgs/Pytorch%20Udemy%20Learning%20c1a27db215b44a018cf303392d263729/Untitled%201.png)

1. **Forward pass** - The model goes through all of the training data once, performing its `forward()` function calculations (`model(x_train)`).
2. **Calculate the loss** - The model's outputs (predictions) are compared to the ground truth and evaluated to see how wrong they are (`loss = loss_fn(y_pred, y_train`).
3. **Zero gradients** - The optimizers gradients are set to zero (they are accumulated by default) so they can be recalculated for the specific training step (`optimizer.zero_grad()`).
4. **Perform backpropagation on the loss** - Computes the gradient of the loss with respect for every model parameter to be updated (each parameter with `requires_grad=True`). This is known as **backpropagation**, hence "backwards" (`loss.backward()`).
5. **Step the optimizer (gradient descent)** - Update the parameters with `requires_grad=True` with respect to the loss gradients in order to improve them (`optimizer.step()`).

## Pytorch layers

```markdown
- Common Layer Types
    - Linear Layers
    - Convolutional Layers
    - Recurrent Layers
    - Transformers
```

## Pytorch datasets

build custom datasets

1. Subclass `torch.utils.data.Dataset`.
2. Initialize our subclass with a `targ_dir` parameter (the target data directory) and `transform` parameter (so we have the option to transform our data if needed).
3. Create several attributes for `paths` (the paths of our target images), `transform` (the transforms we might like to use, this can be `None`), `classes` and `class_to_idx` (from our `find_classes()` function).
4. Create a function to load images from file and return them, this could be using `PIL` or `[torchvision.io](https://pytorch.org/vision/stable/io.html#image)` (for input/output of vision data).
5. Overwrite the `__len__` method of `torch.utils.data.Dataset` to return the number of samples in the `Dataset`, this is recommended but not required. This is so you can call `len(Dataset)`.
6. Overwrite the `__getitem__` method of `torch.utils.data.Dataset` to return a single sample from the `Dataset`, this is required.

## CNN

[https://poloclub.github.io/cnn-explainer/](imgs/https://poloclub.github.io/cnn-explainer/)

![Untitled](imgs/Pytorch%20Udemy%20Learning%20c1a27db215b44a018cf303392d263729/Untitled%202.png)

## Pytorch Modular

![Untitled](imgs/Pytorch%20Udemy%20Learning%20c1a27db215b44a018cf303392d263729/Untitled%203.png)

`from torchinfo import summary` 

![Untitled](imgs/Pytorch%20Udemy%20Learning%20c1a27db215b44a018cf303392d263729/Untitled%204.png)

## Pytorch transfer learning

**Freezing the base model and changing the output layer**

```python
weights = torchvision.models.EfficientNet_B0_Weights.DEFAULT # .DEFAULT = best available weights 
model = torchvision.models.efficientnet_b0(weights=weights).to(device)
# Freeze all base layers in the "features" section of the model (the feature extractor) by setting requires_grad=False
for param in model.features.parameters():
    param.requires_grad = Falsec
# Get the length of class_names (one output unit for each class)
output_shape = len(class_names)
# Recreate the classifier layer and seed it to the target device
model.classifier = torch.nn.Sequential(
    torch.nn.Dropout(p=0.2, inplace=True), 
    torch.nn.Linear(in_features=1280, 
                    out_features=output_shape, # same number of output units as our number of classes
                    bias=True)).to(device)
```