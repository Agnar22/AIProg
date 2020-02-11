import torch.nn as nn
import torch.nn.functional as F


# Use MSE

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(2, 10)
        # self.fc2 = nn.Linear(100, 100)
        # self.fc3 = nn.Linear(100, 100)
        self.fc4 = nn.Linear(10, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        # x = F.relu(self.fc3(x))
        x = F.sigmoid(self.fc4(x))
        return x


if __name__ == '__main__':
    import torch.optim as optim
    import numpy as np
    import torch
    from torch.utils import data

    net = Net()

    criterion = nn.MSELoss()
    optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.0)

    x = [np.array([1, 0]), np.array([0, 1]), np.array([0, 0]), np.array([1, 1])]
    y = [np.array([0]), np.array([0]), np.array([0]), np.array([1])]

    tensor_x = torch.Tensor(x)
    tensor_y = torch.Tensor(y)

    dataset_x = data.TensorDataset(tensor_x, tensor_y)
    dataloader = data.DataLoader(dataset_x)

    elig = [torch.Tensor(np.zeros((10, 2))),
            torch.Tensor(np.zeros((1, 10)))]

    for epoch in range(100):
        running_loss = 0.0

        for i, data in enumerate(dataloader, 0):
            inputs, labels = data
            optimizer.zero_grad()

            outputs = net(inputs)
            # print(outputs, inputs, labels)
            loss = criterion(outputs, labels)
            loss.backward()
            td_error = labels - outputs
            for num, f in enumerate(net.parameters()):
                if num % 2 == 1: continue
                # print(num, f.grad.shape, elig[num//2].shape)

                elig[num // 2] = elig[num // 2] - f.grad * ((2 * td_error) ** (-1))
                print(td_error, elig[num // 2])
                # print(td_error * elig[num // 2])
                # f.grad.data = td_error * elig[num // 2]
                # print(elig[num // 2].mean(), elig[num // 3].abs().mean())
                # print(elig[num//2])
                # print(f.grad.shape)
            optimizer.step()

            running_loss += loss.item()
        # print("epoch: {0}, running_loss: {1:.3f}".format(epoch, running_loss / 4))
