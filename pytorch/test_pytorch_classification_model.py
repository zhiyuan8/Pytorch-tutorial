import torch

# Calculate accuracy (a classification metric)
def accuracy_fn(y_true, y_pred):
    correct = torch.eq(y_true, y_pred).sum().item() # torch.eq() calculates where two tensors are equal
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
        )
        self.loss_fn = torch.nn.BCEWithLogitsLoss() # Does not require sigmoid on input
        self.optimizer = torch.optim.SGD(self.parameters(), lr=0.1)
        
    def forward(self, x):
        # Forward pass through the sequential model
        return self.model(x)

    def train_model(self, X_train, y_train, X_test, y_test, epochs=100, lr=0.01):
        """
        1	Forward pass
        2	Calculate the loss
        3	Zero gradients
        4	Perform backpropagation on the loss
        5	Update the optimizer (gradient descent)
        """
        for epoch in range(epochs):
            self.train()
            
            # Training
            y_logits = self(X_train).squeeze()
            y_pred = torch.round(torch.sigmoid(y_logits))
            
            y_pred = self(X_train)
            loss = self.loss_fn(y_pred, y_train)
            acc = accuracy_fn(y_true=y_train, 
                      y_pred=y_pred)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            self.eval()
            
            with torch.inference_mode():
                y_logits_test = self(X_test).squeeze()
                y_pred_test = torch.round(torch.sigmoid(y_logits_test))
                test_loss = self.loss_fn(y_pred_test, y_test)
                test_acc = accuracy_fn(y_true=y_test, 
                      y_pred=y_pred_test)
            
            if epoch % 10 == 0:
                print(f"Epoch {epoch} | Training Loss: {loss.item()} | Training Accuracy: {acc} | Test Loss: {test_loss.item()} | Test Accuracy: {test_acc}")
        
        
    
    def eval_model(self, X_test, y_test):
        pass
    
    def inference(self, x_test):
        pass