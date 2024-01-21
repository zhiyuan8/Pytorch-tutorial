from modular import data_setup, engine, model_builder, train, utils

"""
data_setup.py - a file to prepare and download data if needed.
engine.py - a file containing various training functions.
model_builder.py or model.py - a file to create a PyTorch model.
train.py - a file to leverage all other files and train a target PyTorch model.
utils.py - a file dedicated to helpful utility functions.
"""

# Create train/test dataloader and get class names as a list
train_dataloader, test_dataloader, class_names = data_setup.create_dataloaders("data/pizza_steak_sushi")

