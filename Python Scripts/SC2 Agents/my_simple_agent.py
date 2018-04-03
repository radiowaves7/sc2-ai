from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

import random

import numpy


# Functions
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id

_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_TRAIN_SCV = actions.FUNCTIONS.Train_SCV_quick.id

_NO_OP = actions.FUNCTIONS.no_op.id

_SELECT_POINT = actions.FUNCTIONS.select_point.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id

_RALLY_UNITS_MINIMAP = actions.FUNCTIONS.Rally_Units_minimap.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id

_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id

# Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Unit IDs
_TERRAN_BARRACKS = 21
_TERRAN_COMMANDCENTER = 18
_TERRAN_SUPPLYDEPOT = 19
_TERRAN_SCV = 45

# Parameters
_PLAYER_SELF = 1
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_SUPPLY_USED = 3
_SUPPLY_MAX = 4
_SCREEN = [0]
_MINIMAP = [1]
_QUEUED = [1]
_NOADD = [0]
_NOT_QUEUED = [0]
_SELECT_ALL = [0]


class SimpleAgent(base_agent.BaseAgent):
    """An agent spcifically for solving the Simple64 map."""
    
    
    base = None
    base_coord = [0,0]
    supply_depot_count = 0
    scv_selected = False
    barracks_count = 0
    barracks_rallied = False
    barracks_selected = False
    army_attacked = False
    army_selected = False
    
    
    def setup(self, obs_spec, action_spec):
        self.reward = 0
        self.episodes = 0
        self.steps = 0
        self.obs_spec = obs_spec
        self.action_spec = action_spec
        self.base = None
        self.base_coord = [0,0]
        self.supply_depot_count = 0
        self.scv_selected = False
        self.barracks_count = 0
        self.barracks_rallied = False
        self.barracks_selected = False
        self.army_attacked = False
        self.army_selected = False
    
    
    def reset(self):
        self.episodes += 1
        self.base = None
        self.base_coord = [0,0]
        self.supply_depot_count = 0
        self.scv_selected = False
        self.barracks_count = 0
        self.barracks_rallied = False
        self.barracks_selected = False
        self.army_attacked = False
        self.army_selected = False
    
    
    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base:
            return [x - x_distance, y - y_distance]
        
        return [x + x_distance, y + y_distance]
    
    
    def getRandomLocation(self, x, y):
        target = self.transformLocation(int(x.mean()), random.randint(0, 15), int(y.mean()), random.randint(0, 15))
        return target
    
    
    def step(self, obs):
        self.steps += 1
        self.reward += obs.reward
        super(SimpleAgent, self).step(obs)
        
        if self.base is None:
            player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
            self.base = player_y.mean() <= 31
            
        if self.supply_depot_count == 0:
            if not self.scv_selected:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()
                if unit_y.any():
                    i = random.randint(0, len(unit_y) - 1)
                    target = [unit_x[i], unit_y[i]]
                self.scv_selected = True    
                return actions.FunctionCall(_SELECT_POINT, [_SCREEN, target])
            elif _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
                
                #target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 20)
                target = self.getRandomLocation(unit_x, unit_y)
                ##target = self.getPlacementLocation(unit_x, unit_y)
                
                #self.supply_depot_count += 1
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_SUPPLYDEPOT).nonzero()
                if  unit_y.any():
                    self.supply_depot_count = (len(unit_y) - 1)
                else:
                    self.supply_depot_count = 0
                    
                return actions.FunctionCall(_BUILD_SUPPLYDEPOT, [_SCREEN, target])
        
        elif self.barracks_count == 0:
            if not self.scv_selected:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()
                if unit_y.any():
                    i = random.randint(0, len(unit_y) - 1)
                    target = [unit_x[i], unit_y[i]]
                self.scv_selected = True    
                return actions.FunctionCall(_SELECT_POINT, [_SCREEN, target])
            elif _BUILD_BARRACKS in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
                
                #target = self.transformLocation(int(unit_x.mean()), 20, int(unit_y.mean()), 0)
                target = self.getRandomLocation(unit_x, unit_y)
                
                #self.barracks_count += 1
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()
                if unit_y.any():
                    self.barracks_count = (len(unit_y) - 1)
                else:
                    self.barracks_count = 0
                    
                return actions.FunctionCall(_BUILD_BARRACKS, [_SCREEN, target])
        
        elif not self.barracks_rallied:
            if not self.barracks_selected:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()        
                if unit_y.any():
                    target = [int(unit_x.mean()), int(unit_y.mean())]        
                    self.barracks_selected = True
                    self.scv_selected = False
                    return actions.FunctionCall(_SELECT_POINT, [_SCREEN, target])
            else:
                self.barracks_rallied = True        
                if self.base:
                    return actions.FunctionCall(_RALLY_UNITS_MINIMAP, [_MINIMAP, [29, 21]])
                return actions.FunctionCall(_RALLY_UNITS_MINIMAP, [_MINIMAP, [29, 46]])
        
        elif obs.observation["player"][_SUPPLY_USED] < obs.observation["player"][_SUPPLY_MAX]:
            if not self.barracks_selected:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()        
                if unit_y.any():
                    target = [int(unit_x.mean()), int(unit_y.mean())]        
                    self.barracks_selected = True
                    self.scv_selected = False
                    self.army_selected = False
                    return actions.FunctionCall(_SELECT_POINT, [_SCREEN, target])
            elif _TRAIN_MARINE in obs.observation["available_actions"]:
                return actions.FunctionCall(_TRAIN_MARINE, [_QUEUED])
        
        else:
            if self.army_attacked == True:
                if not self.scv_selected:
                    unit_type = obs.observation["screen"][_UNIT_TYPE]
                    unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()
                    if unit_y.any():
                        i = random.randint(0, len(unit_y) - 1)
                        target = [unit_x[i], unit_y[i]]
                    self.scv_selected = True
                    self.barracks_selected = False
                    self.army_selected = False
                    return actions.FunctionCall(_SELECT_POINT, [_SCREEN, target])
                elif _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                    unit_type = obs.observation["screen"][_UNIT_TYPE]
                    unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
                    
                    #target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 20)
                    target = self.getRandomLocation(unit_x, unit_y)
                    ##target = self.getPlacementLocation(unit_x, unit_y)
                    
                    #self.supply_depot_count += 1
                    unit_type = obs.observation["screen"][_UNIT_TYPE]
                    unit_y, unit_x = (unit_type == _TERRAN_SUPPLYDEPOT).nonzero()
                    if  unit_y.any():
                        self.supply_depot_count = (len(unit_y) - 1)
                    else:
                        self.supply_depot_count = self.supply_depot_count
                        
                    return actions.FunctionCall(_BUILD_SUPPLYDEPOT, [_SCREEN, target])
                elif _BUILD_BARRACKS in obs.observation["available_actions"]:
                    unit_type = obs.observation["screen"][_UNIT_TYPE]
                    unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
                    
                    #target = self.transformLocation(int(unit_x.mean()), 20, int(unit_y.mean()), 0)
                    target = self.getRandomLocation(unit_x, unit_y)
                    
                    #self.barracks_count += 1
                    unit_type = obs.observation["screen"][_UNIT_TYPE]
                    unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()
                    if unit_y.any():
                        self.barracks_count = (len(unit_y) - 1)
                        self.army_attacked = False
                    else:
                        self.barracks_count = self.barracks_count                    
                        self.army_attacked = True
                    
                    return actions.FunctionCall(_BUILD_BARRACKS, [_SCREEN, target])
                
            elif not self.army_selected:
                    if _SELECT_ARMY in obs.observation["available_actions"]:
                        self.army_selected = True
                        self.barracks_selected = False
                        return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
            elif _ATTACK_MINIMAP in obs.observation["available_actions"]:
                self.army_attacked = True
                player_relative = obs.observation["minimap"][_PLAYER_RELATIVE]
                hostile_y, hostile_x = (player_relative == _PLAYER_HOSTILE).nonzero()
                if not hostile_y.any():
                    if self.base:
                        return actions.FunctionCall(_ATTACK_MINIMAP, [[1], [39, 45]])
                    return actions.FunctionCall(_ATTACK_MINIMAP, [[1], [21, 24]])
                index = numpy.argmax(hostile_y)
                target = [hostile_x[index], hostile_y[index]]
                return actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, target])
                
        
        return actions.FunctionCall(_NO_OP, [])