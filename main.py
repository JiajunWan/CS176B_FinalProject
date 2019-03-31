import os, urllib, wget, subprocess, time, pydrive, glob
from flask import Flask, render_template, url_for, flash, redirect
from forms import InformationForm
from auth import AuthForm
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdf'
uploaded = []
gauth = GoogleAuth()
url = gauth.GetAuthUrl()
auth_url = url.replace("http%3A%2F%2Flocalhost%3A8080%2F", "http://localhost:8080/")
split_index = auth_url.find("localhost")+2

# rm -rf ~/./.local/share/Trash/files/*

# du -a | sort -n -r | head -n 5

# http://releases.ubuntu.com/18.04/ubuntu-18.04.2-desktop-amd64.iso.torrent
# http://releases.ubuntu.com/18.04/ubuntu-18.04.2-desktop-amd64.iso.torrent?_ga=2.66795821.2059850810.1551004639-1774269339.1551004639
# https://scontent-sjc3-1.cdninstagram.com/vp/4d000808a3b8d90515e039396ded719b/5D21D574/t51.2885-15/e35/35576110_416537562161449_2422131224437850112_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com
# https://scontent-sjc3-1.cdninstagram.com/vp/e771e02ae0170458aecab9df3a0cd70f/5D20FC82/t51.2885-15/e35/37033573_429721974178062_4679925287754924032_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = AuthForm()
    if form.validate_on_submit():
        error = 0
        try:
            gauth.Auth(form.authcode.data)
        except pydrive.auth.AuthenticationError as e:
            error = 1
            flash('Authentication failed. Please check AuthCode!', 'danger')
        if error is not 1:
            flash('Successful login to Google Drive!', 'success')
            flash('Now you can start download!', 'success')
            return redirect(url_for('home'))
    return render_template('login.html', title='AuthCode', form=form, post1=auth_url[:split_index], post2=auth_url[split_index:])


@app.route("/bt_address", methods=['GET', 'POST'])
def bt_address():
    form = InformationForm()
    if form.validate_on_submit():
        error = 0
        try:
            urllib.request.urlopen(form.address.data)
        except urllib.error.HTTPError as e:
            error = 1
            flash('Downloading failed. Please check address!', 'danger')
        except urllib.error.URLError as e:
            error = 1
            flash('Downloading failed. Please check address!', 'danger')
        if error is not 1:
            flash('BitTorrent Download starts...', 'success')
            command = "aria2c -d /home/alphajun/cs176b/downloads --allow-overwrite=true --seed-time=0 --summary-interval=0 --follow-torrent=mem " + form.address.data
            os.system(command)
            flash('BitTorrent Download finished!', 'success')
            flash('Upload to Google Drive starts...', 'success')
            drive = GoogleDrive(gauth)
            for filename in glob.glob("/home/alphajun/cs176b/downloads/**", recursive=True):
                if not os.path.isdir(filename):
                    if filename not in uploaded:
                        file1 = drive.CreateFile()
                        file1.SetContentFile(filename)
                        file1.Upload()
                        uploaded.append(filename)
            return redirect(url_for('home'))
    return render_template('bt_address.html', title='BitTorrent', form=form)


@app.route("/http_address", methods=['GET', 'POST'])
def http_address():
    form = InformationForm()
    if form.validate_on_submit():
        error = 0
        try:
            urllib.request.urlopen(form.address.data)
        except urllib.error.HTTPError as e:
            error = 1
            flash('HTTP Downloading failed. Please check address!', 'danger')
        except urllib.error.URLError as e:
            error = 1
            flash('URL Error. Please check URL!', 'danger')
        if error is not 1:
            flash('HTTP Download starts...', 'success')
            filename = wget.download(form.address.data, "/home/alphajun/cs176b/downloads")
            flash('Upload to Google Drive starts...', 'success')
            time.sleep(1)
            drive = GoogleDrive(gauth)
            if filename not in uploaded:
                file1 = drive.CreateFile()
                file1.SetContentFile(filename)
                file1.Upload()
                uploaded.append(filename)
            return redirect(url_for('home'))
    return render_template('http_address.html', title='HTTP', form=form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
