workflow "Test" {
  on = "push"
  resolves = "Test: Run"
}

action "Test: Setup" {
  uses = "docker://python:3.7.2-slim"
  runs = "pip"
  args = ["install", "--user", "tox"]
}

action "Test: Run" {
  needs = "Test: Setup"
  uses = "docker://python:3.7.2-slim"
  runs = "python"
  args = ["-m", "tox"]
}


workflow "Release" {
  on = "push"
  resolves = "Release: Publish"
}

action "Release: Filter" {
  uses = "actions/bin/filter@master"
  args = "tag v*"
}

action "Release: Test Setup" {
  needs = "Release: Filter"
  uses = "docker://python:3.7.2-slim"
  runs = "pip"
  args = ["install", "--user", "tox"]
}

action "Release: Test" {
  needs = "Release: Test Setup"
  uses = "docker://python:3.7.2-slim"
  runs = "python"
  args = ["-m", "tox"]
}

action "Release: Build" {
  needs = "Release: Test"
  uses = "ross/python-actions/setup-py/3.7@627646f618c3c572358bc7bc4fc413beb65fa50f"
  args = "sdist bdist_wheel"
}

action "Release: Publish" {
  needs = "Release: Build"
  uses = "ross/python-actions/twine@627646f618c3c572358bc7bc4fc413beb65fa50f"
  args = "upload ./dist/*"
  secrets = ["TWINE_USERNAME", "TWINE_PASSWORD"]
}
