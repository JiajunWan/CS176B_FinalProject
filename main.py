import os, webbrowser, urllib, pyYify, wget
from flask import Flask, render_template, url_for, flash, redirect
from forms import InformationForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdf'

downloaded = []
uploaded = []

# http://releases.ubuntu.com/18.04/ubuntu-18.04.2-desktop-amd64.iso.torrent
# http://releases.ubuntu.com/18.04/ubuntu-18.04.2-desktop-amd64.iso.torrent?_ga=2.66795821.2059850810.1551004639-1774269339.1551004639


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


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
            filename = wget.download(form.address.data, "/home/jiajunwan2015/cs176b/CS176B_FinalProject/downloads")
            downloaded.append(filename)
            return redirect(url_for('home'))
    return render_template('http_address.html', title='HTTP', form=form)


if __name__ == '__main__':
    app.run(debug=True)