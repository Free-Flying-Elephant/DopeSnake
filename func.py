

import numpy as np
import os, sys


def temp_path():
    try:
        abspath = sys._MEIPASS
    except:
        abspath = os.getcwd()
    return abspath


def find_food(yum_pos, head_pos, head_dir, tail_pos) -> str:
    turn = None
    yum_dist = np.zeros(len(yum_pos))
    for i, yum in enumerate(yum_pos):
        yum_dist[i] = (abs(yum[0] - head_pos[0]) + abs(yum[1] - head_pos[1]))
    try: i = np.where(yum_dist == np.nanmin(yum_dist))[0][0]
    except ValueError: return None
    corr_x = 0
    if yum_pos[i][0] - head_pos[0] > 0: corr_x = 1 # go right
    elif yum_pos[i][0] - head_pos[0] < 0: corr_x = -1 # go left
    corr_y = 0
    if yum_pos[i][1] - head_pos[1] > 0: corr_y = 1 # go down
    elif yum_pos[i][1] - head_pos[1] < 0: corr_y = -1 # go up
    if head_dir == "up" or head_dir == "down":
        if corr_y == 1 and head_dir == "down": pass # do nothing
        elif corr_y == -1 and head_dir == "up": pass # do nothing
        elif corr_y == 0:
            if corr_x == 1:
                turn = "right"
            else:
                turn = "left"
        else:
            # go right or left
            if corr_x == 1:
                turn = "right"
            else:
                turn = "left"
    else: # head_dir right or left
        if corr_x == 1 and head_dir == "right": pass # do nothing
        elif corr_x == -1 and head_dir == "left": pass # do nothing
        elif corr_x == 0:
            if corr_y == 1:
                turn = "down"
            else:
                turn = "up"
        else:
            # go right or left
            if corr_y == 1:
                turn = "down"
            else:
                turn = "up"
    return turn


def find_potential_collisions(head_pos, head_dir, tail_pos, snake_speed) -> list:
    col_coord = []
    for i in range(3): # x
        for j in range(3): # y
            coord = head_pos[0] + (i - 1) * abs(snake_speed), head_pos[1] + (j - 1) * abs(snake_speed) # ambient coords
            for tail in tail_pos[2:]:
                if tail == coord:
                    col_coord.append((i-1, j-1))
    return col_coord


def turn_2_avoid_tail(head_pos, decision, tail_pos) -> str:
    diff = []
    if "left" in decision:
        for tail in tail_pos[1:]:
            if tail[1] == head_pos[1]:
                diff.append(head_pos[0] - tail[0])
        if len(diff) == 0: diff.append(0)
        try:
            idx = diff.index(min([abs(x) for x in diff]))
            idx = 1 # go right
            turn = "right"
        except ValueError:
            idx = diff.index(-min([abs(x) for x in diff]))
            idx = -1 # go left
            turn = "left"
    else:
        for tail in tail_pos[1:]:
            if tail[0] == head_pos[0]:
                diff.append(head_pos[1] - tail[1])
        if len(diff) == 0: diff.append(0)
        try:
            idx = diff.index(min([abs(x) for x in diff]))
            idx = 1 # go down
            turn = "down"
        except ValueError:
            idx = diff.index(-min([abs(x) for x in diff]))
            idx = -1 # go up
            turn = "up"
    return turn


def snake_ai(yum_pos, head_pos, head_dir, tail_pos, turn_hist, snake_speed):
    turn = find_food(yum_pos, head_pos, head_dir, tail_pos)
    # print(f"dir: {head_dir}; turn: {turn}")
    col_coord = find_potential_collisions(head_pos, head_dir, tail_pos, snake_speed)
    signal = []
    sgn_crd = []
    if len(col_coord) == 5 or 1:
        for i in range(2):
            tmp_coord = [x[i] for x in col_coord]
            for j in range(3):
                if tmp_coord.count(j-1) == 3:
                # if tmp_coord.count(j-1) >= 2:
                    signal.append(j-1)
                    sgn_crd.append(i)
        if len(signal) == 0:
            for i in range(2):
                tmp_coord = [x[i] for x in col_coord]
                for j in range(3):
                    if tmp_coord.count(j-1) == 2:
                    # if tmp_coord.count(j-1) >= 2:
                        signal.append(j-1)
                        sgn_crd.append(i)
            # if len(signal) > 0: time.sleep(2)
        if len(signal) == 0:
            trig = 0
            if len(col_coord) > 0:
                for memb in col_coord:
                    for r in range(2):
                        if memb[r] == 0:
                            trig = 1
                if trig == 1:
                    if head_dir == "up" or head_dir == "down":
                        turn = turn_2_avoid_tail(head_pos, ["left", "right"], tail_pos)
                    else:
                        turn = turn_2_avoid_tail(head_pos, ["up", "down"], tail_pos)
        elif len(signal) == 1:
            if sgn_crd[0] == 1:
                if signal[0] == 1 and ((head_dir == "down" and turn == None) or (turn == "down")):
                    if head_dir != "down": turn = head_dir
                    # elif randint(0, 1) == 0: turn = "right"
                    # else: turn = "left"
                    else: turn = turn_2_avoid_tail(head_pos, ["left", "right"], tail_pos)
                elif signal[0] == -1 and ((head_dir == "up" and turn == None) or (turn == "up")):
                    if head_dir != "up": turn = head_dir
                    # elif randint(0, 1) == 0: turn = "right"
                    # else: turn = "left"
                    else: turn = turn_2_avoid_tail(head_pos, ["left", "right"], tail_pos)
                else: turn = turn_2_avoid_tail(head_pos, ["up", "down"], tail_pos)
            else:
                if signal[0] == 1 and ((head_dir == "right" and turn == None) or (turn == "right")):
                    if head_dir != "right": turn = head_dir
                    # elif randint(0, 1) == 0: turn = "down"
                    # else: turn = "up"
                    else: turn = turn_2_avoid_tail(head_pos, ["up", "down"], tail_pos)
                elif signal[0] == -1 and ((head_dir == "left" and turn == None) or (turn == "left")):
                    if head_dir != "left": turn = head_dir
                    # elif randint(0, 1) == 0: turn = "down"
                    # else: turn = "up"
                    else: turn = turn_2_avoid_tail(head_pos, ["up", "down"], tail_pos)
                else: turn = turn_2_avoid_tail(head_pos, ["left", "right"], tail_pos)
        elif signal[0] == 1 and signal[1] == 1:
            if head_dir == "right" or (turn == "right" and head_dir != "down"): turn = "up"
            elif head_dir == "down" or (turn == "down" and head_dir != "right"): turn = "left"
        elif signal[0] == -1 and signal[1] == 1:
            if head_dir == "left" or (turn == "left" and head_dir != "down"): turn = "up"
            elif head_dir == "down" or (turn == "down" and head_dir != "left"): turn = "right"
        elif signal[0] == -1 and signal[1] == -1:
            if head_dir == "left" or (turn == "left" and head_dir != "up"): turn = "down"
            elif head_dir == "up" or (turn == "up" and head_dir != "left"): turn = "right"
        elif signal[0] == 1 and signal[1] == -1:
            if head_dir == "right" or (turn == "right" and head_dir != "up"): turn = "down"
            elif head_dir == "up" or (turn == "up" and head_dir != "right"): turn = "left"
    # print(f"new turn: {turn}")
    return turn



