import time
from flask import Flask, render_template, request
from zhi import ZhihuSpider
from billboard import hot,Zhihu

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        start = time.time()
        f = request.files['file']
        f.save(f.filename)
        ZhihuSpider(filename=f.filename)
        end = time.time()
        print("总共耗时：%f" % (end - start))
        return render_template('zhihu.html', name=f.filename)


@app.route('/zhihu', methods=['POST', 'GET'])
def zhihu():
    start = time.time()
    hot()
    Zhihu()
    end = time.time()
    print("总共耗时：%f" % (end - start))
    return render_template('zhihu.html')


if __name__ == '__main__':
    app.run(debug=True)
