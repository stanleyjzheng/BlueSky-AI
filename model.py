from makedataset import dataset
import pandas as pd
import numpy as np
from collections import namedtuple
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
import torch
import numpy

train, trainLabels, verLabels, ver = dataset()


def processDF():
    a

DISCOVERY_DOY = pd.DataFrame(data,columns=['DISCOVERY_DOY','Age'])



def train_model(model, dataloaders, criterion, optimizer, epochs=25, is_inception=False):
    val_acc_history = []
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    for epoch in range(epochs):
        printEpoch = 'Epoch [{}/{}]'.format(epoch, epochs - 1)
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  
            else:
                model.eval()
            running_loss = 0.0
            running_corrects = 0
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)
                optimizer.zero_grad()
                with torch.set_grad_enabled(phase == 'train'):
                    if is_inception and phase == 'train':
                        outputs, aux_outputs = model(inputs)
                        loss1 = criterion(outputs, labels)
                        loss2 = criterion(aux_outputs, labels)
                        loss = loss1 + 0.4*loss2
                    else:
                        outputs = model(inputs)
                        loss = criterion(outputs, labels)

                    _, preds = torch.max(outputs, 1)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)
            print(printEpoch + ', {} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
            if phase == 'val':
                val_acc_history.append(epoch_acc)

    model.load_state_dict(best_model_wts)
    return model, val_acc_history

def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False

model, input_size = initialize_model(modelName, numClasses, feature_extract, use_pretrained=True)

train = torch.utils.data.TensorDataset(images, labels)
verification = torch.utils.data.TensorDataset(verImg, verLabels)
train = torch.utils.data.DataLoader(train, batchSize = batchSize, shuffle = True, num_workers = 4)
verification = torch.utils.data.DataLoader(verification, batchSize = 180, shuffle = True, num_workers = 4)
dataloaders_dict = {'train': train, 'val': verification}
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = model.to(device)
params_to_update = model.parameters()
optimizer_ft = torch.optim.SGD(params_to_update, lr=1e-4, momentum=0.9)#, nesterov = True)
criterion = torch.nn.CrossEntropyLoss()