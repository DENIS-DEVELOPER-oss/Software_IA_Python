
import torch.nn as nn
import torchvision.models as models


class modelo_para_prediccion(nn.Module):
    def __init__(self, model_name="modelo_para_prediccion", targets=5, pretrained=False):
        super().__init__()
        self.model = models.resnext50_32x4d()
        n_features = self.model.fc.in_features
        self.model.fc = nn.Linear(n_features, targets)

    def forward(self, x):
        x = self.model(x)
        return x

