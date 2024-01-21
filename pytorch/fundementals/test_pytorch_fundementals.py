import torch
import numpy as np

# 1. Basic Tensor Operations
def create_basic_tensors():
    # Scalar
    scaler = torch.tensor(7)
    print("Scalar to integer:", scaler.item())

    # Vector
    vector = torch.tensor([7, 7])
    print("Vector ndim:", vector.ndim)
    print("Vector shape:", vector.shape)

    # Matrix
    mat = torch.tensor([[7, 8], [9, 10]])
    print("Matrix ndim:", mat.ndim)
    print("Matrix shape:", mat.shape)

    # Tensor
    tensor = torch.tensor([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
    print("Tensor ndim:", tensor.ndim)
    print("Tensor shape:", tensor.shape)


# 2. Random Tensor Generation
def create_random_tensors():
    random_tensor = torch.rand(3, 2)  # matrix
    print("Random tensor (matrix):", random_tensor)
    random_tensor = torch.rand(2, 3, 4)  # tensor
    print("Random tensor (general):", random_tensor)


# 3. Zeros and Ones Tensor Creation
def create_zeros_ones_tensors():
    zeros = torch.zeros(3, 2)
    print("Zeros tensor:", zeros)
    ones = torch.ones(3, 2)
    print("Ones tensor:", ones)


# 4. Tensor Datatypes
def demonstrate_tensor_datatypes():
    float_32_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)
    float_16_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float16)
    long_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.long)
    print("Long tensor:", long_tensor)


# 5. Tensor Manipulations
def tensor_arithmetic_operations():
    ts = torch.tensor([1, 2, 3])
    print("Multiply by 10:", torch.multiply(ts, 10))
    print("Add 10:", torch.add(ts, 10))
    print("Element-wise multiplication:", ts * ts)
    print("Matrix multiplication:", ts @ ts)


# 6. Tensor Aggregation
def tensor_aggregation():
    ts = torch.tensor([1, 2, 3])
    print("Min:", ts.min())
    print("Max:", ts.max())
    print("Mean:", ts.type(torch.float32).mean())
    print("Sum:", ts.sum())
    print("Argmax:", ts.argmax())


# 7. Tensor Reshaping and Squeezing
def reshape_squeeze_tensors():
    x = torch.arange(0, 9)
    x_reshaped = x.reshape(3, 3)
    print("Reshaped x:", x_reshaped)
    z = x.view(3, 3)
    print("View of x:", z)
    x_stacked = torch.stack([x, x, x, x, x])
    print("Stacked x:", x_stacked)
    y = torch.squeeze(torch.zeros(2, 1, 2, 1, 2))
    print("Squeezed shape:", y.shape)


def tensor_datatypes():
    float_32_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)
    float_16_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float16)
    res = float_32_tensor * float_16_tensor
    print("Result:", res, " datatype:", res.dtype, " shape:", res.shape)


def manipulation_tensors_with_numpy():
    x = torch.arange(0, 9).reshape(1, 3, 3)
    print("x:", x, "x[0]:", x[0], "x[0][0]:", x[0][0], "x[0][0][0]:", x[0][0][0])
    print(x[:, 1:, 1:])
    array = np.array([1, 2, 3])
    
# putting tensors and models on the GPU
def tensor_on_gpu():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tensor = torch.tensor([1, 2, 3], device = device)
    print("Tensor device : ", tensor.device)
    
    
if __name__ == "__main__":
    # Running the functions
    # create_basic_tensors()
    # create_random_tensors()
    # create_zeros_ones_tensors()
    # demonstrate_tensor_datatypes()
    # tensor_arithmetic_operations()
    # tensor_aggregation()
    # reshape_squeeze_tensors()
    tensor_datatypes()
    tensor_on_gpu()