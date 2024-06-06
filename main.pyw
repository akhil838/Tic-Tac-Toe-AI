from customtkinter import *
import random
import time


top = CTk()
top.title("TicTacToe AI")
top.resizable(False, False)
frame = CTkFrame(top)
frame.pack()
myFont = CTkFont(family='Arial bold', size=40)

global pscore, ascore, banner, player_score, ai_score,tie
pscore, ascore,tie = 0, 0, 0

## SCORE BOARD
banner = CTkLabel(frame, text='', font=('Arial', 20))
banner.grid(row=4, column=2)

player_score = CTkLabel(frame, text=f'You: {pscore}', font=('Arial', 18))
player_score.grid(row=4, column=1)

ai_score = CTkLabel(frame, text=f'AI: {ascore}', font=('Arial', 18))
ai_score.grid(row=4, column=3)

draw = CTkLabel(frame, text=f'Tie: {tie}', font=('Arial', 18))
draw.grid(row=5, column=3)

lable = CTkLabel(frame, text=f'   Made with ❤️\nby akhil838', font=('Arial', 10))
lable.grid(row=5, column=2)


## WIN STATES and STATE SPACE
win = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 4, 8}, {2, 4, 6}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}]
num = [0, 1, 2, 3, 4, 5, 6, 7, 8]


## CHECK WIN CONDITION
def IsWin(p1, p2):
    global pscore, ascore, tie
    for i in range(0, 8):
        if win[i].issubset(p1):
            banner.configure(text='YOU WON')
            pscore += 1
            player_score.configure(text=f'YOU: {pscore}')
            frame.update()
            time.sleep(2)
            main()
        elif win[i].issubset(p2):
            banner.configure(text='YOU LOST')
            ascore += 1
            print(ascore)
            ai_score.configure(text=f'AI: {ascore}')
            top.update()
            time.sleep(2)
            main()
    if t == 0:
        banner.configure(text='TIE')
        tie += 1
        draw.configure(text=f'Tie: {tie}')
        top.update()
        time.sleep(2)
        main()


def Win(p):
    for i in range(0, 8):
        if win[i].issubset(p):
            return True
    else:
        return False


## MIN MAX ALGORITHM
def minmax(board, p1, p2, depth, is_max):
    if Win(p2):
        return float('inf'), depth
    elif Win(p1):
        return float('-inf'), depth
    elif ' ' not in board:
        return 0, depth

    if is_max:
        bestscore = 1000
        bestdepth = 9
        move = -1
        for i in range(len(board)):
            if board[i] == ' ':
                board[i] = 'O'
                p2.add(i)
                score, dep = minmax(board, p1, p2, depth + 1, False)
                p2.remove(i)
                board[i] = ' '
                if score >= bestscore and dep < bestdepth:
                    bestscore = score
                    bestdepth = dep
                    move = i
        #print('MAX', bestscore, 'depth:', depth, dep, 'move:', move)
        return bestscore, dep
    else:
        bestscore = 1000
        bestdepth = 9
        move = -1
        for i in range(len(board)):
            if board[i] == ' ':
                board[i] = 'X'
                p1.add(i)
                score, dep = minmax(board, p1, p2, depth + 1, True)
                p1.remove(i)
                board[i] = ' '
                if score <= bestscore and dep < bestdepth:
                    bestscore = score
                    bestdepth = dep
                    move = i
        #print('MIN', bestscore, 'depth:', depth, dep, 'move:', move)
        #print('MIN',bestscore,'depth',depth,dep)
        return bestscore, dep

