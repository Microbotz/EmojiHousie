# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 00:59:35 2020

@author: sujain
"""
import random
import pickle
import argparse
import sys

from datetime import datetime
random.seed(datetime.now())

def checkTicket(ticketNo):
    if ticketNo < 1 or ticketNo > 200:
        return False
    t = ticketsAll[ticketNo-1]
    
    corner = (t[0][0]-1 in drawns) and (t[0][8]-1 in drawns) and (t[2][0]-1 in drawns) and (t[2][8]-1 in drawns)
    r1 = True
    for v in t[0]:
        if v == 0 or (v-1 in drawns):
            continue
        r1 = False
        
    r2 = True
    for v in t[1]:
        if v == 0 or (v-1 in drawns):
            continue
        r2 = False
    
    r3 = True
    for v in t[2]:
        if v == 0 or (v-1 in drawns):
            continue
        r3 = False
    fh = r1 and r2 and r3
    return [corner,r1,r2,r3,fh]

def drawEmoji(candidates, drawns):
    count = len(drawns)
    if count == len(candidates):
        return
    return candidates[count]

def renderTicket(ticket, ticketNo, drawns, imagePath):
    if ticket == None:
        return ""
    table = "";
    border = 0
    # The emoji images are hosted in a sub-folder
    for row in ticket:
        table += "<tr>";
        for v in row:
            img = "white.gif" if v == 0 else str(v)+".png"
            if str(v) in drawns:
                border = 4
            table += "<td width=50 height=50><img src='{0}/{1}' width=50 height=50 style=\"border:{2}px solid green;\"/></td>".format(imagePath,img,border)
            border=0
        table += "</tr>";

    ftable = "<head> <center><H1><b><i>Ticket Number {0}</b></i></H1></center></head><table cellspacing=0 cellpadding=5 border=2>{1}</table>".format(ticketNo,table)
    return ftable

def renderBoard(boardPath, drawns, data, cur=None, ticketNum=None):
    # Get BoardSize
    size = data["BoardSize"]
    imagePath = data["ImagePath"]
    
    # Get ticket to be checked for highliting in board
    ticket = data["Tickets"][int(ticketNum)-1] if ticketNum else None
    
    tableHtml = drawBoard(size, drawns, imagePath, ticket)
    curHtml = renderCurrent(cur, drawns, imagePath)
    ticketHtml = renderTicket(ticket, ticketNum, drawns, imagePath)
    
    boardName = "Welcome to Emoji Housie"
    rowElement1 = "<td><head><center><H1><b><i>{0}</b></i></H1></center></head>{1}</td>".format(boardName,tableHtml)
    rowElement2 = "<td><table><tr><td>{0}</td></tr><tr><td>{1}</td></tr></table></td>".format(curHtml, ticketHtml)
    board = "<table><tr>{0}{1}</tr></table>".format(rowElement1,rowElement2)
    with open(boardPath,'w') as file:
        file.write(board)


def drawBoard(size,drawns,imagePath,ticket=None):
    table = "";
    # The emoji images are hosted in a sub-folder
    width=size[0]
    height=size[1]
    board=[]
    count = 0
    border=0
    ticketSet = {}
    
    # Find images in ticket
    if ticket:
        for trow in ticket:
            for tval in trow:
                ticketSet[tval]=True
    #Initialize board
    for h in range(height):
        r = []
        for w in range(width):
            if count < len(drawns):
                r.append(drawns[count])
                count += 1
            else:
                r.append(0)
        board.append(r)
    for row in board:
        table += "<tr>";
        border = 0
        for v in row:
            img = "white.gif" if v == 0 else str(v)+".png"
            #Highlight image on board which are present on ticket
            if ticket and v != 0: 
                if str(v) in ticketSet:
                    border = 8
            table += "<td width=70 height=70><img src='{0}/{1}' width=70 height=70 style=\"border:{2}px solid green;\"/></td>".format(imagePath,img,border)
            border = 0
        table += "</tr>";
    return "<table cellspacing=0 cellpadding=10 border=2>{0}</table>".format(table)
        
def renderCurrent(cur, drawns, imagePath):
    if not cur:
        return ""
    num = len(drawns)
    img = str(cur)+".png"
    table = "<tr><td width=400 height=400><img src='{0}/{1}' width=400 height=400/></td></tr>".format(imagePath, img)
    board = "<head> <left><H1><b><i>Turn Number {0}</b></i></H1></left></head><table cellspacing=0 cellpadding=1 border=2>{1}</table>".format(num,table)
    return board


def play(boardPath, candidates, drawns, data):
    cur = drawEmoji(candidates, drawns)
    renderBoard(boardPath, drawns=drawns, data=data, cur=cur)
    return cur

def parseArgs():
    parser = argparse.ArgumentParser()
    # add arguments to the parser
    parser.add_argument('-d', help='DataBase Path. Path of the data baase folder used while generating tickets.')
    parser.add_argument('-b', help='Board Path. This where the game board will be rendered.')
    args = parser.parse_args()
    if args.d == None or args.b == None:
        parser.print_help()
        sys.exit()
    return args

def startGame():
    args = parseArgs()
    dataFile = open(args.d + "data.db",'rb')
    data= pickle.load(dataFile)
    candidates = data["Candidates"]
    random.shuffle(candidates)
    noOfTickets = len(data["Tickets"])
    drawns = []
    renderBoard(boardPath = args.b, drawns=drawns, data=data)
    cur = None
    while True:
        ip = input()
        if ip.lower().strip() == "next" or ip.lower().strip() == "n":
            cur = play(boardPath = args.b, candidates=candidates, drawns=drawns, data=data)
            drawns.append(cur)
        elif ip.lower().strip() == "check" or ip.lower().strip() == "c":
            num = input("Enter Ticket Number:")
            if int(num) < 1 or int(num) > noOfTickets:
                continue
            else:
                renderBoard(boardPath = args.b, drawns=drawns, cur=cur, ticketNum=num, data=data)

if __name__ == "__main__":
    startGame()
    
    
