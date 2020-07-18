from __future__ import print_function
import argparse
from makedataset import dataset
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
import numpy as np

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.input = nn.Linear(4, 14)
        self.dense1 = nn.Linear(14, 9)
        self.dense2 = nn.Linear(9, 3)
        #self.dense3 = nn.Linear(3, 1)

    def forward(self, x):
        x = self.input(x)
        x = F.relu(x)
        x = self.dense1(x)
        x = F.relu(x)
        x = self.dense2(x)
        #x = self.dense3(x)
        #output = F.log_softmax(x, dim=1)
        #x = x.clamp(0, 1)

        output = F.sigmoid(x)

        return output

def train(args, model, device, train_loader, optimizer, epoch):
    for batch_idx, (data, target) in enumerate(train_loader):
        with torch.set_grad_enabled(True):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            output = output.type(torch.float)
            target = target.type(torch.long)
            criterion = torch.nn.CrossEntropyLoss()
            loss = criterion(output, torch.max(target, 1)[1])
            loss.backward()
            optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
            if args.dry_run:
                break

def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    cost=0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            output = output.type(torch.float)
            target = target.type(torch.long)
            criterion = torch.nn.CrossEntropyLoss()
            test_loss = criterion(output, torch.max(target, 1)[1]).item()
            cost += abs(target-output)
        diff = torch.sum(cost)
    print(len(test_loader.dataset))
    diff /= len(test_loader.dataset)
    test_loss /= 48

    print('\nTest set: Average loss: ' + str(test_loss) + ' Cost:' + str(diff.item()))

def main():
    parser = argparse.ArgumentParser(description='Forestfire-AI')
    parser.add_argument('--batch-size', type=int, default=2048, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default= 2191, metavar='N',
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--epochs', type=int, default=40, metavar='N',
                        help='number of epochs to train (default: 14)')
    parser.add_argument('--lr', type=float, default=0.5, metavar='LR',
                        help='learning rate (default: 1.0)')
    parser.add_argument('--gamma', type=float, default=0.7, metavar='M',
                        help='Learning rate step gamma (default: 0.7)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='quickly check a single pass')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=40, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--save-model', action='store_true', default=False,
                        help='For Saving the current Model')
    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()

    torch.manual_seed(args.seed)

    device = torch.device("cuda" if use_cuda else "cpu")

    kwargs = {'batch_size': args.batch_size}
    if use_cuda:
        kwargs.update({'num_workers': 1,
                       'pin_memory': True,
                       'shuffle': True},
                      )
    batchSize=2048 
    train1, trainLabels, ver, verLabels = dataset()
    train1, trainLabels, ver, verLabels = torch.from_numpy(np.array(train1).astype(np.float32)), torch.from_numpy(np.array(trainLabels).astype(np.float32)), torch.from_numpy(np.array(ver).astype(np.float32)), torch.from_numpy(np.array(verLabels).astype(np.float32))
    train1, trainLabels, ver, verLabels = torch.tensor(train1), torch.tensor(trainLabels), torch.tensor(ver), torch.tensor(verLabels)

    train1 = torch.utils.data.TensorDataset(train1, trainLabels)
    verification = torch.utils.data.TensorDataset(ver, verLabels)
    train_loader = torch.utils.data.DataLoader(train1, batch_size = 2048, shuffle = True, num_workers = 4)
    test_loader = torch.utils.data.DataLoader(verification, batch_size = 2191, shuffle = True, num_workers = 4)
    model = Net().to(device)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    scheduler = StepLR(optimizer, step_size=1, gamma=args.gamma)
    for epoch in range(1, args.epochs + 1):
        train(args, model, device, train_loader, optimizer, epoch)
        test(model, device, test_loader)
        scheduler.step()

    torch.save(model, "forestfire-aiwork.pt")

if __name__ == '__main__':
    main()