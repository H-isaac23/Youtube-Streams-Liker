from flask import Flask, render_template
from YSL import StreamLiker
import os

email = os.environ.get('TEST_EMAIL')
passwd = os.environ.get('TEST_PASS')
sl = StreamLiker('channel ids.txt', email, passwd)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/like')
def like():
    sl.start_liking_with_data("isaac", "localhost", "DevAisha23!", "YSL")
    sl.clear_data()
    return render_template('like.html')

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.10')