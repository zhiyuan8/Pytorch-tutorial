import torch
import torchvision
import matplotlib.pyplot as plt
from torch import nn
from torchvision import transforms
from pathlib import Path

# Import your custom modules here. Replace 'your_module' with the actual module name.
# from your_module import engine, data_setup
from torchinfo import summary
from timeit import default_timer as timer
from modular import engine, data_setup

start_time = timer()

if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Setup path to data folder
    data_path = Path("data/")
    image_path = data_path / "pizza_steak_sushi"
    train_dir = image_path / "train"
    test_dir = image_path / "test"

    manual_transforms = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    train_dataloader, test_dataloader, class_names = data_setup.create_dataloaders(
        train_dir=train_dir,
        test_dir=test_dir,
        transform=manual_transforms,
        batch_size=32,
    )

    print(train_dataloader, test_dataloader, class_names)

    model = torchvision.models.efficientnet_b0(
        weights=torchvision.models.EfficientNet_B0_Weights.DEFAULT
    ).to(device)

    print(
        summary(
            model,
            input_size=(32, 3, 224, 224),
            col_names=["input_size", "output_size", "num_params", "trainable"],
            col_width=20,
            row_settings=["var_names"],
        )
    )

    for param in model.features.parameters():
        param.requires_grad = False

    torch.manual_seed(42)
    torch.cuda.manual_seed(42)

    output_shape = len(class_names)

    model.classifier = nn.Sequential(
        nn.Dropout(p=0.2, inplace=True),
        nn.Linear(in_features=1280, out_features=output_shape, bias=True),
    ).to(device)

    print(
        summary(
            model,
            input_size=(32, 3, 224, 224),
            verbose=0,
            col_names=["input_size", "output_size", "num_params", "trainable"],
            col_width=20,
            row_settings=["var_names"],
        )
    )

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    results = engine.train(
        model=model,
        train_dataloader=train_dataloader,
        test_dataloader=test_dataloader,
        optimizer=optimizer,
        loss_fn=loss_fn,
        epochs=5,
        device=device,
    )

    end_time = timer()
    print(f"[INFO] Total training time: {end_time - start_time:.3f} seconds")
