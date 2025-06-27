import torch
import os
import model as Model
import argparse
import logging
import core.logger as Logger
import core.metrics as Metrics
from core.wandb_logger import WandbLogger
from tensorboardX import SummaryWriter
from dataset import Data_set
import warnings
warnings.filterwarnings("ignore")
os.environ['WANDB_MODE'] = 'disabled'

def parse_args():
    parse = argparse.ArgumentParser(description="New Network")
    parse.add_argument('--config', type=str, default='config/config_train.json')
    parse.add_argument('-p', '--phase', type=str, choices=['train', 'val'], default='train')
    parse.add_argument('-gpu', '--gpu_ids', type=str, default=None)
    parse.add_argument('-d', '--debug', action='store_true')
    parse.add_argument('-enable_wandb', default=True, action='store_true')
    parse.add_argument('-log_wandb_ckpt', action='store_true')
    parse.add_argument('-log_eval', action='store_true')
    args = parse.parse_args()
    return args