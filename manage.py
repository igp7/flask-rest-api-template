import unittest
import click
from app import db
from app.api.models import Users
import coverage


@click.option("--pattern", default='tests_*.py', help='Patron búsqueda de tests', required=False)
def cov(pattern):
    """
    Run the unit tests with coverage
    """
    cov = coverage.coverage(
        branch=True,
        include='app/*'
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests', pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        cov.erase()
        return 0
    return 1


@click.option("--pattern", default='tests_*.py', help='Patron búsqueda de tests', required=False)
def cov_html(pattern):
    """
    Run the unit tests with coverage and report in html
    """
    cov = coverage.coverage(
        branch=True,
        include='app/*'
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests', pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        cov.html_report(directory='report/htmlcov')
        cov.erase()
        return 0
    return 1


@click.option("--pattern", default='tests_*.py', help='Patron búsqueda de tests', required=False)
def tests(pattern):
    """
    Run the tests without code coverage
    """
    tests = unittest.TestLoader().discover('tests', pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


def create_db():
    """
    Create Database.
    """
    db.create_all()
    db.session.commit()


def reset_db():
    """
    Reset Database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


def drop_db():
    """
    Drop Database.
    """
    db.drop_all()
    db.session.commit()


@click.option("--name", default="admin", help='Name user Admin')
@click.option("--password", default="1234", help='Password user Admin')
def create_user_admin(name, password):
    """
    Create User Admin.
    """
    admin = Users.simple_filter(name=name, admin=True)
    if admin is None:
        user = Users(name=name, password=password, admin=True)
        user.save()


def init_app(app):
    if app.config['APP_ENV'] == 'production':
        commands = [create_db, reset_db, drop_db, create_user_admin]
    else:
        commands = [create_db, reset_db, drop_db, create_user_admin, tests, cov, cov_html]

    for command in commands:
        app.cli.add_command(app.cli.command()(command))
