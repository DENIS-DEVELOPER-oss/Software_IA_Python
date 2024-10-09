
import numpy as np
import pandas as pd
import torch
from functools import partial
import streamlit as st

from models import modelo_para_prediccion
from utils import CFG

import warnings

warnings.filterwarnings("ignore")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_state(model_path):
    model = modelo_para_prediccion(CFG.model_name, pretrained=False)
    model.load_state_dict(
        torch.load(model_path, map_location=torch.device("cpu"))["model"], strict=True
    )
    state_dict = torch.load(model_path, map_location=torch.device("cpu"))["model"]
    return state_dict

def inference(model, states, img, device):
    model.to(device)
    probs = []
    img = img.to(device)
    avg_preds = []
    for state in states:
        model.load_state_dict(state)
        model.eval()
        with torch.no_grad():
            preds = model(img)
        avg_preds.append(preds.softmax(1).to("cpu").numpy())
    avg_preds = np.mean(avg_preds, axis=0)
    probs.append(avg_preds)
    probs = np.concatenate(probs)
    return probs, preds
