from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox

import torch
import torchvision

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import matplotlib.pyplot as plt

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay



# очередность расположения строк
rowShowRecognizedPatterns = 0
rowChanceOfPatternDetection = rowShowRecognizedPatterns + 1
rowTrainModel = rowChanceOfPatternDetection + 1
rowCheckRecognizedPattern = rowTrainModel + 1
rowScrolledText = rowCheckRecognizedPattern + 1


# создание окна
window = Tk()
window.title("AIClassificationTask")
window.geometry('600x550')


# значения, введенные пользователем
valN_epochs = StringVar()
valRecognizedPattern = StringVar()



# оисание столбиков
lblEpochs = Label(window, text="Кол-во эпох обучения")
lblEpochs.grid(column=0, row=rowTrainModel, pady=5)
txtN_epochs = Entry(window, width=10, textvariable=valN_epochs)
txtN_epochs.grid(column=1, row=rowTrainModel)
txtN_epochs.insert(0, 7)
lblEmpty = Label(window, text="")       # создает третий столбик в grid для красивого вывода infoPanel
lblEmpty.grid(column=3, row=rowTrainModel, padx=100)

lblCheckRecognizedPattern = Label(window, text="Номер изображения")
lblCheckRecognizedPattern.grid(column=0, row=rowCheckRecognizedPattern, pady=5)
txtCheckRecognizedPattern = Entry(window, width=10, textvariable=valRecognizedPattern)
txtCheckRecognizedPattern.grid(column=1, row=rowCheckRecognizedPattern)
txtCheckRecognizedPattern.insert(0, 254)




n_epochs = 0
batch_size_train = 64
batch_size_test = 1000
learning_rate = 0.01
momentum = 0.5
log_interval = 10

random_seed = 1
torch.backends.cudnn.enabled = False
torch.manual_seed(random_seed)

# загрузка датасета
train_loader = torch.utils.data.DataLoader(
  torchvision.datasets.MNIST('/files/', train=True, download=True,
                             transform=torchvision.transforms.Compose([
                               torchvision.transforms.ToTensor(),
                               torchvision.transforms.Normalize(
                                 (0.1307,), (0.3081,))
                             ])),
  batch_size=batch_size_train, shuffle=True)

test_loader = torch.utils.data.DataLoader(
  torchvision.datasets.MNIST('/files/', train=False, download=True,
                             transform=torchvision.transforms.Compose([
                               torchvision.transforms.ToTensor(),
                               torchvision.transforms.Normalize(
                                 (0.1307,), (0.3081,))
                             ])),
  batch_size=batch_size_test, shuffle=True)


examples = enumerate(test_loader)
batch_idx, (example_data, example_targets) = next(examples)


# просмотр датасета
'''
fig = plt.figure()
for i in range(6):
  plt.subplot(2,3,i+1)
  plt.tight_layout()
  plt.imshow(example_data[i][0], cmap='gray', interpolation='none')
  plt.title("Ground Truth: {}".format(example_targets[i]))
  plt.xticks([])
  plt.yticks([])
#fig
#plt.show()
'''


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)


network = Net()
optimizer = optim.SGD(network.parameters(), lr=learning_rate, momentum=momentum)

train_losses = []
train_counter = []
test_losses = []
test_counter = [i*len(train_loader.dataset) for i in range(n_epochs + 1)]


def train(epoch):
  network.train()
  for batch_idx, (data, target) in enumerate(train_loader):
    optimizer.zero_grad()
    output = network(data)
    loss = F.nll_loss(output, target)
    loss.backward()
    optimizer.step()
    if batch_idx % log_interval == 0:
      """print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
        epoch, batch_idx * len(data), len(train_loader.dataset),
        100. * batch_idx / len(train_loader), loss.item()))"""
      str = '\nTrain Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
        epoch, batch_idx * len(data), len(train_loader.dataset),
        100. * batch_idx / len(train_loader), loss.item())
      infoPanel.insert(INSERT, str)
      infoPanel.update()

      train_losses.append(loss.item())
      train_counter.append(
        (batch_idx*64) + ((epoch-1)*len(train_loader.dataset)))
      torch.save(network.state_dict(), 'model.pth')
      torch.save(optimizer.state_dict(), 'optimizer.pth')


def test():
  network.eval()
  test_loss = 0
  correct = 0
  with torch.no_grad():
    for data, target in test_loader:
      output = network(data)
      test_loss += F.nll_loss(output, target, size_average=False).item()
      pred = output.data.max(1, keepdim=True)[1]
      correct += pred.eq(target.data.view_as(pred)).sum()
  test_loss /= len(test_loader.dataset)
  test_losses.append(test_loss)
  """print('\nTest set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
    test_loss, correct, len(test_loader.dataset),
    100. * correct / len(test_loader.dataset)))"""
  str = '\nTest set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
    test_loss, correct, len(test_loader.dataset),
    100. * correct / len(test_loader.dataset))
  infoPanel.insert(INSERT, str)
  infoPanel.update()


