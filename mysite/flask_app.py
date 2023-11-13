from flask import Flask, redirect, render_template, request, url_for
import idleonTaskSuggester

app = Flask(__name__)
app.config["DEBUG"] = True

capturedCharacterInput = ""

text3 = "Text 3 content"
text4 = "Text 4 content"
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        output = [""]*20
        output[1] = ["Please hit submit with Valid profile to populate data"]
        return render_template("main_page.html") #, output=output)
    if request.method == "POST":
        capturedCharacterInput = request.form["characterInput"]
        output = autoReviewBot(capturedCharacterInput)
        return render_template("results.html", output=output)


#@app.route("/", methods=["GET"])
def autoReviewBot(capturedCharacterInput):
    reviewInfo = ""
    if not capturedCharacterInput:
        reviewInfo = ["placeholder"]
    else:
        reviewInfo = idleonTaskSuggester.main(capturedCharacterInput)
    #Do review stuff function, passinto array
    return reviewInfo


if __name__ == '__main__':
    app.run()
