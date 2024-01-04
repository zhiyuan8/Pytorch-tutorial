import torch
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split


# Calculate accuracy (a classification metric)
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
class CircleModelV1(torch.nn.Module):
    def __init__(self):
        super().__init__()
        # Define the layers using nn.Sequential
        self.model = torch.nn.Sequential(
            torch.nn.Linear(in_features=2, out_features=5),  # First layer
            torch.nn.Linear(in_features=5, out_features=1),  # Second layer
        ).to(device)
        self.loss_fn = torch.nn.BCEWithLogitsLoss()  # Does not require sigmoid on input
        self.optimizer = torch.optim.SGD(self.parameters(), lr=0.1)

    def forward(self, x):
        # Forward pass through the sequential model
        return self.model(x)

    def train_model(self, X_train, y_train, X_test, y_test, epochs=1000, lr=0.01):
        """
        1	Forward pass
        2	Calculate the loss
        3	Zero gradients
        4	Perform backpropagation on the loss
        5	Update the optimizer (gradient descent)
        """
        for epoch in range(epochs):
            self.train()
            y_logits = self(X_train).squeeze()
            loss = self.loss_fn(y_logits, y_train)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            self.eval()
            with torch.inference_mode():
                y_logits_test = self(X_test).squeeze()
                test_loss = self.loss_fn(y_logits_test, y_test)

            if epoch % 100 == 0:
                y_pred = torch.sigmoid(y_logits).round()
                acc = accuracy_fn(y_train, y_pred)

                y_pred_test = torch.sigmoid(y_logits_test).round()
                test_acc = accuracy_fn(y_test, y_pred_test)

                print(
                    f"Epoch {epoch} | Training Loss: {loss.item()} | Training Accuracy: {acc} | Test Loss: {test_loss.item()} | Test Accuracy: {test_acc}"
                )

    def eval_model(self, X_test, y_test):
        self.eval()
        with torch.no_grad():
            y_logits = self(X_test).squeeze()
            y_pred = torch.sigmoid(y_logits).round()
            loss = self.loss_fn(y_logits, y_test)
            acc = accuracy_fn(y_test, y_pred)
        return y_pred, loss.item(), acc

    def inference(self, x_test):
        with torch.no_grad():
            return torch.round(torch.sigmoid(self(x_test)))


def generate_data(weight=0.7, bias=0.3):
    X = torch.arange(0, 1, 0.02).unsqueeze(dim=1)
    y = weight * X + bias
    return X, y


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Make 1000 samples
    n_samples = 1000
    X, y = make_circles(n_samples, noise=0.03, random_state=42)
    X = torch.from_numpy(X).type(torch.float).to(device)
    y = torch.from_numpy(y).type(torch.float).to(device)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model_0 = CircleModelV1()
    model_0.to(device)
    model_0.train_model(X_train, y_train, X_test, y_test, epochs=1000)
    
    # Save the trained model
    model_path = "circle_model_v1.pth"
    torch.save(model_0.state_dict(), model_path)

    # Load the model for inference
    loaded_model = CircleModelV1()
    loaded_model.load_state_dict(torch.load(model_path))
    loaded_model.to(device)
    loaded_model.eval()

    # Perform inference
    predictions, test_loss, test_accuracy = loaded_model.eval_model(X_test, y_test)
    print(f"Test Loss: {test_loss}, Test Accuracy: {test_accuracy}")

    # Example of using inference method
    example_data = X_test[:5]  # Taking a small subset for demonstration
    example_predictions = loaded_model.inference(example_data)
    print("Example Predictions:", example_predictions)
