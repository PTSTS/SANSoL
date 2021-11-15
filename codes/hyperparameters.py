import optuna

from run import *
import sys
import random


def obj_sans(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)

