import json
import datetime
from datetime import time
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


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
        club_name = request.args.get("club")
        club = [c for c in clubs if c["name"] == club_name][0]
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if c["name"] == competition][0]
    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchase-places", methods=["POST"])
def purchase_places():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])
    places_available = int(competition["number_of_places"])
    club_points = int(club["points"])
    now = datetime.datetime.now()
    competition_date = datetime.datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    error = False
    if competition_date < now :
        flash("You can't book places to an already passed competition")
        error = True
    if club_points < places_required :
        flash("You don't have enough points.")
        error = True
    if places_required > places_available:
        flash("Not enough places available.")
        error = True
    if places_required > 12 :
        flash("You can't book more than 12 places.")
        error = True
    if not error:
        competition["number_of_places"] = places_available - places_required
        club["points"] = club_points - places_required
        flash("Great-booking complete!")

    return redirect(url_for('show_summary', club=club["name"]))

# TODO: Add route for points display

@app.route("/points_display")
def points_display():
    return render_template("points_display.html", clubs=clubs)

@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
