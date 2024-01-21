import torch
from sklearn.datasets import make_circles

class LinearRegressionModel(torch.nn.Module):
    def __init__(self, lr=0.01):
        super().__init__()
        self.weights = torch.nn.Parameter(
            torch.randn(1, requires_grad=True, dtype=torch.float32)
        )
        self.bias = torch.nn.Parameter(
            torch.randn(1, requires_grad=True, dtype=torch.float32)
        )
        self.loss_fn = torch.nn.MSELoss()
        self.optimizer = torch.optim.SGD(self.parameters(), lr=lr)

    def forward(self, x):
        return self.weights * x + self.bias

    def train_model(self, X_train, y_train, X_test, y_test, epochs=100):
        """
        1	Forward pass
        2	Calculate the loss
        3	Zero gradients
        4	Perform backpropagation on the loss
        5	Update the optimizer (gradient descent)
        """
        for epoch in range(epochs):
            # Training
            self.train()
            y_logits = self(X_train).squeeze() # squeeze to remove extra `1` dimensions, this won't work unless model and data are on same device 
            train_loss = self.loss_fn(y_logits, y_train)
            self.optimizer.zero_grad()
            train_loss.backward()
            self.optimizer.step()

            # Testing
            self.eval()
            with torch.inference_mode():
                y_test_pred = self(X_test)
                test_loss = self.loss_fn(y_test_pred, y_test)

            # Logging
            if epoch % 10 == 0:
                print(
                    f"Epoch: {epoch} | Train Loss: {train_loss:.5f} | Test Loss: {test_loss:.5f}"
                )

    def eval_model(self, X_test, y_test):
        self.eval()
        with torch.no_grad():
            y_pred = self(X_test)
            loss = torch.nn.functional.mse_loss(y_pred, y_test)
        return y_pred, loss.item()

    def inference(self, x_test):
        with torch.no_grad():
            return self(x_test)


def generate_data(weight=0.7, bias=0.3):
    X = torch.arange(0, 1, 0.02).unsqueeze(dim=1)
    y = weight * X + bias
    return X, y


def split_data(X, y, train_ratio=0.8):
    num_samples = X.shape[0]
    train_size = int(num_samples * train_ratio)
    indices = torch.randperm(num_samples)
    return (
        X[indices[:train_size]],
        y[indices[:train_size]],
        X[indices[train_size:]],
        y[indices[train_size:]],
    )


if __name__ == "__main__":
    torch.manual_seed(42)
    model = LinearRegressionModel(lr=0.01)
    X, y = generate_data()
    X_train, y_train, X_test, y_test = split_data(X, y)
    model.train_model(X_train, y_train, X_test, y_test, epochs=100)
    y_pred_test, test_loss = model.eval_model(X_test, y_test)
    print(f"Test Loss: {test_loss}")

    # Inference
    x_new = torch.tensor([1.0, 2.0, 3.0]).unsqueeze(dim=1)
    y_pred_new = model.inference(x_new)
    print("Predictions:", y_pred_new)
