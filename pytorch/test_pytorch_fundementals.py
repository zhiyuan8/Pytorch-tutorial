import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# scalar
scaler = torch.tensor(7)
# tensor back to int
print("scaler.ndim: ", scaler.ndim)
res = scaler.item()
print("integer: ", res)

# vector
vector = torch.tensor([7, 7])
print("vector.ndim: ", vector.ndim)
print("vector.shape: ", vector.shape)

# matrix
mat = torch.tensor([[7, 8], [9, 10]])
print("mat.ndim: ", mat.ndim)
print("mat.shape: ", mat.shape)
print("mat[0]: ", mat[0])

# tensor
tensor = torch.tensor([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print("tensor.ndim: ", tensor.ndim)
print("tensor.shape: ", tensor.shape)
print("tensor[0]: ", tensor[0])
print("tensor[0][0]: ", tensor[0][0])

# random tensor
random_tensor = torch.rand(3, 2)  # matrix
print("random_tensor: ", random_tensor)
random_tensor = torch.rand(2, 3, 4)  # tensor
print("random_tensor: ", random_tensor)

# zeros and ones
zeros = torch.zeros(3, 2)
print("zero: ", zeros)
ones = torch.ones(3, 2)
print("one: ", ones)
print("ones.dtype: ", ones.dtype)

# range
range_tensor = torch.arange(start=0, end=10, step=1)
print("range_tensor: ", range_tensor)

# tensor datatypes
float_32_tensor = torch.tensor(
    [1.0, 2.0, 3.0], dtype=torch.float32
)  # default is float 32
float_16_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float16)
long_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.long)  # tensor([1, 2, 3])
print("long_tensor: ", long_tensor)

# Manipulating tensors (tensor operations)
"""
addition, subtraction, multiplication, division 
"""
ts = torch.tensor([1, 2, 3])
print("multiple by 10: ", torch.multiply(ts, 10))
print("add by 10: ", torch.add(ts, 10))

# element-wise multiplication
print("element-wise multiplication: ", ts * ts)  # tensor([1, 4, 9])
print("matrix multiplication: ", torch.matmul(ts, ts))  # tensor(14)
print("matrix multiplication: ", ts @ ts)  # tensor(14)

# tensor aggregation (find min, max, mean, sum)
print("min: ", ts.min())
print("max: ", ts.max())
print("mean: ", ts.type(torch.float32).mean() )  # Input dtype must be either a floating point or complex dtype. Got: Long
print("sum: ", ts.sum())
print("argmax: ", ts.argmax())

# reshape & view & stack,squeeze,unsqueeze,permute
x = torch.arange(0, 9)
x_reshaped = x.reshape(3, 3)
print("x_reshaped: ", x_reshaped)

# The view method in PyTorch is used to reshape a tensor without changing its data. 
# It returns a new tensor with the same data as the original tensor but with a different shape. 
z = x.view(3, 3)
print("z: ", z)

x_stacked = torch.stack([x, x, x, x, x])
print("x_stacked: ", x_stacked)

# Returns a tensor with all specified dimensions of input of size 1 removed.
z = torch.zeros(2, 1, 2, 1, 2)
y = torch.squeeze(z)
print(y.shape)  # torch.Size([2, 2, 2])


