from flask import Flask, render_template, abort

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/load_page/<page>')
def load_page(page):
    if page not in ['docker', 'kubernetes']:
        abort(404)  # Si la página no es válida, devolver un error 404
    return render_template(f'{page}.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)