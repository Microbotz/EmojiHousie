# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import random
import imgkit
import pickle
import argparse
import os
import sys
from datetime import datetime
random.seed(datetime.now())

def createTicket(candidates,size=[3,9], corners=False):
    numCount = 15
    random.shuffle(candidates)
    selected = candidates[:numCount]
    ticket = []
    count = 0
    for i in range(size[0]):
        if (i == 0 or i == 2) and corners:
            rowRange = [i+1 for i in range(size[1] - 2)]
            random.shuffle(rowRange)
            rowSelected = rowRange[:3]
            r = [0]*size[1]
            r[0] = selected[count]
            count+= 1
            for j in rowSelected:
                r[j] = selected[count]
                count += 1
            r[-1]=selected[count]
            count+=1
            ticket.append(r)
        else:
            rowRange = [i for i in range(size[1])]
            random.shuffle(rowRange)
            rowSelected = rowRange[:5]
            r = [0]*size[1]
            for j in rowSelected:
                r[j] = selected[count]
                count += 1
            ticket.append(r)
    return ticket

def isGoodTicket(ticket):
    for r in ticket:
        val1 = r[0]
        val2 = r[1]
        val3 = r[2]
        if val1==val2 and val2==val3:
            return False
        for v in range(len(r)-3):
            val1=val2
            val2=val3
            val3=r[3+v]
            if val1==val2 and val2==val3:
                return False
    return True

def createGoodTicket(candidates, corner):
    t = createTicket(candidates, corners=corner)
    while not isGoodTicket(t):
        t = createTicket(candidates, corners=corner) 
    return t

def getCandidates(path):
    cand=[]
    fileName = os.listdir(path)
    for fileN in fileName:
        if fileN=="white.gif":
            continue
        cand.append(fileN.split('.')[0])
    return cand

def renderTicket(t, number, imagePath):
    table = "";
    # The emoji images are hosted in a sub-folder
    for row in t:
        table += "<tr>";
        for v in row:
            img = "white.gif" if v == 0 else str(v)+".png"
            table += "<td width=160 height=160><img src='{0}/{1}' width=160 height=160/></td>".format(imagePath, img)
        table += "</tr>";

    ftable = "<head> <center><H1><b><i>Ticket Number {0}</b></i></H1></center></head><table cellspacing=0 cellpadding=10 border=2>{1}</table>".format(number,table)
    return ftable

def GenerateTickets(num, imagePath, ticketPath, dbPath, corner, conf):
    if not os.path.exists(imagePath):
        print("Image Folder Dont exists : {0}".format(imagePath))
    if not os.path.exists(ticketPath):
        os.makedirs(ticketPath)
    if not os.path.exists(dbPath):
        os.makedirs(dbPath)
    cand = getCandidates(imagePath)
    ticketMap = {}
    for i in range(num):
        t = createGoodTicket(cand, corner)
        ticketMap[i] = t
        renderedTicket = renderTicket(t, i+1, imagePath)
        imgkit.from_string(renderedTicket,"{0}/{1}.png".format(ticketPath,str(i+1)), config=conf)
    dataBase = {}
    dataBase["ImagePath"] = imagePath
    dataBase["Tickets"] = ticketMap
    dataBase["Candidates"] = cand
    dataBase["BoardSize"] = [10, len(cand)//10 if len(cand)%10 == 0 else (len(cand)//10)+1 ]
    
    with open("{0}/data.db".format(dbPath),'wb') as file:
        pickle.dump(dataBase, file)

def parseArgs():
    parser = argparse.ArgumentParser()
    # add arguments to the parser
    parser.add_argument("-n", help="Number to Tickets. Default : 100", default=100, type=int)
    parser.add_argument("-i", help="Image Folder Path. This is where all the images used for housie ticker is stored. Could be any number.")
    parser.add_argument('-d', help='Output DataBase Path. This is where all the information about generated tickets will be stored and will be used by GameBoardSimulator.')
    parser.add_argument('-o', help="Output Ticket folder where all the generated tickets will be stored." )
    parser.add_argument('-w', help='wkhtmlToImage Path. This is used for rendering Tickets')
    parser.add_argument('-c', help='Fix Corners in Ticket. If set to True, all the tickets will have images on corner. Default : False', default=False, type=bool)
    args = parser.parse_args()
    if args.i == None or args.o == None or args.d == None or args.w == None:
        parser.print_help()
        sys.exit()
    return args

def start():
    args = parseArgs()
    conf = imgkit.config(wkhtmltoimage=args.w if args.w !=None else "")
    GenerateTickets(args.n, args.i, args.o, args.d, args.c, conf)

if __name__ == "__main__":
    start()
    