from flask import Flask, redirect, render_template
import output_mood_v2 as output_mood
import os

app = Flask(__name__, static_folder='')
@app.route("/")
def hello():
        #path to song
        return render_template('home_page.html')

@app.route("/display") #includes smartplay
def display():
    curr_song = 0 #placeholder
    output_mood.main()
    return render_template("display.html", song = curr_song)# wont be called


#playlist stuff
@app.route("/playlist")
def playlist():
    return render_template("playlist.html")


@app.route("/mood", methods=["GET"])
def mood():
    mood = output_mood.current_mood
    direc = '/home/pi/app/'+ mood + '/'
    lines = os.listdir(direc)
    file = mood + ".html"
    return render_template(file, playlist = lines)

#/endof playlist stuff


@app.route("/add_music")
def add_music():
    return render_template("add_music.html")

@app.route("/settings")
def settings():
    usersettings = 0 #placeholder
    return render_template("settings.html", settings=usersettings)


if __name__ =="__main__":
    flag = False
    if flag:
        output_mood.main()
    app.run(host='172.20.10.3', port=8989, debug=True, threaded=True)
