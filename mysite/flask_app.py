from flask import Flask, redirect, render_template, request, url_for
import idleonTaskSuggester

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
            pythonOutput = autoReviewBot(capturedCharacterInput)
            return render_template("results.html", htmlInput = pythonOutput)
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

@app.errorhandler(404)
def page_not_found(e):
    try:
        if len(request.path) <= 16:
            capturedCharacterInput = request.path[1:]
            pythonOutput = autoReviewBot(capturedCharacterInput)
            return render_template("results.html", htmlInput = pythonOutput)
    except:
        return render_template("main_page.html")

if __name__ == '__main__':
    app.run()
