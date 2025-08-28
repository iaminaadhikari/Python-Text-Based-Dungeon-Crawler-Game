# Dungeon Crawler - DSA Learning Project

A text-based adventure game demonstrating Data Structures and Algorithms concepts from a 5-week curriculum.

## Game Overview

Navigate a dungeon, collect treasures, battle monsters, and reach the goal while the game demonstrates practical DSA implementations.

## DSA Concepts Implemented

**Week 1 - Lists & Matrices**: 2D game map, 1D inventory system
**Week 2 - Recursion**: Pathfinding algorithm, fog of war exploration  
**Week 3 - Functions & Loops**: Main game loop, command processing
**Week 4 - Linked Lists**: Quest log system with event tracking
**Week 5 - Stacks & Queues**: Undo moves (stack), NPC actions (queue)

## Installation

```bash
git clone https://github.com/yourusername/dungeon-crawler-dsa.git
cd dungeon-crawler-dsa
python dungeon_crawler.py
```

## Controls

- `north/south/east/west` - Move around
- `get` - Collect items
- `inventory` - View items  
- `quests` - View quest log
- `path` - Check if goal is reachable
- `undo` - Undo last move
- `help` - Show all commands

## Features

- 6x6 grid-based dungeon exploration
- Inventory management with capacity limits
- Combat system with random outcomes
- Recursive pathfinding to goal
- Stack-based undo functionality
- Queue-based NPC event system
- Comprehensive game statistics

## Technical Details

- Pure Python implementation (no external dependencies)
- Custom linked list for quest tracking
- Recursive algorithms for map exploration
- Proper stack/queue data structure usage
- Matrix operations for game world

## Educational Value

This project demonstrates practical applications of fundamental computer science concepts through engaging gameplay mechanics, making abstract DSA concepts tangible and memorable.

## License

MIT License - feel free to fork and extend for educational purposes.
