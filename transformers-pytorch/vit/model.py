import torch
import torchvision
from torch import nn
import os
import matplotlib.pyplot as plt
from torchinfo import summary
## Replicating ViT : overview

# 1. Create a class which subclasses nn.Module
class PatchEmbedding(nn.Module):
    """Turns a 2D input image into a 1D sequence learnable embedding vector.

    Args:
        in_channels (int): Number of color channels for the input images. Defaults to 3.
        patch_size (int): Size of patches to convert input image into. Defaults to 16.
        embedding_dim (int): Size of embedding to turn image into. Defaults to 768.
    """

    # 2. Initialize the class with appropriate variables
    def __init__(
        self, in_channels: int = 3, patch_size: int = 16, embedding_dim: int = 768
    ):
        super().__init__()
        self.patch_size = patch_size
        self.in_channels = in_channels
        self.embedding_dim = embedding_dim

        # 3. Create a layer to turn an image into patches
        self.patcher = nn.Conv2d(
            in_channels=in_channels,
            out_channels=embedding_dim,
            kernel_size=patch_size,
            stride=patch_size,
            padding=0,
        )

        # 4. Create a layer to flatten the patch feature maps into a single dimension
        self.flatten = nn.Flatten(
            start_dim=2,  # only flatten the feature map dimensions into a single vector
            end_dim=3,
        )

    # 5. Define the forward method
    def forward(self, x):
        # Create assertion to check that inputs are the correct shape
        image_resolution = x.shape[-1]
        assert (
            image_resolution % self.patch_size == 0
        ), f"Input image size must be divisble by patch size, image shape: {image_resolution}, patch size: {patch_size}"

        # Perform the forward pass
        x_patched = self.patcher(x)
        x_flattened = self.flatten(x_patched)
        # 6. Make sure the output shape has the right order
        return x_flattened.permute(
            0, 2, 1
        )  # adjust so the embedding is on the final dimension [batch_size, P^2•C, N] -> [batch_size, N, P^2•C]


"""
x_input = [class_token, image_patch_1, image_patch_2, ..., image_patch_n] + [class_token_pos, image_patch_1_pos, image_patch_2_pos, ..., image_patch_n_pos]
x_output_MSA_block = MSA_layer(LN_layer(x_input)) + x_input
x_output_MLP_block = MLP_layer(LN_layer(x_output_MSA_block)) + x_output_MSA_block
y_output = Linear_layer(LN_layer(x_output_MLP_block))

ViT-Base, ViT-Large, ViT-Huge
"""
class ViT(nn.Module):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    patchify = PatchEmbedding(in_channels=3, patch_size=16, embedding_dim=768)

    # Pass a single image through
    image_path = "../data/pizza_steak_sushi"
    train_dir = os.path.join(image_path, "train")
    test_dir = os.path.join(image_path, "test")
    # read image as PyTorch tensor
    image_np = plt.imread(os.path.join(train_dir, "pizza", "1008844.jpg"))
    # Convert the NumPy array to a PyTorch tensor and normalize to range [0, 1]
    image = (
        torch.tensor(image_np).permute(2, 0, 1).float() / 255.0
    )  # Rearrange the dimensions and convert to float
    print(f"Input image shape: {image.unsqueeze(0).shape}")
    patch_embedded_image = patchify(
        image.unsqueeze(0)
    )  # add an extra batch dimension on the 0th index, otherwise will error
    print(f"Output patch embedding shape: {patch_embedded_image.shape}")
    
    random_input_image = (1, 3, 224, 224)
    print(
        summary(PatchEmbedding(),
        input_size=random_input_image, # try swapping this for "random_input_image_error"
        col_names=["input_size", "output_size", "num_params", "trainable"],
        col_width=20,
        row_settings=["var_names"]))