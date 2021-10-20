from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

boggle_game = Boggle()

debug = DebugToolbarExtension(app)

@app.route("/")
def create_board():
  """draw the html board, set board, set the session, high score and number of plays. Call index.html """
  board = boggle_game.make_board()
  session['board'] = board
  highscore = session.get("highscore", 0)
  nplays = session.get("nplays", 0)

  return render_template("draw_board.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route("/test-word")
def test_word():
  """Check if the word is in the dictionary or rather the list of words imported into board.py"""
  word = request.args['word']
  board=session["board"]
  response = boggle_game.check_valid_word(board, word)
  return jsonify({'result':response})



@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    
    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore) 





