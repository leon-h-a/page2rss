from flask import Flask, render_template, send_file 
from page2rss import OUTPUT_DIR
from page2rss.webapp import logger

app = Flask(__name__)
# note: do not use scraper, scraper shall have 
#       filwatcher on global input dir


@app.route("/")
def root():
    # todo: also sent out all already available pages inside OUTPUT_DIR
    return render_template("index.html")


@app.route("/add-entry", methods=["POST"])
def add_entry():
    # pg = PageEntry(
    #     nick=request.form.get("nick", "").strip(),
    #     url=request.form.get("url", "").strip(),
    #     tag=request.form.get("tag", "").strip(),
    #     css=request.form.get("css", "").strip()
    # )
    # logger.info(pg)
    return render_template("index.html")


@app.route("/remove-entry", methods=["POST"])
def remove_entry():
    return render_template("index.html")


@app.route("/scrape", methods=["GET"])
def scrape():
    # todo: add safety checks and fe notifications
    #       1. ping website and notify front
    #       2. notify if bs4 returns empty list for tag&css combo
    #       3. notify that sub-pages are scraped
    #       4. notify that xml is created and stored
    #       5. notify that index of <page>.html is stored
    pass


@app.route("/feed/<xml_filename>")
def feed_serve(xml_filename):
    logger.info(f"client requested: /feed/{xml_filename}")
    xml_file = OUTPUT_DIR.resolve() / xml_filename

    if not xml_file.exists():
        abort(404, description="feed not found")

    return send_file(
        xml_file,
        mimetype="application/rss+xml"
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=1234,
        debug=True
    )
