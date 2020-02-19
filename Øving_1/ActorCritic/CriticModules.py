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

    def fit(self, state, td_error, after=False):
        self.state_values[state[0]] = self.state_values[state[0]] + self.lr * self.state_elig[state[0]] * td_error


class NNApproximator:
    def __init__(self, param):
        print(param['network_structure'])
        self.param = param
        self.NN = Net(param['network_structure'])
        self.criterion = nn.MSELoss()
        self.optimizer = optim.SGD(self.NN.parameters(), lr=param['lr_critic'], momentum=0.0)
        print([tuple(layer.shape) for layer in self.NN.parameters()])
        self.elig = [torch.Tensor(np.zeros(tuple(layer.shape))) for layer in self.NN.parameters()
        ]

        self.elig_decay = param['elig_decay_critic']
        self.disc_critic = param['disc_critic']

    def reset(self):
        self.elig = [torch.Tensor(np.zeros(tuple(layer.shape))) for layer in self.NN.parameters()
        ]

    def set_eligibility(self, state, eligibility):
        pass

    def get_eligibility(self, state):
        return -1

    def predict(self, x):

        ans = self.NN(torch.Tensor(x[1].flatten()))
        # ans = self.NN(torch.Tensor(x.flatten()))
        # print("state estimate", ans)
        return ans

    def fit(self, state, td_error, after=False):
        """

        @param state:
        @param td_error:
        @return:
        """

        if not after:
            return

        self.optimizer.zero_grad()
        # print("TD_error: ", td_error)

        # print("error", td_error)
        if td_error == 0:
            td_error = 1.0E-10

        outputs = self.NN(torch.Tensor(state[1].flatten()))
        # outputs = self.NN(torch.Tensor(state.flatten()))
        # loss = self.criterion(outputs, outputs + td_error)
        loss = self.criterion(outputs + td_error, outputs)
        loss.backward(retain_graph=True)
        # Update weights with eligibility
        for num, f in enumerate(self.NN.parameters()):
            # if num % 2 == 1: continue
            self.elig[num] = self.elig[num] + f.grad * ((2 * float(td_error)) ** (-1))
            f.grad = float(td_error) * self.elig[num]
            self.elig[num] = self.disc_critic * self.elig_decay * self.elig[num]
        self.optimizer.step()

        # print("epoch: {0}, running_loss: {1:.3f}".format(0, loss.item()))


class Net(nn.Module):
    def __init__(self, architectrue):
        super(Net, self).__init__()
        self.weights = nn.ModuleList()
        print(architectrue)
        for num, val in enumerate(architectrue):
            if num == 0: continue
            print(num, val, architectrue[num - 1])
            self.weights.append(nn.Linear(architectrue[num - 1], val))
        # self.weights=nn.ParameterList(self.weights)
        # self.fc1 = nn.Linear(25, 100)
        # self.fc2 = nn.Linear(100, 100)
        # self.fc3 = nn.Linear(100, 100)
        # self.fc4 = nn.Linear(100, 1)

    def forward(self, x):
        for num, layer in enumerate(self.weights):
            if num + 1 == len(self.weights):
                x = F.tanh(layer(x))
            else:
                x = F.relu(layer(x))
        # x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        # x = F.relu(self.fc3(x))
        # x = F.sigmoid(self.fc4(x))
        return x


if __name__ == '__main__':
    # param=
    net = NNApproximator({'network_structure': [2, 10, 1], 'lr_critic': 0.02, 'elig_decay_critic': 0.3})

    # criterion = nn.MSELoss()
    # optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.0)

    x = [np.array([1, 0]), np.array([0, 1]), np.array([0, 0]), np.array([1, 1])]
    y = [np.array([0]), np.array([0]), np.array([0]), np.array([1])]

    tensor_x = torch.Tensor(x)
    tensor_y = torch.Tensor(y)

    print(net.predict(tensor_x[0]))
    for _ in range(1000):
        for num in range(4):
            td_error = tensor_y[num] - net.predict(tensor_x[num])
            net.fit(tensor_x[num], td_error, after=True)
            print("out", net.predict(tensor_x[num]), tensor_y[num])

    # dataset_x = data.TensorDataset(tensor_x, tensor_y)
    # dataloader = data.DataLoader(dataset_x)

    # elig = [
    #     torch.Tensor(np.zeros((100, 2))), torch.Tensor(np.zeros((100))),
    #     torch.Tensor(np.zeros((100, 100))), torch.Tensor(np.zeros((100))),
    #     torch.Tensor(np.zeros((100, 100))), torch.Tensor(np.zeros((100))),
    #     torch.Tensor(np.zeros((1, 100))), torch.Tensor(np.zeros((1)))
    # ]
    #
    # for epoch in range(2000):
    #     running_loss = 0.0
    #
    #     for i, data in enumerate(dataloader, 0):
    #         inputs, labels = data
    #         optimizer.zero_grad()
    #
    #         outputs = net(inputs)
    #         loss = criterion(outputs, labels)
    #         loss.backward()
    #         td_error = outputs - labels
    #         for num, f in enumerate(net.parameters()):
    #             elig[num] = elig[num] + f.grad * ((2 * float(td_error)) ** (-1))
    #             f.grad = float(td_error) * elig[num]
    #             elig[num] = 0.6 * elig[num]
    #         optimizer.step()
    #
    #         running_loss += loss.item()
    #     print("epoch: {0}, running_loss: {1:.3f}".format(epoch, running_loss / 4))
