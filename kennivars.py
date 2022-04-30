from flask import Flask, render_template, session
app = Flask(__name__)

def render_template_with_login(template, **variables):
    logged_in = session.get('name')
    variables.update({'logged_in': logged_in})
    return render_template(template, **variables)

@app.route('/')
def hello():
    djs = []
    return render_template_with_login('index.html', djs=djs, logged_in=False)

if __name__ == '__main__':
    app.run(debug=True)



# it's the wrong way around above - don't want to override the vars

    # from flask import Flask, render_template, session
# app = Flask(__name__)

# def render_template_with_login(template, **variables):
#     logged_in = session.get('name')
#     return render_template(template, logged_in=logged_in, **variables)

# @app.route('/')
# def hello():
#     djs = []
#     return render_template_with_login('index.html', djs=djs, logged_in=False)

# if __name__ == '__main__':
#     app.run(debug=True)
