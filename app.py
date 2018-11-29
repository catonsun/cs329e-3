from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import codecs


app = Flask(__name__)
usernames = ["mom", "dad"]
passwords = ["asdf", "1234"]
user = False


@app.route("/")
def index():
    choreList = makeChoreList()
    print(choreList)
    if not user:
        return render_template("home.html", chores=choreList)
    else:
        return render_template("home-user.html", chores=choreList)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        verify(username, password)
        return redirect(url_for('index'))
    return render_template("login.html")


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    global user
    user = False
    return redirect(url_for("index"))


def verify(username, password):
    try:
        ind = usernames.index(username)
        if passwords[ind] == password:
            global user
            user = True
            return "user is verified"
    except ValueError:
        return "Username not found"


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join('static', filename))
        print(request.form.get('name'))
        print(request.form["description"])
        chore = request.form.get('name')
        description = request.form["description"]
        save(chore, description, filename, 'DATABASE.csv')
        deletechore(chore)
        return redirect(url_for('index'))
    if not user:
        output = makeChoreList()
        return render_template("upload.html", chore=output)
    else:
        output = makeChoreList()
        return render_template("upload-user.html", chore=output)


def save(chore, description, picture, csvFile):
    row = [str(chore), str(description), str(picture)]
    with open(csvFile, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)
    return row


@app.route("/deletechorelist", methods=['POST', 'GET'])
def deletechorelist():
    if request.method == 'POST':
        chore = request.form["chore"]
        print(chore)

        deletechore(chore)

        return redirect(url_for('index'))
    return render_template("delete_from_chore_checklist.html")


def deletechore(chore):
    holder = []
    with open('CHORES.csv', 'r') as inp:
        for row in csv.reader(inp):
            if not row:
                continue
            else:
                print(row[0])
                if row[0] != chore:
                    holder.append(row)
    with open('CHORES.csv', 'w') as output:
        writer = csv.writer(output)
        for row in holder:
            writer.writerow(row)


@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        chore = request.form["chore"]
        print(chore)
        holder = []
        with open('DATABASE.csv', 'r') as inp:
            for row in csv.reader(inp):
                if not row:
                    continue
                elif row[0] != chore:
                    holder.append(row)
                else:
                    picture = row[2]
                    if os.path.exists("static/" + picture):
                        os.remove("static/" + picture)
                    else:
                        print("The file does not exist")
        with open('DATABASE.csv', 'w') as output:
            writer = csv.writer(output)
            for row in holder:
                writer.writerow(row)

        return redirect(url_for('index'))
    return render_template("delete.html")


@app.route("/checklist", methods=['POST', 'GET'])
def checklist():
    if request.method == 'POST':
        print(request.form["chore"])
        print(request.form["description"])
        chore = request.form["chore"]
        description = request.form["description"]
        row = [str(chore), str(description)]
        with open("CHORES.csv", 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row)
        return redirect(url_for('index'))
    return render_template("checklist.html")


@app.route("/choreview", methods=['POST', 'GET'])
def choreview():
    output = makeList('DATABASE.csv')
    if not user:
        return render_template("choreview.html", chore=output)
    else:
        return render_template("choreview-user.html", chore=output)

# This opens the DATABASE.csv file and records the data
def makeList(csvFile):
    dataList = ""
    # with open('Questions.csv', 'r') as csvfile:
    with codecs.open(csvFile, "r", encoding='utf-8', errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            dataList += str(row) + '`'
    csvfile.close()
    return dataList


def makeChoreList():
    dataList = ""
    with codecs.open("CHORES.csv", "r", encoding='utf-8', errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            dataList += str(row) + '`'
    csvfile.close()
    return dataList


# @app.route("/listOutput", methods=['POST', 'GET'])
# def listOutput():
#     output=makeList()
#     return render_template("listview.html", name = output)

@app.route("/noAccess", methods=['POST', 'GET'])
def noAccess():
    return render_template("noAccess.html")


if __name__ == '__main__':
    app.run()
