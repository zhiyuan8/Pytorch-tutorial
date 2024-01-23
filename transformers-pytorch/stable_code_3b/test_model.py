import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# The model is a decoder-only transformer similar to the LLaMA (Touvron et al., 2023) 

tokenizer = AutoTokenizer.from_pretrained(
    "stabilityai/stable-code-3b", trust_remote_code=True
)
model = AutoModelForCausalLM.from_pretrained(
    "stabilityai/stable-code-3b",
    trust_remote_code=True,
    torch_dtype="auto",
    attn_implementation="flash_attention_2",
)
model.cuda()
inputs = tokenizer("import torch\nimport torch.nn as nn", return_tensors="pt").to(
    model.device
)
tokens = model.generate(
    **inputs,
    max_new_tokens=48,
    temperature=0.2,
    do_sample=True,
)
print(tokenizer.decode(tokens[0], skip_special_tokens=True))
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
import torchvision
from torchvision import datasets
"""