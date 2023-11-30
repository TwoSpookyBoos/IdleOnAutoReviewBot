from flask import Flask, redirect, render_template, request, url_for
import idleonTaskSuggester
#import beta_idleonTaskSuggester

app = Flask(__name__)
app.config["DEBUG"] = True

capturedCharacterInput = ""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html") #, output=output)
    if request.method == "POST":
        capturedCharacterInput = request.form["characterInput"]
        if capturedCharacterInput != "":
            output = autoReviewBot(capturedCharacterInput)
            return render_template("results.html", output=output)
        else:
            return render_template("main_page.html")

#@app.route("/")
def autoReviewBot(capturedCharacterInput):
    reviewInfo = ""
    if not capturedCharacterInput:
        reviewInfo = ["placeholder"]
    else:
        reviewInfo = idleonTaskSuggester.main(capturedCharacterInput)
    #Do review stuff function, passinto array
    return reviewInfo

@app.route("/beta", methods=["GET", "POST"])
def betaIndex():
    if request.method == "GET":
        return render_template("beta_main_page.html")
    if request.method == "POST":
        capturedCharacterInput = request.form["beta_characterInput"]
        if capturedCharacterInput != "":
            beta_output = beta_autoReviewBot(capturedCharacterInput)
            return render_template("beta_results.html", output=beta_output)
        else:
            return render_template("beta_main_page.html")
    #return redirect(url_for('beta_results')) #

#@app.route("/beta_results", methods=["GET"])
def beta_autoReviewBot(capturedCharacterInput):

    beta_reviewInfo = ""
    if not capturedCharacterInput:
        beta_reviewInfo = ["placeholder"]
    else:
        beta_reviewInfo = beta_idleonTaskSuggester.main(capturedCharacterInput)
    #Do review stuff function, passinto array
    return beta_reviewInfo

if __name__ == '__main__':
    app.run()
