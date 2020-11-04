
import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()

        #create linear layer
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU() # activate function

    def forward(self, x):
        # layer 1
        out = self.l1(x)
        out = self.relu(out)
        # layer 2
        out = self.l2(out)
        out = self.relu(out)
        # layer 3
        out = self.l3(out)
        # no activation and no softmax at the end
        return out