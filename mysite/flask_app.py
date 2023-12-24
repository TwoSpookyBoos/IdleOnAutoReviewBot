from flask import Flask, render_template, request, url_for, redirect
import idleonTaskSuggester

app = Flask(__name__)
app.config["DEBUG"] = True


def format_character_name(name: str) -> str:
    name = name.strip().lower().replace(' ', '_')

    return name


def get_character_name() -> str:
    name: str = request.args.get('player', '') or request.form["player"]
    name = format_character_name(name)

    return name


@app.route("/review", defaults=dict(main_or_beta=""), methods=["GET", "POST"])
@app.route("/review/<main_or_beta>", methods=["GET", "POST"])
def index(main_or_beta: str) -> str:
    page: str = 'beta_results.html' if main_or_beta == 'beta' else 'results.html'
    error: bool = False
    pythonOutput: list | None = None

    try:
        capturedCharacterInput: str = get_character_name()
        # print("FlaskApp.index~ OUTPUT request.args.get('player'):",type(capturedCharacterInput),capturedCharacterInput)
        if capturedCharacterInput:
            pythonOutput = autoReviewBot(capturedCharacterInput)

        if len(capturedCharacterInput) > 15:
            page = 'beta_results.html'

    except Exception as reason:
        print("FlaskApp.index~ Could not get Player from Request Args:", reason)
        error = True

    return render_template(page, htmlInput=pythonOutput, error=error)


# @app.route("/")
def autoReviewBot(capturedCharacterInput):
    reviewInfo: list | None = None
    if capturedCharacterInput:
        reviewInfo = idleonTaskSuggester.main(capturedCharacterInput)
    # Do review stuff function, pass into array
    return reviewInfo


@app.errorhandler(404)
def page_not_found(e):
    try:
        if len(request.path) < 16:
            capturedCharacterInput = request.path[1:].strip().replace(" ", "_").lower()
            if capturedCharacterInput.find(".") == -1:
                return redirect(url_for('index', player = capturedCharacterInput))
            else:
                return redirect(url_for('index')) # Probably should get a real 404 page at some point
        else:
            return redirect(url_for('index')) # Probably should get a real 404 page at some point
    except:
        return redirect(url_for('index')) # Probably should get a real 404 page at some point


def ensure_data(results: list):
    return bool(results)


def img(filename: str):
    return url_for('static', filename=f'imgs/{filename}')


app.jinja_env.globals['ensure_data'] = ensure_data
app.jinja_env.globals['img'] = img

if __name__ == '__main__':
    app.run()
