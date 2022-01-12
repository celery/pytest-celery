import nox


@nox.session
def test(session):
    requirements = session.run_always(
        "poetry", "export", "-f", "requirements.txt", "--with", "test", "--without-hashes", silent=True, external=True
    )
    session.install(*[req for req in requirements.split("\n") if req])

    session.run("pytest", "-nauto", "--cov=pytest_celery", "--cov-branch", "--cov-report=xml")
