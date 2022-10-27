import torch
import torch.nn as nn
import torch.optim as optim
from model import LSTM
from sklearn.preprocessing import MinMaxScaler
from preprocess_data import preprocess_data
from pathlib import Path
import os

def create_inout_sequences(input_data, tw):
    inout_seq = []
    L = len(input_data)
    for i in range(L-tw):
        train_seq = input_data[i:i+tw]
        train_label = input_data[i+tw:i+tw+1]
        inout_seq.append((train_seq ,train_label))
    return inout_seq


def train(train_data_normalized, train_window, i):
    train_inout_seq = create_inout_sequences(train_data_normalized, train_window)
    epochs = 30

    model = LSTM()
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    # 경로 지정
    PATH = os.path.join(Path(__file__).resolve().parent, f"model_pt_files/model_{i}.pt")

    for i in range(epochs):
        for seq, labels in train_inout_seq:
            optimizer.zero_grad()
            model.hidden_cell = (torch.zeros(1, 1, model.hidden_layer_size),
                            torch.zeros(1, 1, model.hidden_layer_size))

            y_pred = model(seq)

            single_loss = loss_function(y_pred, labels)
            single_loss.backward()
            optimizer.step()

        if i%25 == 1:
            print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')
        
        if i == epochs-1:
            print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')
            torch.save(model.state_dict(), PATH)


if __name__ == '__main__':

    train_window = 30
    df_test_lst = preprocess_data()

    for i in range(25):
        print(f'{i} region training...', df_test_lst[i].shape)
        test_data_size = df_test_lst[i].shape[0]-30

        train_data = df_test_lst[i][:-test_data_size].to_numpy()
        test_data = df_test_lst[i][-test_data_size:].to_numpy()

        scaler = MinMaxScaler(feature_range=(0, 1))
        train_data_normalized = scaler.fit_transform(train_data.reshape(-1, 1))
        train_data_normalized = torch.FloatTensor(train_data_normalized).view(-1)

        train(train_data_normalized, train_window, i)