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
    if not user:
        return render_template("home.html")
    else:
        return render_template("home-user.html")


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
    return render_template("home.html")


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
        print(request.form["chore"])
        print(request.form["description"])
        chore = request.form["chore"]
        description = request.form["description"]
        save(chore, description, filename)
        return redirect(url_for('index'))
    return render_template("upload.html")


def save(chore, description, picture):
    row = [str(chore), str(description), str(picture)]
    with open('DATABASE.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)
    return


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
    choreList = []
    if request.method == 'POST':
        checkChore = request.form["Chore"]
        choreList.append(checkChore)
    return render_template("checklist.html")


@app.route("/choreview", methods=['POST', 'GET'])
def choreview():
    output = makeList()
    return render_template("choreview.html", chore=output)


# This opens the DATABASE.csv file and records the data
def makeList():
    dataList = ""
    # with open('Questions.csv', 'r') as csvfile:
    with codecs.open('DATABASE.csv', "r", encoding='utf-8', errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            dataList += str(row) + '`'
    csvfile.close()
    return dataList


# @app.route("/listOutput", methods=['POST', 'GET'])
# def listOutput():
#     output=makeList()
#     return render_template("listview.html", name = output)


if __name__ == '__main__':
    app.run()
