from model import LSTM
import torch
from sklearn.preprocessing import MinMaxScaler
from app.preprocess_data import preprocess_data
from pathlib import Path
import os
import numpy as np

def inference(i):
    model = LSTM()
    df_test_lst = preprocess_data()
    df_test = df_test_lst[i]

    train_window = 30
    PATH = os.path.join(Path(__file__).resolve().parent, f"model_pt_files/model_{i}.pt")
    fut_pred = 30
    test_data_size = 30
    train_data = df_test[:-test_data_size].to_numpy()

    scaler = MinMaxScaler(feature_range=(0, 1))
    train_data_normalized = scaler.fit_transform(train_data.reshape(-1, 1))
    train_data_normalized = torch.FloatTensor(train_data_normalized).view(-1)

    test_inputs = train_data_normalized[-train_window:].tolist()

    model.load_state_dict(torch.load(PATH))
    model.eval()

    for i in range(fut_pred):
        seq = torch.FloatTensor(test_inputs[-train_window:])
        with torch.no_grad():
            model.hidden = (torch.zeros(1, 1, model.hidden_layer_size),
                            torch.zeros(1, 1, model.hidden_layer_size))
            test_inputs.append(model(seq).item())

    actual_predictions = scaler.inverse_transform(np.array(test_inputs[train_window:] ).reshape(-1, 1))
    preds = np.where(actual_predictions < 0, 0, actual_predictions)
    return preds


if __name__ == '__main__':
    inference(i=0)