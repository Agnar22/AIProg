import torch.nn as nn
import torch.nn.functional as F


class Table:
    def __init__(self):
        self.state_values = dict()

    def predict(self, state):
        return self.state_values.setdefault(state, np.random.uniform(-0.01, 0.01))


class NNApproximator:
    def __init__(self, NN):
        self.NN = NN

    def predict(self, x):
        return self.NN(torch.Tensor(x))


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(2, 100)
        self.fc2 = nn.Linear(100, 100)
        self.fc3 = nn.Linear(100, 100)
        self.fc4 = nn.Linear(100, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.sigmoid(self.fc4(x))
        return x


if __name__ == '__main__':
    import torch.optim as optim
    import numpy as np
    import torch
    from torch.utils import data

    net = Net()
    # net.predict([np.array([1, 0])])

    criterion = nn.MSELoss()
    optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.0)

    x = [np.array([1, 0]), np.array([0, 1]), np.array([0, 0]), np.array([1, 1])]
    y = [np.array([0]), np.array([0]), np.array([0]), np.array([1])]

    tensor_x = torch.Tensor(x)
    tensor_y = torch.Tensor(y)

    dataset_x = data.TensorDataset(tensor_x, tensor_y)
    dataloader = data.DataLoader(dataset_x)

    elig = [
        torch.Tensor(np.zeros((100, 2))), torch.Tensor(np.zeros((100))),
        torch.Tensor(np.zeros((100, 100))), torch.Tensor(np.zeros((100))),
        torch.Tensor(np.zeros((100, 100))), torch.Tensor(np.zeros((100))),
        torch.Tensor(np.zeros((1, 100))), torch.Tensor(np.zeros((1)))
    ]

    for epoch in range(2000):
        running_loss = 0.0

        for i, data in enumerate(dataloader, 0):
            inputs, labels = data
            optimizer.zero_grad()

            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            td_error = outputs - labels
            for num, f in enumerate(net.parameters()):
                elig[num] = elig[num] + f.grad * ((2 * float(td_error)) ** (-1))
                f.grad = float(td_error) * elig[num]
                elig[num] = 0.6 * elig[num]
            optimizer.step()

            running_loss += loss.item()
        print("epoch: {0}, running_loss: {1:.3f}".format(epoch, running_loss / 4))
