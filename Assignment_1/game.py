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

# P1_score = 0
# P2_score = 0
# P1 = "green"
# P2 = "red"
sense = SenseHat()

def gameInit():
    # sense.show_message("Dice game, shake to roll, 30 points to win!")
    P1_score = 0
    P2_score = 0
    P1 = "green"
    P2 = "red"
    status = P1
    winner = ""
    winning_time = ""
    winner_score = 0


    while True:
        # get_random_num(status)

        for x in sense.stick.get_events():
            if x.direction == "left":
                status = P1
                P1_score = P1_score + get_random_num(status)
                print("Player1 score: " + str(P1_score)) 
                
                # sense.clear()
                break
        if P1_score >= 10 :
            print("GGWP, player1 wins")
            winner = "Player1"
            winner_score = P1_score
            winning_time = datetime.now()
            winning_time = winning_time.strftime("%c")
            sense.clear()
            break

        for x in sense.stick.get_events():
            if x.direction == "right":
                status = P2
                P2_score = P2_score + get_random_num(status)
                print("Player2 score: " + str(P2_score)) 
                
                # sense.clear()
                break
        if P2_score >= 30 :
            print("GGWP, player2 wins")
            winner = "Player2"
            winner_score = P2_score
            winning_time = datetime.now()
            winning_time = winning_time.strftime("%c")
            sense.clear()
            break
    create_CSV(winner, winner_score, winning_time)


def create_CSV(winner, score, time):
    score = str(score)
    time = str(time)
    row = [[time, winner, score]]
    
    
    with open("winner.csv", "w", newline='') as csv_file: 
        csv_writer = csv.writer(csv_file)
        
        # csv_writer.writerow(["Date","Winner","Score"])
        csv_writer.writerows(row)
        print("writing")   

        # for x in report:
        #     print(report[0])
        # for x in report:
        #     csv_writer.writerow(report["time"])
        # csv_writer.writerow([report_time[0] for i in report_time]) # write headers
        
        # csv_writer.writerows(report_time)
        
       
        # csv_writer.writerows(report_time)
            




        #start button
        
        # P1_score = P1_score + get_random_num(status)
        # print("Player1 score: " + str(P1_score))
        # status = P2
        # if P1_score >= 30 :
        #     print("GGWP, player1 wins")
        #     break

        # #start button
        # P2_score = P2_score + get_random_num(status)
        # print("Player2 score: " + str(P2_score))
        # status = P1

        # if P2_score >= 30:
        #     print("GGWP, Player2 wins")
        #     break

        
        


while True:
    gameInit()
    break
