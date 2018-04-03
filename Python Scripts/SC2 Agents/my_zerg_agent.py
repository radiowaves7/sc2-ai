from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

#Actions
_no_op = actions.FUNCTIONS.no_op.id
_move_camera = actions.FUNCTIONS.move_camera.id
_select_point = actions.FUNCTIONS.select_point.id
_select_control_group = actions.FUNCTIONS.select_control_group.id

_select_larva = actions.FUNCTIONS.select_larva.id
_train_drone = actions.FUNCTIONS.Train_Drone_quick.id

#Screen
_unit_type = features.SCREEN_FEATURES.unit_type.index


#Player information
_minerals = 1
_gas = 2
_supply_used = 3
_supply_max = 4
_supply_army = 5
_supply_workers = 6
_idle_workers = 7
_army = 8
_larva = 10

#IDs
_infested_terran = 9
_baneling_cocoon = 1886
_baneling = 30153
_changeling = 601
_changeling_zealot = 413
_changeling_marine_shield = 375
_changeling_marine = 189
_changeling_ling_wings = 215
_changeling_ling = 30
_hatchery = 14783
_creeptumor = 11033
_extractor = 16391
_spawning_pool = 3984
_evo_chamber = 3900
_hydra_den = 878
_spire = 799
_ultra_cavern = 179
_infest_pit = 729
_nydus_network = 118
_bane_nest = 1718
_roach_warren = 1774
_spine = 5073
_spore = 6717
_hatchery_lair = 1335
_hatchery_hive = 176
_spire_greater = 19
_egg = 9930
_drone = 1230660
_zergling = 201575
_overlord = 34652
_hydra = 34836
_muta = 13423
_ultra = 2104
_roach = 47483
_infestor = 1156
_corruptor = 5346
_broodlord_cacoon = 38
_broodlord = 1250
_bane_b = 2
_drone_b = 33
_hydra_b = 1
_roach_b = 202
_ling_b = 76
_queen_b = 1
_queen = 12086
_infestor_b = 364
_overlord_cacoon = 73
_overseer = 3891
_creep_tumor_b = 9990
_creep_tumor_q = 5400
_spine_u = 131
_spore_u = 65
_nydus_canal = 186
_infested_terran_egg = 581
_larva = 168703
_broodling = 27568
_locust = 3152
_swarm_b = 89
_swarm = 2145
_viper = 733
_lurker_egg = 68
_lurker = 1175
_lurker_b = 542
_lurker_den = 61
_ravager_cacoon = 146
_ravager = 3880
_locust_fly = 1490
_parasitic = 41
_droplord_cacoon = 8
_droplord = 236

#
_screen = [0]
_queue = [1]

class SimpleAgent(base_agent.BaseAgent):
    """An agent spcifically for solving the Simple64 map."""
    
    def setup(self, obs_spec, action_spec):
        self.reward = 0
        self.episodes = 0
        self.steps = 0
        self.obs_spec = obs_spec
        self.action_spec = action_spec
        
    def reset(self):
        self.episodes += 1
        
    def step(self, obs):
        self.steps += 1
        self.reward += obs.reward
        super(SimpleAgent, self).step(obs)
        
        #print(obs.observation["available_actions"])
        #print("minerals = ", obs.observation["player"][_minerals])
        #print("gas = ", obs.observation["player"][_gas])
        
        """
        if (obs.observation["player"][_minerals] >= 50
            and obs.observation["player"][_larva] > 0
            and obs.observation["player"][_supply_workers] < 70):
            if not _select_larva in obs.observation["available_actions"]: 
                unit = obs.observastion["screen"][_unit_type]
                unit_y, unit_x = (unit == _hatchery).nonzero()
                target = [unit_x, unit_y]
                return actions.FunctionCall(_select_point, target)
            elif _train_drone in obs.observation["available_actions"]:
                return actions.FunctionCall(_train_drone, [_queue])
        """
        
        return actions.FunctionCall(_no_op, [])