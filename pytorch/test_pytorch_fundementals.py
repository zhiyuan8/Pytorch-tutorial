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
random_tensor = torch.rand(3, 2) # matrix
print("random_tensor: ", random_tensor)
random_tensor = torch.rand(2, 3, 4) # tensor
print("random_tensor: ", random_tensor)

# zeros and ones
zeros = torch.zeros(3, 2)
print("zero: ", zeros)
ones = torch.ones(3, 2)
print("one: ", ones)
print("ones.dtype: ", ones.dtype)


