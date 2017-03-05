# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A:	From the problem , we understand that naked twins exist within SAME UNIT.
	Also if naked twins are found, then they must be eliminated (without modifying the twins themselves) from the SAME UNIT in which they are found.
	Using the above knowledge learned about the constraint :
	We first find the duplicates and gather the list. Then we iterate through each list, if we find a duplicate member, then we traverse this unit and modify all values where twins can be removed. Two special cases need to be considered where if value is already fixed (i.e. one digit) then it should not be modified. Also twins themselves should not be modified.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A:
	From the problem, we learn that diagonal sudoku is just a specialized form of regular sudoku, where diagonals must be considered as units in solving the problem. This is a property of encoding the board itself, hence we define the diagonal units as a part of total unitlist.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