def showChanceOfPatternDetection():
    output = network(example_data)

    y_hat = torch.argmax(output, dim=1)

    class_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    infoPanel.delete(1.0, END)
    infoPanel.insert(INSERT, 'Classification Report:\n')
    infoPanel.insert(INSERT, classification_report(example_targets[:], y_hat, target_names=class_names))

    conf = confusion_matrix(example_targets[:], y_hat)

    cmd1 = ConfusionMatrixDisplay(conf, display_labels=class_names)
    cmd1.plot()
    plt.show()


def trainModel():
    # тренровка модели №1 (предварительная)
    test()
    train(1)
    test()

    continued_network = Net()
    continued_optimizer = optim.SGD(network.parameters(), lr=learning_rate,
                                    momentum=momentum)

    network_state_dict = torch.load('model.pth')
    continued_network.load_state_dict(network_state_dict)

    optimizer_state_dict = torch.load('optimizer.pth')
    continued_optimizer.load_state_dict(optimizer_state_dict)

    # тренровка модели №2
    for i in range(2, n_epochs + 1):
        test_counter.append(i * len(train_loader.dataset))
        train(i)
        test()


def checkInputTrain():
    if valN_epochs.get() == '':
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Укажите кол-во эпох')
    elif valN_epochs.get().isdigit() is False:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Кол-во эпох должно быть целым числом')
    elif int(valN_epochs.get()) < 1:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Кол-во эпох не может быть меньше 1')
    else:
        global n_epochs
        n_epochs = int(valN_epochs.get())
        return True


def startTrain():
    if not checkInputTrain():
        return
    infoPanel.delete(1.0, END)
    trainModel()


def showRecognizedPatterns():
    numbersOfPatterns = [14, 29, 2, 8, 0, 10, 16, 19, 4, 32]

    for i in range(10):
        j = numbersOfPatterns[i]
        #plt.subplot(2, 3, i + 1)
        plt.subplot(3, 4, i + 1)
        plt.tight_layout()
        plt.imshow(example_data[j][0], cmap='gray', interpolation='none')
        plt.title("The number: {}".format(example_targets[j]))
        plt.xticks([])
        plt.yticks([])
    plt.show()


def showRecognizedPattern():
    output = network(example_data)
    #i = 255
    i = int(valRecognizedPattern.get())

    plt.close()

    plt.tight_layout()
    plt.imshow(example_data[i][0], cmap='gray', interpolation='none')
    plt.title("Prediction: {}".format(
        output.data.max(1, keepdim=True)[1][i].item()))
    plt.xticks([])
    plt.yticks([])
    plt.show()


def checkInputCheckRecognizedPattern():
    if valRecognizedPattern.get() == '':
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Укажите номер изображения')
        return False
    elif valRecognizedPattern.get().isdigit() is False:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Номер изображения должен быть целым числом')
        return False
    elif int(valRecognizedPattern.get()) < 0 or int(valRecognizedPattern.get()) > 999:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Номер изображения не может быть меньше 1 или больше 999')
        return False
    else:
        return True


def checkRecognizedPattern():
    if not checkInputCheckRecognizedPattern():
        return
    showRecognizedPattern()



btnShowRecognizedPatterns = Button(window, text="Перечень распознаваемых образов", command=showRecognizedPatterns)
btnShowRecognizedPatterns.grid(column=0, row=rowShowRecognizedPatterns, columnspan=2, padx=5, pady=5)

btnChanceOfPatternDetection = Button(window, text="Вероятность определения образа", command=showChanceOfPatternDetection)
btnChanceOfPatternDetection.grid(column=0, row=rowChanceOfPatternDetection, columnspan=2, padx=5, pady=5)

btnStartTrain = Button(window, text="Начать тренировку модели", command=startTrain)
btnStartTrain.grid(column=2, row=rowTrainModel, columnspan=2, padx=0, pady=5, sticky= W)

btnCheckRecognizedPattern = Button(window, text="Распознать", command=checkRecognizedPattern)
btnCheckRecognizedPattern.grid(column=2, row=rowCheckRecognizedPattern, padx=0, pady=5, sticky= W)

infoPanel = scrolledtext.ScrolledText(window, width=65, height=23)
infoPanel.grid(column=0, row=rowScrolledText, columnspan=4, padx=5)

#rowCheckRecognizedPattern

window.mainloop()
