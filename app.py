from flask import Flask
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

### HOME ###

@app.route("/getusername/<userID>")
def getusername(userID):
    with open("./files/users.txt", 'r') as f:
        return f.readlines()[int(userID)-1].split('-')[0]

### CROSSWORD ###

@app.route("/checkalreadydone/<userID>")
def checkalreadydone(userID):
    with open("./files/leaderboard.txt", 'r') as f:
        lines = f.readlines()
    for line in lines:
        l = line.split('-')
        if userID == l[0]:
            return l[1].strip()
    return "false"

@app.route("/checkgrid/<grid>")
def checkgrid(grid):
    with open("./files/clues.txt", 'r') as f:
        if f.readlines()[10].strip() == grid:
            return "correct"
        return ""

@app.route("/getclue/<index>")
def getclue(index):
    i = int(index)
    with open("./files/clues.txt", 'r') as f:
        return f.readlines()[i].strip()

### LEADERBOARD ###

@app.route("/getleaderboard")
def getleaderboard():
    with open("./files/leaderboard.txt", 'r') as f:
        lines = f.readlines()
    with open("./files/users.txt", 'r') as g:
        users = g.readlines()

    leaderboard = []
    i = 0
    while i < 9 and i < len(lines):
        line = lines[i].strip()
        data = line.split('-')
        leaderboard.append({"username":users[int(data[0])-1].split('-')[0],"time":data[1]})
        i = i+1
    return leaderboard
    
@app.route("/updateleaderboard/<data>")
def updateleaderboard(data):
    time = int(data.split('-')[1])
    with open("./files/leaderboard.txt", 'r') as f:
        lines = f.readlines()

    putIn = False
    i = 0
    for line in lines:
        if not putIn:
            lineTime = int(line.strip().split("-")[1])
            if time < lineTime:
                lines.insert(i, data + '\n')
                putIn = True
        i += 1

    if not putIn:
        lines.append(data +'\n')

    with open('./files/leaderboard.txt', 'w') as f:
        f.writelines(lines)

    return "done"



### LOGIN ###

@app.route("/checkuser/<userData>")
def checkuser(userData):
    with open("./files/users.txt", 'r') as f:
        i = 1
        for line in f:
            data = line.strip()
            if userData == data:
                return str(i)
            i+=1

    return "invalid"

@app.route("/checknewuser/<userData>")
def checknewuser(userData):
    username = userData.split('-')[0]
    with open("./files/users.txt", 'r') as f:
        i = 1
        valid = True
        for line in f:
            name = line.split('-')[0]
            print(name,username)
            if username == name:
                valid = False  
            i += 1
        if not valid:
            return "invalid"
    
    with open("./files/users.txt", 'a') as f:
        f.write(userData + "\n")
    return str(i)



import os
# ... your routes and setup ...
app = Flask(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
