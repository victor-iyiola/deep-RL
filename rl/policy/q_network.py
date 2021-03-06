"""Q-Learning with function approximation & Bellman Equation.

   @author
     Victor I. Afolabi
     Artificial Intelligence & Software Engineer.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: q_network.py
     Created on 10 September, 2018 @ 12:57 AM.

   @license
     MIT License
     Copyright (c) 2018. Victor I. Afolabi. All rights reserved.
"""
from rl.policy.base import BasePolicy


class QNetwork(BasePolicy):
    def __init__(self, **kwargs):
        super(QNetwork, self).__init__(**kwargs)

    def get(self, state, **kwargs):
        pass
