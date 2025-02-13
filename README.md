# routefinders
Comparison and visualization of the route finding algorithms Dijkstra, A* and Jump Point Search¹.

¹Harabor, D., & Grastien, A. (2011). Online Graph Pruning for Pathfinding On Grid Maps. Proceedings of the AAAI Conference on Artificial Intelligence, 25(1), 1114-1119. https://doi.org/10.1609/aaai.v25i1.7994

## starting
1. Install dependencies with
```
poetry install
```

2. Run program with
```
poetry run python src/index.py
```

## usage
Follow the instructions of the text based ui.

```
Select how you want to run your search algorithms:
1 draw custom map
2 load saved map
3 run algorithm comparison
q quit
```

Selecting "1" allows you to draw your own map. 

Selecting "2" allows you to load an existing map. After opening the map you can make modifications to it. 

You can run the algorithims and see a visualization of their function on the map. Press "d" for Dijkstra, "a" for A* and "j" for Jump Point Search. You can run the algorithms multiple times without closing the map. Quit the map by closing the map window. After quitting you are asked if you want to save the map.

Selecting "3" runs an algorithm comparison on a random Moving AI benchmark map and prints out statistics but no visualization.

Selecting "q" quits the program.