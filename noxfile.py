import nox


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
@nox.parametrize("suite", ["unit", "functional", "integration"])
def test(session, suite):
    session.run_always("poetry", "lock", external=True)
    requirements = session.run_always(
        "poetry",
        "export",
        "-f",
        "requirements.txt",
        "--with",
        "test",
        "--without-hashes",
        silent=True,
        external=True,
        env={"PYTHONWARNINGS": "ignore"},
    )
    session.install(*[req.strip() for req in requirements.split("\n") if req.strip()])

    test_args = session.posargs or ("-nauto", "--cov=pytest_celery", "--cov-branch", "--cov-report=xml")
    session.run("pytest", f"tests/{suite}", *test_args)
