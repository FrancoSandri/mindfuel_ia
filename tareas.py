import pandas as pd
import tez
from sklearn import model_selection
import torch
import torch.nn as nn

class TareaDataset:
    def __init__(self,users,tareas,ratings):
        self.users = users
        self.tareas = tareas
        self.ratings = ratings
    
    def __len__(self):
        return len(self.users)

    def __getitem__(self,item):
        user = self.users[item]
        tarea = self.tareas[item]
        rating = self.ratings[item]
        return {"user":torch.tensor(user,dtype=torch.long),
        "movie":torch.tensor(tarea,dtype=torch.long),
        "rating": torch.tensor(rating,dtype=torch.float)}

def train():
    df = pd.read_csv("../input/puntuacion.csv")
    #ID, USER,TAREA_ID,RATING
    df_train, df_valid = model_selection.train_test_split(
        df,test_size = 0.1,random_state = 42, stratify = df.rating.values
    )
    train_dataset = TareaDataset(
        users = df_train.user.values, tareas = df_train.tarea.values, ratings = df_train.rating.values
    )

    valid_dataset = TareaDataset(
        users = df_valid.user.values, tareas = df_valid.tarea.values, ratings = df_valid.rating.values
    )

if __name__ == "__main__":
    train()