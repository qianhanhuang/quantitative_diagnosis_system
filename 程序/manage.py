import app
from route import *

app = app.create_app()

app.login_manager.user_loader(load_user)
app.login_manager.unauthorized_handler(unauthorized)

app.add_url_rule(index.route_index, view_func=index.func, methods=index.methods)
for rule in maps:
    app.add_url_rule(rule.route_index, view_func=login_required(rule.func), methods=rule.methods)

if __name__ == '__main__':
    app.run(debug=True,port=5001,host="127.0.0.1")