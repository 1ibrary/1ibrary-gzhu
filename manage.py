"""
Author: Tyan boot <tyanboot@outlook.com>
Date: 2017/6/18

"""

# -*- coding: utf-8 -*-

from yitu import create, db

from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager, Shell
import os

app = create(os.getenv("yitu_cfg") or "default")


@app.teardown_request
def teardown(e):
    if e:
        db.session.rollback()
        db.session.remove()
    else:
        db.session.commit()

    db.session.remove()


manage = Manager(app)
migrate = Migrate(app, db)

manage.add_command("db", MigrateCommand)
manage.add_command("shell", Shell(make_context=lambda: {"app": app, "db": db}))

if __name__ == "__main__":
    manage.run()
