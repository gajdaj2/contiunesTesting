from flask import Flask, render_template_string

app = Flask(__name__)

HOME_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>CT Demo App</title>
  </head>
  <body>
    <h1 id="title">UI Test App</h1>
    <p id="intro">Prosta aplikacja do testow UI.</p>
    <a id="info-link" href="/info">More information</a>
  </body>
</html>
"""

INFO_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Info</title>
  </head>
  <body>
    <h1 id="info-title">Info Page</h1>
    <p id="details">Dane testowe dla Selenium.</p>
  </body>
</html>
"""


@app.get("/")
def home():
    # Prosta strona domyslna do testow UI.
    return render_template_string(HOME_HTML)


@app.get("/info")
def info():
    return render_template_string(INFO_HTML)


if __name__ == "__main__":
    # Uruchamiaj lokalnie, by testy UI mialy stabilny cel.
    app.run(host="127.0.0.1", port=5000, debug=False)