## INITIALISATION FIRST MOVE
def bestmove(arr, p1, p2):
    bestscore = 0
    move = -1
    bestdepth = 9
    bestmove2 =-1
    for i in range(len(arr)):
        if arr[i] == ' ':
            arr[i] = 'O'
            p2.add(i)
            score, dep = minmax(arr, p1, p2, 0, True)
            #print('in bestmove', score, p2, i)
            arr[i] = ' '
            p2.remove(i)
            #print(score,dep)
            if score >= bestscore and dep < bestdepth:
                bestscore = score
                bestdepth = dep
                move = i
                #print('bestscore', bestscore, 'move', move, 'depth', dep)
    #print('final bestscore', bestscore, 'move', move, 'depth:', dep)
    #print()
    for i in range(len(arr)):
        if arr[i] == ' ':
            p1.add(i)
            if Win(p1):
                bestmove2 = i
            p1.remove(i)
    if bestscore == 1000:
        a = [x for x in range(len(arr)) if arr[x] == ' ']
        #print('list of available moves', a)
        move = random.choice(a)
        #print(move)
    return move if bestmove2 == -1 else bestmove2

## MARK PLAYER MOVES
def label(arr, num):
    global t, player1, player2
    if t % 2 != 0:
        arr[num] = 'X'
        player1.add(num)
        #b[num].configure(fg_color='#8897BD')
        #b[num].configure(fg_color='')
        b[num].configure(text=arr[num])
        b[num].configure(state=DISABLED)
        t = t - 1
        if t <= 5:
            IsWin(player1, player2)
    if t % 2 == 0:
        move = bestmove(arr, player1, player2)
        arr[move] = 'O'
        player2.add(move)
        # b[num].configure(fg_color='#8897BD')
        # b[num].configure(fg_color='')
        b[move].configure(text=arr[move])
        b[move].configure(state=DISABLED)
        t = t - 1
        if t <= 5:
            IsWin(player1, player2)

## GUI
def game():
    b[0] = CTkButton(frame, width=120, height=120, text=arr[0], fg_color='black', font=myFont,
                     command=lambda: label(arr, 0), state=NORMAL)
    b[1] = CTkButton(frame, width=120, height=120, text=arr[1], fg_color='black', font=myFont,
                     command=lambda: label(arr, 1), state=NORMAL)
    b[2] = CTkButton(frame, width=120, height=120, text=arr[2], fg_color='black', font=myFont,
                     command=lambda: label(arr, 2), state=NORMAL)
    b[3] = CTkButton(frame, width=120, height=120, text=arr[3], fg_color='black', font=myFont,
                     command=lambda: label(arr, 3), state=NORMAL)
    b[4] = CTkButton(frame, width=120, height=120, text=arr[4], fg_color='black', font=myFont,
                     command=lambda: label(arr, 4), state=NORMAL)
    b[5] = CTkButton(frame, width=120, height=120, text=arr[5], fg_color='black', font=myFont,
                     command=lambda: label(arr, 5), state=NORMAL)
    b[6] = CTkButton(frame, width=120, height=120, text=arr[6], fg_color='black', font=myFont,
                     command=lambda: label(arr, 6), state=NORMAL)
    b[7] = CTkButton(frame, width=120, height=120, text=arr[7], fg_color='black', font=myFont,
                     command=lambda: label(arr, 7), state=NORMAL)
    b[8] = CTkButton(frame, width=120, height=120, text=arr[8], fg_color='black', font=myFont,
                     command=lambda: label(arr, 8), state=NORMAL)

    b[0].grid(row=1, column=1)
    b[1].grid(row=1, column=2)
    b[2].grid(row=1, column=3)
    b[3].grid(row=2, column=1)
    b[4].grid(row=2, column=2)
    b[5].grid(row=2, column=3)
    b[6].grid(row=3, column=1)
    b[7].grid(row=3, column=2)
    b[8].grid(row=3, column=3)



def main():
    global arr, b, banner, player_score, ai_score, player1, player2, t
    arr = [" "] * 9
    b = [' '] * 9
    player1 = set()
    player2 = set()
    t = 8

    game()
    frame.update()
    time.sleep(1)

    banner.configure(text="")
    move = random.choice(range(9))
    arr[move] = 'O'
    player2.add(move)
    # b[num].configure(fg_color='#8897BD')
    # b[num].configure(fg_color='')
    b[move].configure(text=arr[move])
    b[move].configure(state=DISABLED)
    t = t - 1
    if t <= 5:
        IsWin(player1, player2)

main()

top.mainloop()
