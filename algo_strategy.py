import gamelib
import random
import math
import warnings
from sys import maxsize
import json

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        self.scored_on_locations = []

    def on_turn(self, turn_state):
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        self.starter_strategy(game_state)
        game_state.submit_turn()
    # def turn_strategy(self, game_state):
    #     # Check for delayed attack strategy
    #     self.attack_delay -= 1
    #     if self.attack_delay < 0:
    #         self.attack_status = "NO_ATTACK"
    #         self.build_exceptions = []
    #     else: 
    #         self.attack_status = "WAITING_TO_ATTACK"
        
        # Build Intial Defense Configuration on Turn 0
        # if game_state.turn_number == 0:
        #     self.build_initial_defenses(game_state)
        #     self.remove_base_buildings(game_state)
        #     return
        
        # # Build Core Defenses
        # self.build_defenses(game_state, self.core_queue)

        # # Offensive Moves
        # self.determine_attack_strategy(game_state)

        # # Defensive Moves
        # self.build_additional_defenses(game_state)
        # self.remove_base_buildings(game_state)
    def previous_turn_points(self, game_state):
        ten_turn_number = (game_state.turn_number+1)//10
        return (12-(5+ten_turn_number))*(4/3)


    def starter_strategy(self, game_state):
        if game_state.turn_number == 0:
            self.build_defences2(game_state)
            #self.turn0_scout(game_state)
            # if self.can_inflitrator_cheese(game_state):
            #     game_state.attempt_remove([[2,13],[3,13]])

            
        if game_state.turn_number in [1,2,3,4,5] and game_state.get_resource(1,1) >= 8:
            self.build_midgame_defences2(game_state)
            # self.inflitrator_cheese(game_state)
            game_state.attempt_spawn(INTERCEPTOR,[6,7],1)
            game_state.attempt_spawn(INTERCEPTOR,[21,7],1)
            
        if game_state.turn_number in [6,7] and game_state.get_resource(1,1) >= 12:
            self.build_midgame_defences2(game_state)
            # self.inflitrator_cheese(game_state)
            game_state.attempt_spawn(INTERCEPTOR,[10,3],1)
            game_state.attempt_spawn(INTERCEPTOR,[17,3],1)
            
            
        else:
            # Now let's analyze the enemy base to see where their defenses are concentrated.
            # If they have many units in the front we can build a line for our demolishers to attack them at long range.
            if False:#self.scored_on_locations(game_state):
                return
            else:
                #if game_state.turn_number <= 4:
                    #game_state.attempt_spawn(INTERCEPTOR,[7,6],1)
                    #game_state.attempt_spawn(INTERCEPTOR,[20,6],1)
                    

                
                if game_state.turn_number % 3 == 2:
                    self.build_midgame_defences2(game_state)
                if game_state.turn_number % 3 == 0 and game_state.turn_number > 4 and game_state.get_resource(MP) >= self.previous_turn_points(game_state)-0.1:
                    self.demolish_corner(game_state)
                elif game_state.turn_number % 3 == 1 and game_state.turn_number > 4 and game_state.get_resource(MP) >= 12:
                    self.corner_scout_attack(game_state)
                else:
                    self.build_midgame_defences2(game_state)
                self.support_towers(game_state)
                
                
                
    def can_inflitrator_cheese(self,game_state):
        self.detect_enemy_unit(game_state, TURRET, [0,1,2,3,4,5], [14,15,16,17,18,19])
        if self.detect_enemy_unit(game_state, TURRET, [0,1,2,3,4,5], [14,15,16,17,18,19]) > 0:
            return False
        return True
        
                
                
                
    def inflitrator_cheese(self,game_state):
        game_state.attempt_spawn(DEMOLISHER, [1,12], 100)
        
        
                
    def corner_wall(self,game_state):
        wall_locations = [[0,13],[1,13],[2,13],[27,13],[26,13],[25,13]]
        game_state.attempt_spawn(WALL, wall_locations)
        game_state.attempt_upgrade(wall_locations)
        
    def support_towers(self,game_state):
        support_locations = [[13, 2], [14, 2], [13, 3], [14, 3],[13,4],[14,4],[12,4],[15,4],[11,5],[12,5],[13,5],[14,5],[15,5],[16,5],[17,5]]
        game_state.attempt_spawn(SUPPORT, support_locations)
        game_state.attempt_upgrade(support_locations)
        
                
    def demolish_corner(self,game_state):
        
        
        
        middle_wall_location = []
        wall_locations = [
            [2, 13], [3, 13],
            [25, 13], [24, 13],
            [4, 12], [23, 12],
            [5, 11], [22, 11],
            [6, 10], [21, 10],
            [7, 9], [20, 9],
            [8, 8], [19, 8],
            [9, 8], [18, 8], [10,8], [17,8], [11,8] ,[12,8],[16,8], [12,7], [15,7],[13,7],[14,7], [12,8], [15,8]]
        
        game_state.attempt_spawn(WALL, wall_locations)
        
        for i in [[13,6],[14,6]]:
            middle_wall_location.append(i)
        game_state.attempt_spawn(WALL, middle_wall_location)
        
        wall_locations = [[0,13],[1,13],[1,12],[2,12],[2,11],[3,11],[27,13],[26,13],[26,12],[25,12],[25,11],[24,11]]
        for location in wall_locations:
            game_state.attempt_remove(location)
        upgrade_walls = [[12,8],[15,8]]
        game_state.attempt_spawn(WALL, upgrade_walls)
        game_state.attempt_upgrade(upgrade_walls)
        
        
    def turn0_scout(self,game_state):
        deploy_locations = [[12,1],[15,1],[13,0],[14,0],[18,4],[9,4]] #[0,13],[27,13],
        deploy_locations = self.filter_blocked_locations(deploy_locations, game_state)
        damages = []
        for location in deploy_locations:
            path = game_state.find_path_to_edge(location)
            damage = 0
            if path is None:
                damage = maxsize
            else:
                for path_location in path:
                    damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(TURRET, game_state.config).damage_i
            damages.append(damage)
        
        attack_locations = deploy_locations[damages.index(min(damages))]
        game_state.attempt_spawn(SCOUT, attack_locations,50)        


    def build_defences2(self, game_state):
        # Wall configuration
        wall_locations = [
            [0, 13], [1, 13], [2, 13], [3, 13],
            [27, 13], [26, 13], [25, 13], [24, 13],
            [4, 12], [23, 12],
            [7, 9], [20, 9],
            [8, 8], [19, 8],
            [9, 8], [18, 8], [10,8], [17,8], [11,8], [12, 8], [16,8]]
        game_state.attempt_spawn(WALL, wall_locations)

        # Turret configuration
        turret_locations = [[3, 12], [24, 12]]
        game_state.attempt_spawn(TURRET, turret_locations)
        game_state.attempt_upgrade(turret_locations)





    def build_defences(self, game_state):
        wall_location = []
        for i in [0,1,2,25,26,27]:
            wall_location.append([i,13])
        for locations in [[3,12],[24,12],[4,11],[23,11],[11,11],[16,11]]:
            wall_location.append(locations)
        for i in range(5,11):
            wall_location.append([i,10])
        for i in range(17,23):
            wall_location.append([i,10])
        
        game_state.attempt_spawn(WALL, wall_location)
        turret_locations = [[11,10],[16,10]]
        game_state.attempt_spawn(TURRET, turret_locations)
        game_state.attempt_upgrade(turret_locations)
        
    def build_midgame_defences(self, game_state):
        wall_location = []
        for i in [0,1,2,25,26,27]:
            wall_location.append([i,13])
        for locations in [[3,12],[24,12],[4,11],[23,11],[11,11],[16,11]]:
            wall_location.append(locations)
        for i in range(5,11):
            wall_location.append([i,10])
        for i in range(17,23):
            wall_location.append([i,10])
        game_state.attempt_spawn(WALL, wall_location)
        game_state.attempt_spawn(WALL, [[13,8]])
        turret_locations = [[11,10],[16,10]]
        game_state.attempt_spawn(TURRET, turret_locations)
        game_state.attempt_upgrade(turret_locations)
        wall_location = [[13,11],[12,10],[15,10]]
        game_state.attempt_spawn(WALL, wall_location)
        turret_locations = [[11,9],[15,9]]
        game_state.attempt_spawn(TURRET, turret_locations)
        game_state.attempt_upgrade(turret_locations)
        wall_location = [[12,9],[14,9]]
        game_state.attempt_spawn(WALL, wall_location)
        turret_locations = [[11,8],[15,8]]
        wall_location = [[12,8],[14,8]]
        
    def build_midgame_defences2(self, game_state):
        #priority 0: fix walls
        for location in [[0,13],[1,13],[2,13],[3,13],[27,13],[26,13],[25,13],[24,13]]:
            game_state.attempt_spawn(WALL, location)
        
        for location in [[4,12],[23,12]]:
            game_state.attempt_upgrade(location)
        
        
        # Priority 1: Build and upgrade turrets at [11, 7] and [16, 7]
        priority_turrets = [[11, 7], [16, 7]]
        game_state.attempt_spawn(TURRET, priority_turrets)
        game_state.attempt_upgrade(priority_turrets)

        # Priority 2: Build walls starting from the highest y-coordinate
            
        wall_locations = [
            [0, 13], [1, 13], [2, 13], [3, 13],
            [27, 13], [26, 13], [25, 13], [24, 13],
            [4, 12], [23, 12],
            [5, 11], [22, 11],
            [6, 10], [21, 10],
            [7, 9], [20, 9],
            [8, 8], [19, 8],
            [9, 8], [18, 8], [10,8], [17,8], [11,8],[12,8], [15,8], [16,8], [12,7], [15,7],[13,6],[14,6]]
        
        game_state.attempt_upgrade([[2,13],[25,13]])
        
        if game_state.get_resource(1,1)> 13:
            game_state.attempt_spawn(WALL, [[1,12],[26,12]])
        
        # if game_state.turn_number in [1,2,3,4,5]:
        #     for i in [[6,10],[21,10]]:x
        #         wall_locations.remove(i)
            
            
        for location in wall_locations:
            game_state.attempt_spawn(WALL, location)

        # Priority 3: Build and upgrade remaining turrets
        remaining_turrets = [[3, 12], [24, 12], [11, 6], [16, 6]]
        for location in remaining_turrets:
            game_state.attempt_spawn(TURRET, location)
            game_state.attempt_upgrade(location)

        # Priority 4: Build and upgrade walls
        extra = [[13,7],[14,7],[12,8],[15,8]]
        for location in extra:
            game_state.attempt_spawn(WALL, location)

        # Upgrade walls if there are leftover resources
        ehhe =[[2,13],[25,13],[11,8],[16,8],[12,7],[15,7]]
        for location in ehhe:
            game_state.attempt_upgrade(location)




        
        
    wall_priority = [[3,13],[24,13],[9,10],[18,10]]
    
    def early_walls(self,game_state):
        #wall_locations = [[4,13],[3,13],[4,12],[26,13],[25,13],[24,13],[23,12]]
        wall_locations = [[3,13],[24,13],[9,10],[18,10],[5,12],[23,13],[24,13],[22,12],[4,13]] #Maybe add 0,13 27,13?
        game_state.attempt_spawn(WALL, wall_locations)
        game_state.attempt_upgrade(wall_locations)
        
    def early_middle_walls(self,game_state):
        #wall_locations = [[1,13],[2,13],[3,13],[4,12],[26,13],[25,13],[24,13],[23,12]]
        #game_state.attempt_spawn(WALL, wall_locations) #IDK IF working as intended, but basically i want to fix the side walls before building middle walls
        wall_locations = [[4,13],[3,13],[5,12],[23,13],[24,13],[22,12],[6,11],[7,10],[8,10],[9,10],[10,10],[21,11],[20,10],[19,10],[18,10],[17,10],[11,10],[12,10],[13,10],[14,10],[15,10],[16,10]]
        game_state.attempt_spawn(WALL, wall_locations)
        
    def corner_scout_attack(self,game_state):
        side_turret = [[3,12],[24,12]]
        game_state.attempt_spawn(TURRET, side_turret)
        game_state.attempt_upgrade(side_turret)
        
        
        
        wall_locations = [
            [2, 13], [3, 13],
             [25, 13], [24, 13],
            [4, 12], [23, 12],
            [5, 11], [22, 11],
            [6, 10], [21, 10],
            [7, 9], [20, 9],
            [8, 8], [19, 8],
            [9, 8], [18, 8], [10,8], [17,8], [11,8],[12,8],[15,8], [16,8], [12,7], [15,7],[13,6],[14,6],[13,7],[14,7],[12,6],[15,6]]
        game_state.attempt_spawn(WALL, wall_locations)
        game_state.attempt_remove([[13,6],[14,6]])
        location = [[0,14],[1,15],[2,16],[3,17],[27,14],[26,15],[25,16],[24,17]]
        deploy_locations = [[12,1],[15,1],[13,0],[14,0],[18,4],[9,4]] #[0,13],[27,13],
        deploy_locations = self.filter_blocked_locations(deploy_locations, game_state)
        damages = []
        for location in deploy_locations:
            path = game_state.find_path_to_edge(location)
            damage = 0
            if path is None:
                damage = maxsize
            else:
                for path_location in path:
                    damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(TURRET, game_state.config).damage_i
            damages.append(damage)
        
        attack_locations = deploy_locations[damages.index(min(damages))]

        
        isLeft = attack_locations[0] < 13
        if not isLeft:
            game_state.attempt_spawn(SCOUT, [13,0],5)
            wall = [[27,13],[26,13]]
            for i in wall:
                game_state.attempt_spawn(WALL, i)

            
        else:
            game_state.attempt_spawn(SCOUT, [14,0],5)
            wall = [[0,13],[1,13]]
            for i in wall:
                game_state.attempt_spawn(WALL, i)
            
            
        support_location = [attack_locations[0],attack_locations[1]+2]
        game_state.attempt_spawn(SUPPORT, support_location,1)
        
        
        game_state.attempt_spawn(SCOUT, attack_locations,50)
    
    # Additional walls or upgrades can be added here if resources allow

    def build_reactive_defense(self, game_state):
        """
        This function builds reactive defenses based on where the enemy scored on us from.
        We can track where the opponent scored by looking at events in action frames 
        as shown in the on_action_frame function
        """
        for location in self.scored_on_locations:
            # Build turret one space above so that it doesn't block our own edge spawn locations
            #build_location = [location[0], location[1]+1]
            game_state.early_walls(game_state)

    def stall_with_interceptors(self, game_state):
        """
        Send out interceptors at random locations to defend our base from enemy moving units.
        """
        # We can spawn moving units on our edges so a list of all our edge locations
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        
        # Remove locations that are blocked by our own structures 
        # since we can't deploy units there
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
        
        # While we have remaining MP to spend lets send out interceptors randomly.
        while game_state.get_resource(MP) >= game_state.type_cost(INTERCEPTOR)[MP] and len(deploy_locations) > 0:
            # Choose a random deploy location.
            deploy_location = [[4,9],[3,10]]
            
            game_state.attempt_spawn(INTERCEPTOR, deploy_location)
            """
            We don't have to remove the location since multiple mobile 
            units can occupy the same space.
            """

    def demolisher_line_strategy(self, game_state):
        """
        Build a line of the cheapest stationary unit so our demolisher can attack from long range.
        """
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [WALL, TURRET, SUPPORT]
        cheapest_unit = WALL
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost[game_state.MP] < gamelib.GameUnit(cheapest_unit, game_state.config).cost[game_state.MP]:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our demolisher from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
        for x in range(27, 5, -1):
            game_state.attempt_spawn(cheapest_unit, [x, 11])

        # Now spawn demolishers next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        game_state.attempt_spawn(DEMOLISHER, [24, 10], 1000)

    def least_damage_spawn_location(self, game_state, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to 
        estimate the path's damage risk.
        """
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy turrets that can attack each location and multiply by turret damage
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(TURRET, game_state.config).damage_i
            damages.append(damage)
        
        # Now just return the location that takes the least damage
        return location_options[damages.index(min(damages))]

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x = None, valid_y = None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y) and unit.get('attackRange', 0) > 3:
                        total_units += 1
        return total_units
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at in json-docs.html in the root of the Starterkit.
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly, 
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
