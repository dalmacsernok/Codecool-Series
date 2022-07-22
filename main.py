from flask import Flask, render_template, url_for, jsonify
import data_handler

app = Flask('codecool_series')

@app.route('/')
def index():
    shows = data_handler.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/send-most-rated-shows/<offset>/<column>/<order>')
def send_most_rated_shows(offset, column, order):
    shows = data_handler.get_most_rated_shows(offset, column, order)
    return jsonify(shows)


@app.route('/shows/most-rated')
def most_rated_shows():
    return render_template('most_rated_shows.html')


@app.route('/show/<id>')
def get_detailed_show(id):
    details = data_handler.show_detailed_view(id)
    actors = data_handler.most_active_stars(id)
    seasons = data_handler.get_season(id)

    actors = ", ".join([x["actors"] for x in data_handler.most_active_stars(id)])
    if int(details[0]["runtime"]) < 60:
        details[0]["runtime"] = "{} min".format(*divmod(details[0]["runtime"], 1))
    elif int(details[0]["runtime"]) % 60 == 0:
        details[0]["runtime"] = "{} h".format(*divmod(details[0]["runtime"], 60))
    else:
        details[0]["runtime"] = "{} h {} min".format(*divmod(details[0]["runtime"], 60))
    return render_template('detailed_show.html', details=details, actors=actors, seasons=seasons)

def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
