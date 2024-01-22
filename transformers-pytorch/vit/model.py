import torch
import torchvision
from torch import nn
## Replicating ViT : overview

class PatchEmbedding(nn.Module):
    def __init__(self, in_channels=3, patch_size=16, emb_size=768): # from ViT-base
        super().__init__()

    
    def forward(self, x):
        pass

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