from collections import deque
import random

# Linked List Implementation for Quest Log
class QuestNode:
    def __init__(self, event, timestamp=None):
        self.event = event
        self.timestamp = timestamp or self.get_current_turn()
        self.next = None
    
    def get_current_turn(self):
        # Simple turn counter
        return getattr(QuestNode, 'turn_counter', 0)

class QuestLog:
    def __init__(self):
        self.head = None
        self.size = 0
        QuestNode.turn_counter = 0
    
    def add_event(self, event):
        QuestNode.turn_counter += 1
        new_node = QuestNode(event)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def get_recent_events(self, count=5):
        events = []
        current = self.head
        while current:
            events.append(f"Turn {current.timestamp}: {current.event}")
            current = current.next
        return events[-count:] if len(events) > count else events
    
    def get_all_events(self):
        events = []
        current = self.head
        while current:
            events.append(f"Turn {current.timestamp}: {current.event}")
            current = current.next
        return events

# Recursive Pathfinding with Fog of War
class PathfindingSystem:
    @staticmethod
    def has_path_to_goal(game_map, start_x, start_y, goal_symbol='G', visited=None):
        """Recursive pathfinding to check if goal is reachable"""
        if visited is None:
            visited = set()
        
        # Boundary checks
        if (start_x < 0 or start_y < 0 or 
            start_x >= len(game_map) or start_y >= len(game_map[0])):
            return False
        
        # Wall or already visited
        if game_map[start_x][start_y] == '#' or (start_x, start_y) in visited:
            return False
        
        # Found goal
        if game_map[start_x][start_y] == goal_symbol:
            return True
        
        visited.add((start_x, start_y))
        
        # Recursive exploration in all directions
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # N, S, E, W
        for dx, dy in directions:
            if PathfindingSystem.has_path_to_goal(game_map, start_x + dx, start_y + dy, goal_symbol, visited):
                return True
        
        return False
    
    @staticmethod
    def reveal_fog_of_war(game_map, x, y, revealed, radius=1):
        """Recursive fog of war revealing with limited radius"""
        if (x < 0 or y < 0 or x >= len(game_map) or y >= len(game_map[0]) or 
            (x, y) in revealed or radius < 0):
            return
        
        revealed.add((x, y))
        
        if radius > 0:
            # Recursively reveal adjacent cells with decreasing radius
            directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                PathfindingSystem.reveal_fog_of_war(game_map, x + dx, y + dy, revealed, radius - 1)

# Matrix and List Operations
class GameWorld:
    def __init__(self):
        # 2D Matrix for game map 
        self.game_map = [
            ['#', '#', '#', '#', '#', '#'],
            ['#', 'S', '.', '.', 'M', '#'],
            ['#', '.', '#', 'I', '.', '#'],
            ['#', '.', '.', '#', '.', '#'],
            ['#', 'I', '.', '.', 'G', '#'],
            ['#', '#', '#', '#', '#', '#']
        ]
        
        # 1D List for inventory
        self.inventory = []
        self.max_inventory_size = 10
        
        # Additional matrix operations
        self.trap_locations = [(2, 1), (3, 3)]  # Hidden traps
        self.treasure_values = {
            'I': random.randint(10, 50),  # Random treasure values
            'rare_gem': 100
        }
    
    def get_map_dimensions(self):
        """Matrix dimension analysis"""
        return len(self.game_map), len(self.game_map[0])
    
    def count_map_elements(self):
        """Matrix traversal and counting"""
        counts = {}
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map[0])):
                element = self.game_map[i][j]
                counts[element] = counts.get(element, 0) + 1
        return counts
    
    def get_submatrix_around_player(self, player_pos, radius=1):
        """Submatrix extraction"""
        x, y = player_pos
        submatrix = []
        for i in range(max(0, x - radius), min(len(self.game_map), x + radius + 1)):
            row = []
            for j in range(max(0, y - radius), min(len(self.game_map[0]), y + radius + 1)):
                row.append(self.game_map[i][j])
            submatrix.append(row)
        return submatrix

