from electricDie import get_random_num
from sense_hat import SenseHat
import time
import random
import threading
import os
import csv
from os.path import expanduser
from csv import writer
from csv import reader
from datetime import datetime


sense = SenseHat()

def gameInit():
    """
    Game innitialization and main game program with create csv function called after the game ends
    """
    sense.show_message("Dice game, shake to roll, 30 points to win! LeftStick: Player 1, RightStick: Player 2")
    P1_score = 0
    P2_score = 0
    P1 = "green"
    P2 = "red"
    status = P1
    winner = ""
    winning_time = ""
    winner_score = 0

    #Game starts
    while True:
        # Sensehat joystick left direction for Player 1's turn
        for x in sense.stick.get_events(): 
            if x.direction == "left":
                sense.clear()
                status = P1
                P1_score = P1_score + get_random_num(status)
                print("Player1 score: " + str(P1_score)) 
                break
        if P1_score >= 30 :
            print("player1 wins")
            sense.show_message("Player1 Wins!")
            winner = "Player1"
            winner_score = P1_score
            winning_time = datetime.now()
            winning_time = winning_time.strftime("%c")
            sense.clear()
            break
        # Sensehat joystick right direction for Player 2's turn
        for x in sense.stick.get_events():
            if x.direction == "right":
                sense.clear()
                status = P2
                P2_score = P2_score + get_random_num(status)
                print("Player2 score: " + str(P2_score)) 
                break
        if P2_score >= 30 :
            sense.show_message("Player2 Wins!")
            print("player2 wins")
            winner = "Player2"
            winner_score = P2_score
            winning_time = datetime.now()
            winning_time = winning_time.strftime("%c")
            sense.clear()
            break
    #Game ends, create winner result CSV
    create_CSV(winner, winner_score, winning_time)


def create_CSV(winner, score, time):
    """
    Create CSV function with winner results(props)
    """
    score = str(score)
    time = str(time)
    row = [[time, winner, score]]
    
    with open("winner.csv", "a", newline='') as csv_file: 
        csv_writer = csv.writer(csv_file)
        # csv_writer.writerow(["Date","Player", "Score"])
        csv_writer.writerows(row)
        print("writing")   

#Start main program
while True:
    gameInit()
    break
