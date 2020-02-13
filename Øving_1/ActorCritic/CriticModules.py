import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import torch
from torch.utils import data


class Table:
    def __init__(self, lr):
        self.state_values = dict()
        self.lr = lr
        self.state_elig = dict()

    def reset(self):
        self.state_values = dict()
        self.state_elig = dict()

    def set_eligibility(self, state, eligibility):
        self.state_elig[state[0]] = eligibility

    def get_eligibility(self, state):
        return self.state_elig[state[0]]

    def predict(self, state):
        return self.state_values.setdefault(state[0], np.random.uniform(-0.01, 0.01))

    def fit(self, state, td_error):
        self.state_values[state[0]] = self.state_values[state[0]] + self.lr * self.state_elig[state[0]] * td_error


class NNApproximator:
    def __init__(self, NN):
        self.NN = NN
        self.criterion = nn.MSELoss()
        self.optimizer = optim.SGD(NN.parameters(), lr=0.1, momentum=0.0)
        self.elig = [
            torch.Tensor(np.zeros((100, 2))), torch.Tensor(np.zeros((100))),
            torch.Tensor(np.zeros((100, 100))), torch.Tensor(np.zeros((100))),
            torch.Tensor(np.zeros((100, 100))), torch.Tensor(np.zeros((100))),
            torch.Tensor(np.zeros((1, 100))), torch.Tensor(np.zeros((1)))
        ]
        self.elig_decay = 0.9

    def reset(self):
        self.elig = [
            torch.Tensor(np.zeros((100, 25))), torch.Tensor(np.zeros((100))),
            torch.Tensor(np.zeros((100, 100))), torch.Tensor(np.zeros((100))),
            torch.Tensor(np.zeros((100, 100))), torch.Tensor(np.zeros((100))),
            torch.Tensor(np.zeros((1, 100))), torch.Tensor(np.zeros((1)))
        ]

    def set_eligibility(self, state, eligibility):
        pass

    def get_eligibility(self, state):
        return -1

    def predict(self, x):
        ans = self.NN(torch.Tensor(x[1].flatten()))
        print(ans)
        return ans

    def fit(self, state, td_error):
        """

        @param state:
        @param td_error:
        @return:
        """

        self.optimizer.zero_grad()

        outputs = self.NN(torch.Tensor(state[1].flatten()))
        loss = self.criterion(outputs, outputs + td_error)
        loss.backward(retain_graph=True)

        # Update weights with eligibility
        for num, f in enumerate(self.NN.parameters()):
            self.elig[num] = self.elig[num] + f.grad * ((2 * float(td_error)) ** (-1))
            f.grad = float(td_error) * self.elig[num]
            self.elig[num] = self.elig_decay * self.elig[num]
        self.optimizer.step()

        # print("epoch: {0}, running_loss: {1:.3f}".format(0, loss.item()))


class Net(nn.Module):
    def __init__(self, architectrue):
        super(Net, self).__init__()
        self.weights = []
        for num, val in enumerate(architectrue, 1):
            self.weights.append(nn.Linear(architectrue[num - 1], val))
        # self.fc1 = nn.Linear(25, 100)
        # self.fc2 = nn.Linear(100, 100)
        # self.fc3 = nn.Linear(100, 100)
        # self.fc4 = nn.Linear(100, 1)

    def forward(self, x):
        for layer in self.weights:
            x = F.relu(layer(x))
        # x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        # x = F.relu(self.fc3(x))
        # x = F.sigmoid(self.fc4(x))
        return x


if __name__ == '__main__':
    net = Net()

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