# Main Game Class
class DungeonCrawler:
    def __init__(self):
        self.world = GameWorld()
        self.player_pos = [1, 1]  # Starting position
        self.quest_log = QuestLog()  # Linked List
        self.move_stack = []  # Stack for undo
        self.npc_action_queue = deque()  # Queue for NPC actions
        self.revealed_cells = set()  # Fog of war
        self.game_over = False
        self.turn_count = 0
        
        # Initialize game
        self.initialize_game()
    
    def initialize_game(self):
        """Game initialization function"""
        PathfindingSystem.reveal_fog_of_war(
            self.world.game_map, 
            self.player_pos[0], 
            self.player_pos[1], 
            self.revealed_cells, 
            radius=2
        )
        self.quest_log.add_event("Entered the Dungeon")
        self.populate_npc_queue()
    
    def populate_npc_queue(self):
        """Queue operations or populate NPC actions"""
        npc_actions = [
            "Goblin scout spotted you!",
            "Distant growling echoes through the dungeon",
            "A rat scurries past your feet",
            "You hear footsteps approaching",
            "Something watches you from the shadows"
        ]
        for action in npc_actions:
            self.npc_action_queue.append(action)
    
    def display_game_state(self):
        """Display function with comprehensive game state"""
        print("=" * 60)
        print("🏰 DUNGEON CRAWLER 🏰")
        print("=" * 60)
        
        # Legend
        print("\n📋 LEGEND:")
        legend = {
            'S': 'Start Point', 'P': 'Player (You)', 'G': 'Goal/Exit',
            '#': 'Wall', 'I': 'Item/Treasure', 'M': 'Monster',
            '.': 'Open Path', '?': 'Unexplored Area'
        }
        for symbol, meaning in legend.items():
            print(f"   {symbol} - {meaning}")
        
        # Map display with coordinates
        print(f"\n🗺️  DUNGEON MAP:")
        print("    " + "".join(f"{j:3}" for j in range(len(self.world.game_map[0]))))
        
        for i in range(len(self.world.game_map)):
            row_display = f"{i:2}  "
            for j in range(len(self.world.game_map[0])):
                if [i, j] == self.player_pos:
                    cell = 'P'
                elif (i, j) in self.revealed_cells:
                    cell = self.world.game_map[i][j]
                else:
                    cell = '?'
                row_display += f"{cell:3}"
            print(row_display)
        
        # Game statistics 
        print("\n┌─ 📊 GAME STATUS " + "─" * 39 + "┐")
        print(f"│ 🎯 Position: ({self.player_pos[0]}, {self.player_pos[1]})".ljust(58) + "│")
        
        inv_text = f"🎒 Inventory ({len(self.world.inventory)}/{self.world.max_inventory_size})"
        if self.world.inventory:
            inv_display = ", ".join(self.world.inventory[:2])
            if len(self.world.inventory) > 2:
                inv_display += f" +{len(self.world.inventory)-2} more"
        else:
            inv_display = "Empty"
        print(f"│ {inv_text}: {inv_display}".ljust(58) + "│")
        
        print(f"│ 🔄 Turn: {self.turn_count}".ljust(58) + "│")
        
        recent_events = self.quest_log.get_recent_events(2)
        print(f"│ 📝 Quest Log:".ljust(58) + "│")
        for event in recent_events:
            event_short = event[:45] + "..." if len(event) > 45 else event
            print(f"│   • {event_short}".ljust(58) + "│")
        print("└" + "─" * 57 + "┘")
        
    def process_npc_actions(self):
        """Queue processing for NPC actions"""
        if self.npc_action_queue and random.random() < 0.3:  # 30% chance per turn
            action = self.npc_action_queue.popleft()
            print(f"👹 NPC EVENT: {action}")
            self.quest_log.add_event(f"NPC Event: {action}")
            # Re-queue the action for later
            self.npc_action_queue.append(action)
    
    def move_player(self, direction):
        """Player movement function"""
        directions = {
            'north': (-1, 0), 'south': (1, 0),
            'east': (0, 1), 'west': (0, -1),
            'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'w': (0, -1)
        }
        
        if direction not in directions:
            print("❌ Invalid direction! Use north/south/east/west (or n/s/e/w)")
            return False
        
        dx, dy = directions[direction]
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        
        # Check boundaries and walls
        if (new_x < 0 or new_y < 0 or 
            new_x >= len(self.world.game_map) or 
            new_y >= len(self.world.game_map[0]) or
            self.world.game_map[new_x][new_y] == '#'):
            print("🚫 Can't move there - blocked or out of bounds!")
            return False
        
        # Save current position to stack
        self.move_stack.append(self.player_pos[:])
        
        # Move player
        self.player_pos = [new_x, new_y]
        
        # Reveal new area
        PathfindingSystem.reveal_fog_of_war(
            self.world.game_map, new_x, new_y, self.revealed_cells, radius=1
        )
        
        # Handle cell interactions
        cell_content = self.world.game_map[new_x][new_y]
        self.handle_cell_interaction(cell_content, new_x, new_y)
        
        return True
    
    def handle_cell_interaction(self, cell_content, x, y):
        """Function to handle different cell types"""
        if cell_content == 'I':
            print("✨ You found treasure!")
            self.quest_log.add_event(f"Found treasure at ({x}, {y})")
        elif cell_content == 'M':
            print("⚔️  You encountered a monster!")
            self.quest_log.add_event(f"Encountered monster at ({x}, {y})")
            self.handle_combat()
        elif cell_content == 'G':
            print("🎉 VICTORY! You reached the goal!")
            self.quest_log.add_event("Reached the goal - Victory!")
            self.game_over = True
        elif (x, y) in self.world.trap_locations:
            print("🕳️  You triggered a hidden trap!")
            self.quest_log.add_event(f"Triggered trap at ({x}, {y})")
    
    def handle_combat(self):
        """Simple combat system"""
        if random.random() < 0.7:  # 70% chance to defeat monster
            print("🗡️  You defeated the monster!")
            self.quest_log.add_event("Defeated monster in combat")
            # Add reward
            self.world.inventory.append("monster_trophy")
        else:
            print("💀 The monster dealt damage! You retreat.")
            self.quest_log.add_event("Retreated from combat")
    
    def collect_item(self):
        """List operations for inventory management"""
        x, y = self.player_pos
        if self.world.game_map[x][y] == 'I':
            if len(self.world.inventory) >= self.world.max_inventory_size:
                print("🎒 Inventory full! Cannot collect more items.")
                return
            
            # Add item to inventory 
            treasure_value = self.world.treasure_values.get('I', 25)
            item_name = f"treasure_worth_{treasure_value}"
            self.world.inventory.append(item_name)
            
            # Remove from map
            self.world.game_map[x][y] = '.'
            
            print(f"💎 Collected {item_name}!")
            self.quest_log.add_event(f"Collected {item_name}")
        else:
            print("❌ No items here to collect!")
    
    def show_inventory(self):
        """List display and analysis"""
        print(f"\n🎒 INVENTORY ({len(self.world.inventory)}/{self.world.max_inventory_size}):")
        if not self.world.inventory:
            print("   Empty - go find some treasure!")
        else:
            # List traversal and analysis
            for i, item in enumerate(self.world.inventory):
                print(f"   {i+1}. {item}")
            
            # Calculate total value
            total_value = sum(int(item.split('_')[-1]) for item in self.world.inventory 
                            if 'worth' in item)
            print(f"   💰 Total Value: {total_value} gold")
    
    def undo_move(self):
        """Stack operations for undo functionality"""
        if not self.move_stack:
            print("❌ No moves to undo!")
            return
        
        # Pop from stack 
        previous_pos = self.move_stack.pop()
        self.player_pos = previous_pos
        
        print(f"↩️  Undid last move. Back to ({self.player_pos[0]}, {self.player_pos[1]})")
        self.quest_log.add_event("Used undo to return to previous position")
    
    def check_pathfinding(self):
        """Recursive pathfinding demonstration"""
        has_path = PathfindingSystem.has_path_to_goal(
            self.world.game_map, 
            self.player_pos[0], 
            self.player_pos[1]
        )
        
        if has_path:
            print("🛤️  There IS a path to the goal from your current position!")
        else:
            print("🚫 No path to the goal found from current position.")
        
        self.quest_log.add_event("Checked pathfinding to goal")
    
    def show_quest_log(self):
        """Linked List display"""
        print("\n📜 COMPLETE QUEST LOG:")
        events = self.quest_log.get_all_events()
        if not events:
            print("   No events recorded yet.")
        else:
            for event in events:
                print(f"   📋 {event}")
    
    def show_help(self):
        """Help function"""
        print("\n🆘 AVAILABLE COMMANDS:")
        commands = {
            'Movement': ['north/n', 'south/s', 'east/e', 'west/w'],
            'Actions': ['get', 'inventory', 'quests', 'path', 'undo'],
            'System': ['help', 'stats', 'quit']
        }
        
        for category, cmd_list in commands.items():
            print(f"   {category}: {', '.join(cmd_list)}")
    
    def show_statistics(self):
        """Matrix and list analysis"""
        print(f"\n📊 DETAILED STATISTICS:")
        
        # Matrix analysis 
        rows, cols = self.world.get_map_dimensions()
        print(f"   🗺️  Map Size: {rows}x{cols} = {rows * cols} total cells")
        
        element_counts = self.world.count_map_elements()
        print("   🔍 Map Elements:")
        for element, count in element_counts.items():
            print(f"      {element}: {count}")
        
        # List analysis 
        print(f"   🎒 Inventory Usage: {len(self.world.inventory)}/{self.world.max_inventory_size}")
        print(f"   📍 Revealed Cells: {len(self.revealed_cells)}")
        print(f"   🔄 Moves Made: {len(self.move_stack)}")
        print(f"   📝 Quest Events: {self.quest_log.size}")
        
        # Submatrix around player 
        submatrix = self.world.get_submatrix_around_player(self.player_pos)
        print(f"   🎯 3x3 Area around player:")
        for row in submatrix:
            print(f"      {''.join(f'{cell:3}' for cell in row)}")
    
    def game_loop(self):
        """Main game loop with comprehensive command processing"""
        print("\n")
        print("\n" + "─" * 50)
        print("🎮 Welcome to the Dungeon Crawler!")
        print("   Type 'help' for available commands.")
        
        while not self.game_over:
            print("─" * 50)
            self.display_game_state()
            
            # Process NPC actions 
            self.process_npc_actions()
            
            # Get user input
            command = input("\n🎮 Enter command: ").lower().strip()
            
            # Process commands 
            if command in ['north', 'south', 'east', 'west', 'n', 's', 'e', 'w']:
                if self.move_player(command):
                    self.turn_count += 1
            
            elif command == 'get':
                self.collect_item()
            
            elif command in ['inventory', 'inv']:
                self.show_inventory()
            
            elif command in ['quests', 'log']:
                self.show_quest_log()
            
            elif command == 'path':
                self.check_pathfinding()
            
            elif command == 'undo':
                self.undo_move()
            
            elif command == 'help':
                self.show_help()
            
            elif command in ['stats', 'statistics']:
                self.show_statistics()
            
            elif command in ['quit', 'exit']:
                print("👋 Thanks for playing! Goodbye!")
                break
            
            else:
                print("❓ Unknown command. Type 'help' for available commands.")
        
        # Game over summary
        if self.game_over:
            print(f"\n🏆 GAME COMPLETED in {self.turn_count} turns!")
            print("📊 Final Statistics:")
            self.show_statistics()

# Run the game
if __name__ == "__main__":
    game = DungeonCrawler()
    game.game_loop()