"""Game environment. Interaction with Markov Decision Process (MDP).

   @author
     Victor I. Afolabi
     Artificial Intelligence & Software Engineer.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: game.py
     Created on 09 September, 2018 @ 12:25 AM.

   @license
     MIT License
     Copyright (c) 2018. Victor I. Afolabi. All rights reserved.
"""
# Built-in libraries.

# Third-party libraries.
import gym
import numpy as np

__all__ = ['Game']


class Game(object):
    """Game is a representation of the environment which an agent interacts with.

    Methods:
        def __call__(self, policy, **kwargs):
            # Interact with the environment by taking actions & receiving rewards.

        def reset(self):
            # Place the agent in a random state.

        def render(self, suppress:Optional[bool]=False):
            # Renders the environment, if `suppress=True`, the render will be suppressed.

        def sample(self):
            # Returns a random action in the action space.

        def run(self, policy: Callable, episodes: int = 100, **kwargs):
            # Interact with the environment by taking actions & receiving rewards.

    Attributes:
        env (gym.env.Env): An initialized OpenAI gym environment.
        action_space (np.ndarray):
        observation_space (np.ndarray):
        actions (np.ndarray):
        observations (np.ndarray):
        state (np.ndarray): The current state of the agent.
        n_actions (int): Number of possible actions to be taken in the environment.
        n_observation (int): Number of observable states in the environment.
    """

    def __init__(self, env: str, **kwargs):
        # Initialize the GYM environment.
        self._env = gym.make(env)

        # Extract keyword arguments.
        seed = kwargs.get('seed', None)
        self._env.seed(seed=seed)

        # Get the action & observation spaces.
        self._actions = self._get_space(self._env.action_space)
        self._observations = self._get_space(self._env.observation_space)
        self._state = self._env.reset()

    def __repr__(self):
        return 'Game(env={})'.format(self._env.env)

    def __call__(self, policy, **kwargs):
        return self.run(policy, *kwargs)

    def reset(self):
        """Place the agent in a random state.

        Returns:
            np.ndarray: State where the agent is being placed in.
        """

        self._state = self._env.reset()
        return self._state

    def step(self, action):
        return self._env.step(action)

    def transition(self, state: int, action: int):
        """Transition function i.e. T(s' | s, a) or P(next state | state, action).

        Args:
            state (int): Current state of the agent.
            action (int): Action to be taken by the agent.

        Returns:
            List[Tuple[float, int, float, bool]] - Probability of getting to the
            next state, the next state (s'), reward R(s, a), done or not - for ever

            e.g [(0.3333333333333333, 0, 0.0, False),
                 (0.3333333333333333, 0, 0.0, False),
                 (0.3333333333333333, 4, 0.0, False)]
        """
        return self._env.env.P[state][action]

    def render(self, suppress=False):
        """Renders the environment, if `suppress=True`, the render will be suppressed.

        Args:
            suppress (bool, optional): Defaults to False.
                If set to `True`, the environment will not be rendered.
        """

        if not suppress:
            self._env.render()

    def sample(self):
        """Returns a random action in the action space.

        Returns:
            int: A single integer representing which (random) action to take.
        """
        return self._env.action_space.sample()

    def run(self, policy, episodes: int = 100, **kwargs):
        """Interact with the environment by taking actions & receiving rewards.

        Args:
            policy (Callable): An instance of policy.BasePolicy that tells
                the agent what actions to take.
            episodes (int, optional): Defaults to 100. How many episodes to be run.

        Returns:
            int: Total accumulated rewards.
        """

        # Default keyword arguments.
        render = kwargs.get('render', False)

        # Observation & total reward.
        obs, total_rewards = self._env.reset(), 0

        for episode in range(episodes):
            # Render env.
            if render:
                self._env.render()

            # Get an action.
            action = policy(obs, **kwargs)
            self._state, reward, done, info = self._env.step(action)
            total_rewards += reward

            if done:
                break

        return total_rewards

    @staticmethod
    def _get_space(space):
        # Discrete => n, shape
        if isinstance(space, gym.spaces.Discrete):
            return np.arange(space.n)

        # Box: low, high, shape
        elif isinstance(space, gym.spaces.Box):
            return space.low

        return np.zeros(shape=space.shape)

    @property
    def env(self):
        return self._env

    @property
    def action_space(self):
        # return self._env.action_space
        return self._actions.shape

    @property
    def observation_space(self):
        # return self._env.observation_space
        return self._observations.shape

    @property
    def state(self):
        return self._state

    @property
    def actions(self):
        return self._actions

    @property
    def observations(self):
        return self._observations

    @property
    def n_actions(self):
        return len(self._actions)

    @property
    def n_states(self):
        return len(self._observations)
