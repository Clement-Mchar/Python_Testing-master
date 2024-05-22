import json
import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs

def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions

def save_clubs(data):
    with open("clubs.json") as c:
        clubs_data = json.load(c)
        clubs_list = clubs_data["clubs"]
        for i, club in enumerate(clubs_list):
            if club["name"] == data["name"]:
                clubs_list[i] = data
    with open("clubs.json", 'w') as c:
        json.dump(clubs_data, c, ensure_ascii=False, indent=4)

def save_competitions(data):
    with open("competitions.json") as comps:
        competitions_data = json.load(comps)
        competitions_list = competitions_data["competitions"]
        for i, competition in enumerate(competitions_list):
            if competition["name"] == data["name"]:
                competitions_list[i] = data
                break
    with open("competitions.json", 'w') as c:
        json.dump(competitions_data, c, ensure_ascii=False, indent=4)

app = Flask(__name__)
app.secret_key = "something_special"
app.debug = True

competitions = load_competitions()
clubs = load_clubs()

@app.route("/")
def index():
    return render_template("index.html", form=request.form)

@app.route("/show-summary", methods=["POST", "GET"])
def show_summary():
    if request.method == "POST":
        try:
            club = [club for club in clubs if club["email"] == request.form["email"]][0]
        except (IndexError, TypeError):
            flash("This email is invalid, try again.")
            return redirect(url_for("index"))
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        try:
            club_name = request.args.get("club")
            club = [c for c in clubs if c["name"] == club_name][0]
        except IndexError:
            return render_template("page_not_found.html")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        found_club = [c for c in clubs if c["name"] == club][0]
        found_competition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        return render_template("page_not_found.html")
    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )


@app.route("/purchase-places", methods=["POST"])
def purchase_places():
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    try:
        places_required = int(request.form["places"])
    except ValueError:
        flash('Please enter a valid number of places.')
        return render_template(
            "booking.html", club=club, competition=competition
        )
    places_available = int(competition["number_of_places"])
    club_points = int(club["points"])
    now = datetime.datetime.now()
    competition_date = datetime.datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    error = False
    error_messages = []
    if competition_date < now :
        error = True
        error_messages.append("You can't purchase places to an already passed competition.")
    if club_points < places_required :
        error = True
        error_messages.append("You don't have enough points.")
    if places_required > places_available:
        error = True
        error_messages.append("Not enough places available.")
    if places_required > 12 :
        error = True
        error_messages.append("You can't book more than 12 places.")
    if places_required < 0:
        error = True
        error_messages.append("You can't book a negative number of places.")
    if not error:
        competition["number_of_places"] = places_available - places_required
        competition["number_of_places"] = str(competition["number_of_places"])
        club["points"] = club_points - places_required
        club["points"] = str(club["points"])
        save_clubs(club)
        save_competitions(competition)
        flash("Great-booking complete !")
        flash(f"You have booked {places_required} places to the {competition["name"]} competition !")
    else :
        flash("Something went wrong :")
        for message in error_messages:
            flash(message)
    return redirect(url_for('show_summary', club=club["name"]))

# TODO: Add route for points display

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route("/points_display")
def points_display():
    return render_template("points_display.html", clubs=clubs)

@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
