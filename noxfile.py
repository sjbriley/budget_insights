import nox

@nox.session
def lint(session):
    session.install('pylama')
    session.run(
        'pylama', 'budget_insights',
        '--report', 'pylama_report',
        '--format', 'parsable')

@nox.session
def pytest(session):
    session.install('pytest', 'pytest-cov', '-r', 'requirements.txt')
    session.run(
        'pytest', 'budget_insights',
        '--cov-config=.coveragerc',
        '--cov-report', 'html',
        '--cov-report', 'xml',
        '--cov=budget_insights',
        '--cov-fail-under=80')
