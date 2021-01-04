#!/usr/bin/env python
import csv

csvfile =  open('rolls_results.csv', 'w')
filewriter = csv.writer(csvfile)
filewriter.writerow(['dice', 'tile_choices', 'double_tiles', 'empty_pit'])

dice = []
tile_choices = []
double_tiles = False
empty_pit = False
cherry_cnt = 0
orange_cnt = 0
bell_cnt = 0
money_cnt = 0

for white_die1 in range(1,7):
    for white_die2 in range(1,7):
        white_dice = [white_die1, white_die2]
        for yellow_die1 in range(1,7):
            for yellow_die2 in range(1,7):
                yellow_dice = [yellow_die1, yellow_die2]

                dice = []
                tile_choices = []
                double_tiles = False
                empty_pit = False
                cherry_cnt = 0
                orange_cnt = 0
                bell_cnt = 0
                money_cnt = 0
                for die in white_dice:
                    if die == 1 or die == 4:
                        dice.append("O")
                        orange_cnt += 1
                    elif die == 2 or die == 5:
                        dice.append("B")
                        bell_cnt += 1
                    elif die == 3:
                        dice.append("C")
                        cherry_cnt += 1
                    elif die == 6:
                        dice.append("M")
                        money_cnt += 1
                for die in yellow_dice:
                    if die == 1 or die == 3 or die == 5:
                        dice.append("C")
                        cherry_cnt += 1
                    elif die == 2:
                        dice.append("O")
                        orange_cnt += 1
                    elif die == 4:
                        dice.append("B")
                        bell_cnt += 1
                    elif die == 6:
                        dice.append("M")
                        money_cnt += 1
                if cherry_cnt == 4 or orange_cnt == 4 or bell_cnt == 4 or money_cnt == 4:
                    double_tiles = True
                    empty_pit = True
                    tile_choices = ["C", "O", "B", "M"]
                elif cherry_cnt == 3:
                    empty_pit = True
                    tile_choices = ["C"]
                elif orange_cnt == 3:
                    empty_pit = True
                    tile_choices = ["O"]
                elif bell_cnt == 3:
                    empty_pit = True
                    tile_choices = ["B"]
                elif money_cnt == 3:
                    empty_pit = True
                    tile_choices = ["M"]
                elif cherry_cnt == 2:
                    tile_choices.append("C")
                    if orange_cnt == 2:
                        tile_choices.append("O")
                    elif bell_cnt == 2:
                        tile_choices.append("B")
                    elif money_cnt == 2:
                        tile_choices.append("M")
                elif orange_cnt == 2:
                    tile_choices.append("O")
                    if bell_cnt == 2:
                        tile_choices.append("B")
                    elif money_cnt == 2:
                        tile_choices.append("M")
                elif bell_cnt == 2:
                    tile_choices.append("B")
                    if money_cnt == 2:
                        tile_choices.append("M")
                elif money_cnt == 2:
                    tile_choices = ["M"]
                elif cherry_cnt == 1 and orange_cnt == 1 and bell_cnt == 1 and money_cnt == 1:
                    tile_choices = ["C", "O", "B", "M"]
                filewriter.writerow([dice, tile_choices, double_tiles, empty_pit])

csvfile.close()


