workflow "Main Workflow" {
  on = "push"
  resolves = ["Test"]
}

action "Setup" {
  uses = "docker://python:3.7.2-slim"
  runs = "pip"
  args = ["install", "--user", "tox"]
}

action "Test" {
  needs = "Setup"
  uses = "docker://python:3.7.2-slim"
  runs = "python"
  args = ["-m", "tox"]
}
