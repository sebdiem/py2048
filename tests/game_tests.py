#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Sébastien Diemer <sebastien.diemer@mines-paristech.fr>

from nose.tools import *
from py2048.game import *

def test_make_grid():
    grid = make_grid(('- - - 2\n'
                      '2 - - 4\n'
                      '- 8 - 2\n'
                      '- - 16 16'))
    assert len(grid) == GRID_SIZE**2
    assert is_empty(grid, 0)
    assert is_empty(grid, 1)
    assert is_empty(grid, 2)
    assert grid[3] == 2
    assert grid[4] == 2
    assert is_empty(grid, 5)
    assert is_empty(grid, 6)
    assert grid[7] == 4
    assert is_empty(grid, 8)
    assert grid[9] == 8
    assert is_empty(grid, 10)
    assert grid[11] == 2
    assert is_empty(grid, 12)
    assert is_empty(grid, 13)
    assert grid[14] == 16
    assert grid[15] == 16

def test_add_random():
    grid = make_grid(('- - - 2\n'
                      '2 - - 4\n'
                      '- 8 - 2\n'
                      '- - 16 16'))
    grid_none = [0, 1, 2, 5, 6, 8, 10, 12, 13]
    assert add_random(grid)
    assert grid[3] == 2
    assert grid[4] == 2
    assert grid[7] == 4
    assert grid[9] == 8
    assert grid[11] == 2
    assert grid[14] == 16
    assert grid[15] == 16
    assert len([i for i in grid_none if grid[i] is not None]) == 1

def test_add_random_impossible():
    grid = make_empty_grid()
    for _ in xrange(GRID_FLAT_LEN):
        add_random(grid)
    assert not add_random(grid)

def test_empty_cells():
    grid = make_grid(('- - - 2\n'
                      '2 - - 4\n'
                      '- 8 - 2\n'
                      '- - 16 16'))
    assert get_empty_cells(grid) == [0, 1, 2, 5, 6, 8, 10, 12, 13]

def test_move_left():
    grid = make_grid(('- - - 2\n'
                      '2 - - 4\n'
                      '- 8 - 2\n'
                      '- - 16 16'))
    move(grid, 'left')
    eq_(grid, [2, None, None, None,
               2, 4, None, None,
               8, 2, None, None,
               32, None, None, None])
    grid = make_grid(('2 2 - 2\n'
                      '2 - - 4\n'
                      '- 8 - 2\n'
                      '- - 16 16'))
    move(grid, 'left')
    eq_(grid, [4, 2, None, None,
               2, 4, None, None,
               8, 2, None, None,
               32, None, None, None])

def test_move_right():
    grid = make_grid(('- - - 2\n'
                      '2 - - 4\n'
                      '- 8 - 2\n'
                      '- - 16 16'))
    move(grid, 'right')
    eq_(grid, [None, None, None, 2,
               None, None, 2, 4,
               None, None, 8, 2,
               None, None, None, 32])
    grid = make_grid(('- - - 2\n'
                      '2 2 2 4\n'
                      '- 8 - 2\n'
                      '- - 16 16'))
    move(grid, 'right')
    eq_(grid, [None, None, None, 2,
               None, 2, 4, 4,
               None, None, 8, 2,
               None, None, None, 32])

def test_move_top():
    grid = make_grid(('- - - 2\n'
                      '2 - - 4\n'
                      '- 8 - 2\n'
                      '- - 16 16'))
    move(grid, 'top')
    eq_(grid, [2, 8, 16, 2,
               None, None, None, 4,
               None, None, None, 2,
               None, None, None, 16])
    grid = make_grid(('- - - 2\n'
                      '2 2 2 2\n'
                      '- 8 - 4\n'
                      '- - 16 4'))
    move(grid, 'top')
    eq_(grid, [2, 2, 2, 4,
               None, 8, 16, 8,
               None, None, None, None,
               None, None, None, None])

def test_move_bottom():
    grid = make_grid(('2 4 8 16\n'
                      '2 4 8 16\n'
                      '2 4 8 16\n'
                      '2 4 8 16'))
    move(grid, 'bottom')
    eq_(grid, [None, None, None, None,
               None, None, None, None,
               4, 8, 16, 32,
               4, 8, 16, 32])
    grid = make_grid(('- - - 2\n'
                      '2 2 2 2\n'
                      '- 8 - 4\n'
                      '- - 16 4'))
    move(grid, 'bottom')
    eq_(grid, [None, None, None, None,
               None, None, None, None,
               None, 2, 2, 4,
               2, 8, 16, 8])

def test_a_move():
    grid = make_grid(('2 4 8 16\n'
                      '2 4 8 16\n'
                      '2 4 8 16\n'
                      '2 4 8 16'))
    assert move(grid, 'bottom')
    grid = make_grid(('2 4 8 16\n'
                      '4 2 16 8\n'
                      '2 4 4 16\n'
                      '8 2 8 8'))
    assert not move(grid, 'bottom')
    grid = make_grid(('- - - -\n'
                      '- - - -\n'
                      '- - - -\n'
                      '- - - 8'))
    assert not move(grid, 'right')
    assert not move(grid, 'bottom')

def test_game_finished():
    grid = make_grid(('2 - 8 16\n'
                      '2 4 8 16\n'
                      '2 4 8 16\n'
                      '2 4 8 16'))
    assert not game_finished(grid)
    grid = make_grid(('2 4 8 16\n'
                      '2 4 8 16\n'
                      '2 4 8 16\n'
                      '2 4 8 16'))
    assert not game_finished(grid)
    grid = make_grid(('2 4 8 16\n'
                      '4 2 16 8\n'
                      '2 4 4 16\n'
                      '8 2 8 8'))
    assert not game_finished(grid)
    grid = make_grid(('32 64 16 8\n'
                      '16 2 8 4\n'
                      '4 32 4 2\n'
                      '2 8 8 4'))
    assert not game_finished(grid)
    grid = make_grid(('32 64 16 4\n'
                      '16 2 8 4\n'
                      '4 32 4 2\n'
                      '2 8 2 4'))
    assert not game_finished(grid)
    grid = make_grid(('32 64 16 4\n'
                      '16 2 8 128\n'
                      '4 32 4 512\n'
                      '2 8 2 512'))
    assert not game_finished(grid)
    grid = make_grid(('2 4 8 16\n'
                      '4 2 16 8\n'
                      '2 32 4 16\n'
                      '8 2 128 8'))
    assert game_finished(grid)
    grid = make_grid(('32 64 16 8\n'
                      '16 2 8 4\n'
                      '4 32 4 2\n'
                      '2 4 8 4'))
    assert game_finished(grid)
