import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='omnipath-v0',
    entry_point='gym_omnipath.envs:OmnipathEnv',
)
register(
    id='omnipath-extrahard-v0',
    entry_point='gym_omnipath.envs:OmnipathExtraHardEnv',
)