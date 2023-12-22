from flask import Flask, render_template, request, url_for, redirect
import idleonTaskSuggester

app = Flask(__name__)
app.config["DEBUG"] = True

capturedCharacterInput = ""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        try:
            capturedCharacterInput = request.args.get('player')
            #print("FlaskApp.index~ OUTPUT request.args.get('player'):",type(capturedCharacterInput),capturedCharacterInput)
            if isinstance(capturedCharacterInput, str) and capturedCharacterInput != "":
                pythonOutput = autoReviewBot(capturedCharacterInput)
                return render_template("results.html", htmlInput = pythonOutput)
            else:
                return render_template("main_page.html")
        except Exception as reason:
            print("FlaskApp.index~ Could not get Player from Request Args:",reason)
        return render_template("main_page.html")
    elif request.method == "POST":
        capturedCharacterInput = request.form["characterInput"]
        if len(capturedCharacterInput) > 15:
            pythonOutput = autoReviewBot(capturedCharacterInput)
            return render_template("results.html", htmlInput = pythonOutput)
        else:
            return redirect(url_for('index', player = capturedCharacterInput))
        return render_template("main_page.html")
    else: #shouldn't ever happen. Every instance should be a GET or a POST
        return render_template("main_page.html")

@app.route("/beta", methods=["GET", "POST"])
def betaIndex():
    if request.method == "GET":
        try:
            capturedCharacterInput = request.args.get('player')
            #print("FlaskApp.betaIndex~ OUTPUT request.args.get('player'):",type(capturedCharacterInput),capturedCharacterInput)
            if isinstance(capturedCharacterInput, str) and capturedCharacterInput != "":
                pythonOutput = autoReviewBot(capturedCharacterInput)
                return render_template("beta_results.html", htmlInput = pythonOutput)
            else:
                return render_template("beta_main_page.html")
        except Exception as reason:
            print("FlaskApp.index~ Could not get Player from Request Args:",reason)
        return render_template("beta_main_page.html")
    elif request.method == "POST":
        capturedCharacterInput = request.form["characterInput"]
        if len(capturedCharacterInput) > 15:
            pythonOutput = autoReviewBot(capturedCharacterInput)
            return render_template("beta_results.html", htmlInput = pythonOutput)
        else:
            return redirect(url_for('betaIndex', player = capturedCharacterInput))
        return render_template("beta_main_page.html")
    else: #shouldn't ever happen. Every instance should be a GET or a POST
        return render_template("beta_main_page.html")

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
        if len(request.path) < 16:
            capturedCharacterInput = request.path[1:]
            if capturedCharacterInput.find(".") == -1:
                return redirect(url_for('index', player = capturedCharacterInput))
            else:
                return redirect(url_for('index')) #Probably should get a real 404 page at some point
        else:
            return redirect(url_for('index')) #Probably should get a real 404 page at some point
    except:
        return redirect(url_for('index')) #Probably should get a real 404 page at some point

if __name__ == '__main__':
    app.run()
