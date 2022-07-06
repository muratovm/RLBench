import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='tictactoe-v0',
    entry_point='gym_tictactoe.env:TicTacToeEnv'
)
