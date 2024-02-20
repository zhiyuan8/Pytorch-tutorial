import torch
from torch import nn
import torchvision
from torchvision import datasets
from torchvision.transforms import ToTensor

# Import matplotlib for visualization
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from tqdm import tqdm
from helper_functions import accuracy_fn, print_train_time, timer


class FashionMNISTModelV0(nn.Module):
    def __init__(self, input_shape: int, hidden_units: int, output_shape: int):
        super().__init__()
        self.layer_stack = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=input_shape, out_features=hidden_units),
            nn.Linear(in_features=hidden_units, out_features=output_shape),
        )

    def forward(self, x):
        return self.layer_stack(x)


class FashionMNISTModelV2(nn.Module):
    """
    Model architecture copying TinyVGG from:
    https://poloclub.github.io/cnn-explainer/
    """

    def __init__(self, input_shape: int, hidden_units: int, output_shape: int):
        super().__init__()
        self.block_1 = nn.Sequential(
            nn.Conv2d(
                in_channels=input_shape,
                out_channels=hidden_units,
                kernel_size=3,  # how big is the square that's going over the image?
                stride=1,  # default
                padding=1,
            ),  # options = "valid" (no padding) or "same" (output has same shape as input) or int for specific number
            nn.ReLU(),
            nn.Conv2d(
                in_channels=hidden_units,
                out_channels=hidden_units,
                kernel_size=3,
                stride=1,
                padding=1,
            ),
            nn.ReLU(),
            nn.MaxPool2d(
                kernel_size=2, stride=2
            ),  # default stride value is same as kernel_size
        )
        self.block_2 = nn.Sequential(
            nn.Conv2d(hidden_units, hidden_units, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hidden_units, hidden_units, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            # Where did this in_features shape come from?
            # It's because each layer of our network compresses and changes the shape of our inputs data.
            nn.Linear(in_features=hidden_units * 7 * 7, out_features=output_shape),
        )

    def forward(self, x: torch.Tensor):
        x = self.block_1(x)
        # print(x.shape)
        x = self.block_2(x)
        # print(x.shape)
        x = self.classifier(x)
        # print(x.shape)
        return x


def set_up_model():
    model_0 = FashionMNISTModelV0(
        input_shape=784, hidden_units=10, output_shape=10  # 28x28 pixels  # 10 classes
    )
    model_0 = model_0.to(device)

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(params=model_0.parameters(), lr=0.1)
    return model_0, loss_fn, optimizer


def read_data():
    train_data = datasets.FashionMNIST(
        root="data",  # where to download data to?
        train=True,  # get training data
        download=True,  # download data if it doesn't exist on disk
        transform=ToTensor(),  # images come as PIL format, we want to turn into Torch tensors
        target_transform=None,  # you can transform labels as well
    )

    # Setup testing data
    test_data = datasets.FashionMNIST(
        root="data", train=False, download=True, transform=ToTensor()  # get test data
    )
    # How many samples are there?
    print(
        "How many samples: ",
        len(train_data.data),
        len(train_data.targets),
        len(test_data.data),
        len(test_data.targets),
    )
    # Setup the batch size hyperparameter
    BATCH_SIZE = 32
    # Turn datasets into iterables (batches)
    train_dataloader = DataLoader(
        train_data,  # dataset to turn into iterable
        batch_size=BATCH_SIZE,  # how many samples per batch?
        shuffle=True,  # shuffle data every epoch?
    )

    test_dataloader = DataLoader(
        test_data,
        batch_size=BATCH_SIZE,
        shuffle=False,  # don't necessarily have to shuffle the testing data
    )
    return train_data, test_data, train_dataloader, test_dataloader


# our loss and evaluation metrics will be calculated per batch rather than across the whole dataset.
def train_model(model_0, train_dataloader, test_dataloader, loss_fn, optimizer):
    torch.manual_seed(42)
    train_time_start_on_cpu = timer()
    epochs = 3

    # Create training and testing loop
    for epoch in tqdm(range(epochs)):
        print(f"Epoch: {epoch}\n-------")
        ### Training
        train_loss = 0
        # Add a loop to loop through training batches
        for batch, (X, y) in enumerate(train_dataloader):
            X, y = X.to(device), y.to(
                device
            )  # Move data to the same device as the model
            model_0.train()
            # 1. Forward pass
            y_pred = model_0(X)

            # 2. Calculate loss (per batch)
            loss = loss_fn(y_pred, y)
            train_loss += loss  # accumulatively add up the loss per epoch

            # 3. Optimizer zero grad
            optimizer.zero_grad()

            # 4. Loss backward
            loss.backward()

            # 5. Optimizer step
            optimizer.step()

            # Print out how many samples have been seen
            if batch % 400 == 0:
                print(
                    f"Looked at {batch * len(X)}/{len(train_dataloader.dataset)} samples"
                )

        # Divide total train loss by length of train dataloader (average loss per batch per epoch)
        train_loss /= len(train_dataloader)

        ### Testing
        # Setup variables for accumulatively adding up loss and accuracy
        test_loss, test_acc = 0, 0
        model_0.eval()
        with torch.inference_mode():
            for X, y in test_dataloader:
                # 1. Forward pass
                X, y = X.to(device), y.to(
                    device
                )  # Move data to the same device as the model
                test_pred = model_0(X)

                # 2. Calculate loss (accumatively)
                test_loss += loss_fn(
                    test_pred, y
                )  # accumulatively add up the loss per epoch

                # 3. Calculate accuracy (preds need to be same as y_true)
                test_acc += accuracy_fn(y_true=y, y_pred=test_pred.argmax(dim=1))

            # Calculations on test metrics need to happen inside torch.inference_mode()
            # Divide total test loss by length of test dataloader (per batch)
            test_loss /= len(test_dataloader)

            # Divide total accuracy by length of test dataloader (per batch)
            test_acc /= len(test_dataloader)

        ## Print out what's happening
        print(
            f"\nTrain loss: {train_loss:.5f} | Test loss: {test_loss:.5f}, Test acc: {test_acc:.2f}%\n"
        )

    # Calculate training time
    train_time_end_on_cpu = timer()
    total_train_time_model_0 = print_train_time(
        start=train_time_start_on_cpu,
        end=train_time_end_on_cpu,
        device=str(next(model_0.parameters()).device),
    )
    return model_0  # Return the model


def eval_model(
    model: torch.nn.Module,
    data_loader: torch.utils.data.DataLoader,
    loss_fn: torch.nn.Module,
    accuracy_fn,
):
    """Returns a dictionary containing the results of model predicting on data_loader.

    Args:
        model (torch.nn.Module): A PyTorch model capable of making predictions on data_loader.
        data_loader (torch.utils.data.DataLoader): The target dataset to predict on.
        loss_fn (torch.nn.Module): The loss function of model.
        accuracy_fn: An accuracy function to compare the models predictions to the truth labels.

    Returns:
        (dict): Results of model making predictions on data_loader.
    """
    model.to(device)  # Ensure model is on the correct device
    loss, acc = 0, 0
    model.eval()
    with torch.inference_mode():
        for X, y in data_loader:
            # Make predictions with the model
            y_pred = model(X)

            # Accumulate the loss and accuracy values per batch
            loss += loss_fn(y_pred, y)
            acc += accuracy_fn(
                y_true=y, y_pred=y_pred.argmax(dim=1)
            )  # For accuracy, need the prediction labels (logits -> pred_prob -> pred_labels)

        # Scale loss and acc to find the average loss/acc per batch
        loss /= len(data_loader)
        acc /= len(data_loader)

    return {
        "model_name": model.__class__.__name__,  # only works when model was created with a class
        "model_loss": loss.item(),
        "model_acc": acc,
    }


if __name__ == "__main__":
    train_data, test_data, train_dataloader, test_dataloader = read_data()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model, loss_fn, optimizer = set_up_model()
    model = train_model(model, train_dataloader, test_dataloader, loss_fn, optimizer)
    model_results = eval_model(
        model=model,
        data_loader=test_dataloader,
        loss_fn=loss_fn,
        accuracy_fn=accuracy_fn,
    )
