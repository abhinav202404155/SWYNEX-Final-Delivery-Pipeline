# SWYNEX-Final-Delivery-Pipeline

![Pipeline](https://github.com/abhinav202404155/SWYNEX-Final-Delivery-Pipeline/actions/workflows/pipeline.yml/badge.svg)

This is the last task of my internship with SWYNEX Technologies, and it ties the earlier two
together. In task 2 I set up CI for a small expense tracker. In task 3 I put that tracker in
a Docker container. Here I connected both so that pushing one git tag takes the code all the
way to a published Docker image and a GitHub release, without me doing any step by hand.

The app is still the same small Flask API that keeps expenses in a JSON file. It isn't the
interesting part. What I cared about this time was the route it takes out of my laptop.

## How a release happens

When I push to `main`, GitHub Actions lints the code, runs the tests, builds the Docker image
and starts it to check that it really answers requests. That is the "is this safe" part and
nothing gets published.

When I push a tag like `v1.0.0`, those same checks run first. If they pass, the image is
pushed to GitHub Container Registry under that version number, and a GitHub release is
created. The text of the release comes from the matching section in `CHANGELOG.md`, so the
release notes are something I write together with the code change, and the pipeline just
picks them up.

The longer explanation, with screenshots of a real run, is in
[docs/PIPELINE.md](docs/PIPELINE.md).

## Making a release

Add a section for the new version to `CHANGELOG.md`, commit it, then tag and push:

```
git tag v1.0.0
git push origin v1.0.0
```

Open the Actions tab and wait a couple of minutes. When it finishes there is a new entry
under Releases and a new version under Packages.

## Running the published image

You only need Docker.

```
docker run -d -p 8000:8000 -v expense-data:/data ghcr.io/abhinav202404155/swynex-final-delivery-pipeline:latest
```

The package is private the first time it is pushed. If you can't pull it, the owner has to
switch it to public in the package settings on GitHub.

## Running it from source

```
git clone https://github.com/abhinav202404155/SWYNEX-Final-Delivery-Pipeline.git
cd SWYNEX-Final-Delivery-Pipeline
docker compose up --build -d
```

Stop it with `docker compose down`. The data lives in a named volume, so it is still there
after you start it again. `docker compose down -v` deletes it as well.

## Trying the API

Linux, Mac or Git Bash:

```
curl http://localhost:8000/health
curl http://localhost:8000/version
curl -X POST http://localhost:8000/expenses -H "Content-Type: application/json" -d '{"amount": 250, "category": "travel"}'
curl http://localhost:8000/summary
```

On Windows PowerShell `curl` is something else, so use this instead:

```
Invoke-RestMethod http://localhost:8000/version
Invoke-RestMethod -Method Post -Uri http://localhost:8000/expenses -ContentType "application/json" -Body '{"amount": 250, "category": "travel"}'
Invoke-RestMethod http://localhost:8000/summary
```

`/version` returns whatever version was given to the image when it was built. A local build
says `dev`, a released image says the tag, for example `1.0.0`.

## Working on it locally

```
python -m venv .venv
.venv\Scripts\activate          # on Linux or Mac: source .venv/bin/activate
pip install -r requirements-dev.txt
ruff check .
pytest
```

## A few things I ran into

If you start it with `docker compose up` and no `-d`, the container runs inside that terminal
window and stops as soon as you close it or press Ctrl+C. I lost some time on this during
task 3 because my health check kept failing with nothing running.

Gunicorn runs with a single worker on purpose. All expenses go into one JSON file, and two
workers writing to it at the same time could overwrite each other. Moving to a real database
would be the proper fix.

When I unzipped my earlier project I ended up with a folder inside a folder, and git was
initialised in the wrong one. Worth checking with `git status` before pushing.

## Author

Abhinav Kashyap, [@abhinav202404155](https://github.com/abhinav202404155)
