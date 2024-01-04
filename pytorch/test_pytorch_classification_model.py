import torch


class CircleModelV0(torch.nn.Module):
    def __init__(self):
        super().__init__()
        # 2. Create 2 nn.Linear layers capable of handling X and y input and output shapes
        self.layer_1 = torch.nn.Linear(
            in_features=2, out_features=5
        )  # takes in 2 features (X), produces 5 features
        self.layer_2 = torch.nn.Linear(
            in_features=5, out_features=1
        )  # takes in 5 features, produces 1 feature (y)

    def forward(self, x):
        # Return the output of layer_2, a single feature, the same shape as y
        return self.layer_2(
            self.layer_1(x)
        )  # computation goes through layer_1 first then the output of layer_1 goes through layer_2


# use nn.Sequential to define the model
class CircleModelV1(torch.nn.Module):
    def __init__(self):
        super().__init__()
        # Define the layers using nn.Sequential
        self.model = torch.nn.Sequential(
            torch.nn.Linear(in_features=2, out_features=5),  # First layer
            torch.nn.Linear(in_features=5, out_features=1),  # Second layer
        )

    def forward(self, x):
        # Forward pass through the sequential model
        return self.model(x)
