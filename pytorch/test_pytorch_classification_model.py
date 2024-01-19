import torch
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from torch import nn


# Calculate ac# In the code, `c` is used as a parameter in the `scatter` function to specify the color
# of each data point in the scatter plot.
def accuracy_fn(y_true, y_pred):
    correct = (
        torch.eq(y_true, y_pred).sum().item()
    )  # torch.eq() calculates where two tensors are equal
    acc = (correct / len(y_pred)) * 100
    return acc


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
class CircleModelV1(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=2, out_features=10)
        self.layer_2 = nn.Linear(in_features=10, out_features=10)
        self.layer_3 = nn.Linear(in_features=10, out_features=1)
        self.relu = nn.ReLU()

        self.loss_fn = nn.BCEWithLogitsLoss()
        self.optimizer = torch.optim.SGD(self.parameters(), lr=0.1)

    def forward(self, x):
        x = self.relu(self.layer_1(x))
        x = self.relu(self.layer_2(x))
        return self.layer_3(x)

    def train_model(self, X_train, y_train, X_test, y_test, epochs=1000):
        train_losses = []
        test_losses = []
        for epoch in range(epochs):
            self.train()
            y_logits = self(X_train).squeeze()
            loss = self.loss_fn(y_logits, y_train)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            # Save training loss for visualization
            train_losses.append(loss.item())

            self.eval()
            with torch.no_grad():
                y_logits_test = self(X_test).squeeze()
                test_loss = self.loss_fn(y_logits_test, y_test)
                # Save testing loss for visualization
                test_losses.append(test_loss.item())

            if epoch % 100 == 0:
                y_pred = torch.sigmoid(y_logits).round()
                acc = accuracy_fn(y_train, y_pred)
                y_pred_test = torch.sigmoid(y_logits_test).round()
                test_acc = accuracy_fn(y_test, y_pred_test)

                print(
                    f"Epoch {epoch} | Training Loss: {loss.item()} | Training Accuracy: {acc} | Test Loss: {test_loss.item()} | Test Accuracy: {test_acc}"
                )

        return train_losses, test_losses

    def eval_model(self, X_test, y_test):
        self.eval()
        with torch.no_grad():
            y_logits = self(X_test).squeeze()
            y_pred = torch.sigmoid(y_logits).round()
            loss = self.loss_fn(y_logits, y_test)
            acc = accuracy_fn(y_test, y_pred)
        return y_pred, loss.item(), acc

    def inference(self, x_test):
        self.eval()
        with torch.no_grad():
            y_logits = self(x_test).squeeze()
            return torch.sigmoid(y_logits).round()


def generate_data(weight=0.7, bias=0.3):
    X = torch.arange(0, 1, 0.02).unsqueeze(dim=1)
    y = weight * X + bias
    return X, y


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    n_samples = 1000
    X, y = make_circles(n_samples, noise=0.03, random_state=42)
    X = torch.from_numpy(X).type(torch.float).to(device)
    y = torch.from_numpy(y).type(torch.float).to(device)

    fig, ax = plt.subplots()
    ax.scatter(X[:, 0].cpu(), X[:, 1].cpu(), c=y.cpu(), cmap=plt.cm.RdYlBu)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.title("Circle Data Visualization")
    fig.savefig("circle_data.png")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model_1 = CircleModelV1()
    model_1.to(device)
    train_losses, test_losses = model_1.train_model(
        X_train, y_train, X_test, y_test, epochs=1000
    )

    # Plotting training and testing loss curves
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label="Training Loss")
    plt.plot(test_losses, label="Testing Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title("Training and Testing Loss Curves")
    plt.legend()
    plt.savefig("loss_curves.png")
    plt.show()

    model_path = "circle_model_v1.pth"
    torch.save(model_1.state_dict(), model_path)

    loaded_model = CircleModelV1()
    loaded_model.load_state_dict(torch.load(model_path))
    loaded_model.to(device)

    predictions, test_loss, test_accuracy = loaded_model.eval_model(X_test, y_test)
    print(f"Test Loss: {test_loss}, Test Accuracy: {test_accuracy}")

    example_data = X_test[:5]
    y_test_pred = model_1.inference(X_test)
    plt.figure(figsize=(10, 5))
    plt.scatter(
        X_test[:, 0].cpu(),
        X_test[:, 1].cpu(),
        c=y_test.cpu(),
        cmap="Reds",
        label="Actual",
    )
    plt.scatter(
        X_test[:, 0].cpu(),
        X_test[:, 1].cpu(),
        c=y_test_pred.cpu(),
        cmap="Blues",
        alpha=0.5,
        label="Predicted",
    )
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.title("Actual vs Predicted Data Points")
    plt.legend()
    plt.savefig("actual_vs_predicted.png")
    plt.show()
