#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Sébastien Diemer <sebastien.diemer@mines-paristech.fr>

"""
My implementation of 2048
"""

from random import random, choice

import py2048

GRID_SIZE = 4
GRID_FLAT_LEN = GRID_SIZE**2
EMPTY_CELL = None
TWO_FREQ = 0.8

def is_empty(grid, cell):
    return grid[cell] is None

def make_empty(grid, cell):
    grid[cell] = EMPTY_CELL

def make_empty_grid():
    return [EMPTY_CELL]*(GRID_SIZE**2)

def make_grid(s, empty_cell='-', column_sep=' '):
    grid = s.split('\n')
    if len(grid) == GRID_SIZE:
        grid = [line.split(column_sep) for line in grid]
        to_cell = lambda x: EMPTY_CELL if x == empty_cell else int(x)
        return map(to_cell, [cell for line in grid for cell in line])
    raise ValueError("Grid not well formed")

def make_empty_grid():
    return [None]*(GRID_SIZE**2)

def print_grid(grid):
    print '%s\n' % ('_'*(6*GRID_SIZE-1))
    for line in [grid[i*GRID_SIZE:(i+1)*GRID_SIZE] for i in xrange(GRID_SIZE)]:
        print ' '.join(map(lambda x: "{el:>5}".format(el=(str(x) if x else '-')), line))
    print '_'*(6*GRID_SIZE-1)

def get_empty_cells(grid):
    return [i for i, _ in enumerate(grid) if is_empty(grid, i)]

def add_random(grid):
    """Returns True if there is enough space in the grid to add one number else False."""
    number = 2 if random() < TWO_FREQ else 4
    empty = get_empty_cells(grid)
    if empty:
        grid[choice(get_empty_cells(grid))] = number
        return True
    return False

move_index = {
              'left': lambda i: i-1,
              'right': lambda i: i+1,
              'top': lambda i: i - GRID_SIZE,
              'bottom': lambda i: i + GRID_SIZE,
             }

test_border = {
               'left': lambda i: (i%GRID_SIZE) == 0,
               'right': lambda i: (i%GRID_SIZE) == (GRID_SIZE-1),
               'top': lambda i: 0 <= i < GRID_SIZE,
               'bottom': lambda i: GRID_SIZE**2 > i >= GRID_SIZE**2 - GRID_SIZE,
              }

indices_order = {
                 'left': lambda : range(GRID_FLAT_LEN),
                 'right': lambda : range(GRID_FLAT_LEN)[::-1],
                 'top': lambda : range(GRID_FLAT_LEN),
                 'bottom': lambda : range(GRID_FLAT_LEN)[::-1],
                }

def move(grid, move):
    """Move all the cells of the grid in the left, right, top or bottom direction depending on
    the value of the move parameter.
    Returns True if a move was made else False."""
    joined_cells = [False]*GRID_FLAT_LEN
    a_move = False
    for i in indices_order[move]():
        if not test_border[move](i) and not is_empty(grid, i):
            j, k = move_index[move](i), i
            while is_empty(grid, j) and not test_border[move](j):
                j, k = move_index[move](j), j
            if is_empty(grid, j):
                grid[j] = grid[i]
                make_empty(grid, i)
                a_move = True
            elif grid[j] == grid[i] and not joined_cells[j]:
                grid[j] = grid[i]*2
                make_empty(grid, i)
                joined_cells[j] = True
                a_move = True
            elif j != move_index[move](i):
                grid[k] = grid[i]
                make_empty(grid, i)
                a_move = True
    return a_move

def game_finished(grid):
    """Returns True if the game is finished (no more move possible) else False.
    The game is finished when there is no more empty cell and no two adjacent cell have the same
    value."""
    if len(filter(lambda x: x == EMPTY_CELL, grid)) > 0:
        return False
    for i in xrange(GRID_FLAT_LEN):
        if (i%GRID_SIZE != GRID_SIZE-1) and grid[i] == grid[i+1]:
            return False
        if (i < GRID_FLAT_LEN - GRID_SIZE) and grid[i] == grid[i+GRID_SIZE]:
            return False
    return True

KEYBOARD_MAP = {
                'q': 'left',
                'd': 'right',
                'z': 'top',
                's': 'bottom',
               }

def print_help_message():
    print '### {name} v.{version} by {author} ###'.format(name=py2048.NAME,
                                                            version=py2048.__version__,
                                                            author=py2048.__author__)
    print '    Keyboard commands:'
    print '    {commands}'.format(commands=str(KEYBOARD_MAP))

def print_final_message():
    print '    You lose!'

def play():
    grid = make_empty_grid()
    while add_random(grid):
        print_grid(grid)
        if game_finished(grid):
            print_final_message()
            break
        else:
            m = raw_input('Your move: ')
            try:
                if not move(grid, KEYBOARD_MAP[m]):
                    m = None
                    raise KeyError
            except KeyError:
                while not m in KEYBOARD_MAP.keys():
                    if m is None:
                        message = ('Impossible move.\n'
                                   'The board did not change following your move {move}.\n'
                                   'Please try a new move: ').format(move=m)
                    else:
                        message = ('Bad move: {move}.\n'
                                   'Please choose a move'
                                   'in {moves}: ').format(move=m, moves=str(KEYBOARD_MAP))
                    m = raw_input(message)
                    if m in KEYBOARD_MAP and not move(grid, KEYBOARD_MAP[m]):
                        m = None
