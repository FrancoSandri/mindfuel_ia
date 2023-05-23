import pandas as pd
import tez
from sklearn import model_selection
import torch
import torch.nn as nn
from sklearn import metrics, preprocessing
import numpy as np

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
        "tarea":torch.tensor(tarea,dtype=torch.long),
        "rating": torch.tensor(rating,dtype=torch.float)}

class RecSysModel(tez.Model):
    def __init__(self,num_users,num_tareas):
        super().__init__()
        self.user_embed = nn.Embedding(num_users,32)
        self.tarea_embed = nn.Embedding(num_tareas,32)
        self.out = nn.Linear(64,1)
        self.step_scheduler_after = "epoch"

    def fetch_optimizer(self):
        opt = torch.optim.Adam(self.parameters(), lr =1e-3)
        return opt
    
    def fetch_scheduler(self):
        sch = torch.optim.lr_scheduler.StepLR(self.optimizer, step_size = 3, gamma=0.7)
        return sch

    def monitor_metrics(self, output, rating):
        output = output.detach().cpu().munpy()
        rating = rating.detach().cpu().numpy()
        return{'rmse': np.sqrt(metrics.mean_squared_error(rating, output))}

    def forward(self, users,tareas,ratings=None):
        users = users.to(torch.device("cpu"))
        tareas = tareas.to(torch.device("cpu"))
        ratings = ratings.to(torch.device("cpu"))

        user_embeds = self.user_embed(users)
        tarea_embeds = self.tarea_embed(tareas)
        output = torch.cat([user_embeds,tarea_embeds],dim= 1)
        output = self.out(output)
        loss = nn.MSELoss()(output,ratings.view(-1,1))
        calc_metrics = self.monitor_metrics(output,ratings.view(-1,1))
        return output, loss, calc_metrics

def train():
    df = pd.read_csv("../input/puntuacion.csv")
    #ID, USER,TAREA_ID,RATING
    lbl_user = preprocessing.LabelEncoder()
    lbl_tarea = preprocessing.LabelEncoder()

    df.user_id = lbl_user.fit_transform(df.user_id.values)
    df.tarea_id = lbl_tarea.fit_transform(df.tarea_id.values)
    
    df_train, df_valid = model_selection.train_test_split(
        df,test_size = 0.1,random_state = 42, stratify = df.rating.values
    )
    train_dataset = TareaDataset(
        users = df_train.user_id.values, tareas = df_train.tarea_id.values, ratings = df_train.rating.values
    )

    valid_dataset = TareaDataset(
        users = df_valid.user_id.values, tareas = df_valid.tarea_id.values, ratings = df_valid.rating.values
    )

    model = RecSysModel(num_users = len(lbl_user.classes_),num_tareas = len(lbl_tarea.classes_))
    model.fit(
        train_dataset,valid_dataset,train_bs = 1024,
        valid_bs = 1024,fp16 = True
    )

if __name__ == "__main__":
    train()