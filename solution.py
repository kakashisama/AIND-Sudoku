from collections import defaultdict
assignments = []

# Defining naming convention
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    """
    Helper function that creates all possible two digit combinations of provided strings

    Args:
        Two strings

    Returns:
        All possible combinations of two characters each from provided strings
    """
    return [s+t for s in A for t in B]

#Defining units, peers and unitlist
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    #Defining set in which all naked twins will be captured
    naked_twin_set=set()
    # Find all instances of naked twins
    for each_unit in unitlist:
        #Checking for twins in unit
        for each_member in each_unit:
            #Checking member in the unit
            if len(values[each_member]) == 2:
                for compare_with_key in each_unit:
                    if each_member!=compare_with_key and values[each_member]==values[compare_with_key]:
                        # If not self-referencing and
                        naked_twin_set.add(each_member)

    # Eliminate the naked twins as possibilities for their peers
    for each_unit in unitlist:
        for each_member in each_unit:
            if each_member in naked_twin_set:
                for find_duplicate in each_unit:
                    if find_duplicate!=each_member and values[find_duplicate] == values[each_member]:
                        # Confirmed that this member has potential twins and we're currently checking the unit with the duplicate in it
                        for compare_with_key in each_unit:
                            if values[each_member]!=values[compare_with_key]:
                                # Confirming that not dealing with unit or its twin
                                if len(values[compare_with_key])>1:
                                    chars_to_remove=values[each_member]
                                    string_to_remove_from=values[compare_with_key]
                                    for s in chars_to_remove:
                                        string_to_remove_from=string_to_remove_from.replace(s,'')
                                    assign_value(values,compare_with_key,string_to_remove_from)
                                    # Naked twins were eliminated from this peer

    # fail-safe to ensure empty values are not returned
    if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    grid_temp=dict(zip(boxes, grid))
    for key, value in grid_temp.items():
        if value=='.':
            grid_temp[key]='123456789'
    return grid_temp

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Eliminate values which are available as single digits in one of the boxes in each unit.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the single digit box values eliminated from peers.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
           temp_value = values[peer].replace(digit,'')
           assign_value(values,peer,temp_value)

    return values

def only_choice(values):
    """
    Apply value to boxes where only one possible value could be assigned.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with only available value assigned in each unit
    """

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values,dplaces[0],digit)
    return values

def reduce_puzzle(values):
    """
    Reduce possible values for each box by applying all strategies sequentially once.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The values dictionary with only available value assigned in each unit.
        Returns False if solution cannot be improved or if solution cannot be achieved.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Performs depth first search to find the sudoku solution recursively.
    At each decision point, box with lowest possible values is chosen.
    One of the potential values is assigned and tree is branched.


    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The values dictionary with only available value assigned in each unit.
        Returns False if solution cannot be found.
    """

    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid.
        False if no solution exists.
    """

    #First, convert the grid into actionable grid (replace empties with possible values)
    values=grid_values(grid)
    #Second, search for the solution recursively
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # Run the entire solution
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')