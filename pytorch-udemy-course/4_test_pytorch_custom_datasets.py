import torch
from torch import nn
import requests
import zipfile
from pathlib import Path
import os
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


def walk_through_dir(dir_path):
    """
    Walks through dir_path returning its contents.
    Args:
      dir_path (str or pathlib.Path): target directory

    Returns:
      A print out of:
        number of subdiretories in dir_path
        number of images (files) in each subdirectory
        name of each subdirectory
    """
    for dirpath, dirnames, filenames in os.walk(dir_path):
        print(
            f"There are {len(dirnames)} directories and {len(filenames)} images in '{dirpath}'."
        )


def download_data():
    # Setup path to data folder
    data_path = Path("data/")
    image_path = data_path / "pizza_steak_sushi"

    # If the image folder doesn't exist, download it and prepare it...
    if image_path.is_dir():
        print(f"{image_path} directory exists.")
    else:
        print(f"Did not find {image_path} directory, creating one...")
        image_path.mkdir(parents=True, exist_ok=True)

        # Download pizza, steak, sushi data
        with open(data_path / "pizza_steak_sushi.zip", "wb") as f:
            request = requests.get(
                "https://github.com/mrdbourke/pytorch-deep-learning/raw/main/data/pizza_steak_sushi.zip"
            )
            print("Downloading pizza, steak, sushi data...")
            f.write(request.content)

        # Unzip pizza, steak, sushi data
        with zipfile.ZipFile(data_path / "pizza_steak_sushi.zip", "r") as zip_ref:
            print("Unzipping pizza, steak, sushi data...")
            zip_ref.extractall(image_path)


if __name__ == "__main__":
    # Download data
    # download_data()

    data_path = Path("data/")
    image_path = data_path / "pizza_steak_sushi"
    # walk_through_dir(image_path)

    train_dir = image_path / "train"
    test_dir = image_path / "test"
    print(train_dir, test_dir)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    data_transform = transforms.Compose(
        [
            # Resize the images to 64x64
            transforms.Resize(size=(64, 64)),
            # Flip the images randomly on the horizontal
            transforms.RandomHorizontalFlip(
                p=0.5
            ),  # p = probability of flip, 0.5 = 50% chance
            # Turn the image into a torch.Tensor
            transforms.ToTensor(),  # this also converts all pixel values from 0 to 255 to be between 0.0 and 1.0
        ]
    )

    train_data = datasets.ImageFolder(
        root=train_dir,  # target folder of images
        transform=data_transform,  # transforms to perform on data (images)
        target_transform=None,
    )  # transforms to perform on labels (if necessary)

    test_data = datasets.ImageFolder(root=test_dir, transform=data_transform)

    print(f"Train data:\n{train_data}\nTest data:\n{test_data}")

    train_dataloader = DataLoader(
        dataset=train_data,
        batch_size=1,  # how many samples per batch?
        num_workers=1,  # how many subprocesses to use for data loading? (higher = more)
        shuffle=True,
    )  # shuffle the data?

    test_dataloader = DataLoader(
        dataset=test_data, batch_size=1, num_workers=1, shuffle=False
    )  # don't usually need to shuffle testing data
