# Frame Recorder: Review, Concepts and Roadmap

Nov 12, 2026 · @Sergio

## Review

The Flask app in your zip does not start: two files are damaged, two are missing, and one is in the wrong shape. The plugin code is sound but its panel had a startup bug, now fixed.

### What is wrong

- `app/routes.py` holds the model classes (the full set, including Frame), not routes, while app/models.py is an older copy without Frame. Python imports it, defines `User` twice, and crashes with `Table 'user' is already defined`. The `/`, `/login` and `/feed` routes are gone.
- `app/frames_api.py` has two spaces in front of line 1 (`   import hashlib `), so Python raises `IndentationError`.
- `app/__init__.py` imports `cli`, but `app/cli.py` and `app/atn_import.py` are not in the zip, so you would get `ImportError` even after the two fixes above. It also never imports frames\_api, so /api/frames would answer 404 and the panel could not upload.
- `app/templates/base.html` contains a pasted HTML table, not a page layout. It has no `{% block content %}`, so `index.html`, `login.html` and `feed.html` render nothing.
- There is no `migrations/` folder and `app.db` is 0 bytes, so no tables exist. Nothing can be stored until you run the migration commands.
- `requirements.txt` is UTF-16 (PowerShell's `>` does that) and dates from Oct 29. It lacks Flask-SQLAlchemy, Flask-Migrate, Flask-WTF, WTForms and Alembic, so a fresh install would not run your app.
- `timelapse.py` replaced `microblog.py` as the entry point but its shell context only knows `User` and `Post`, not `PsStroke` or `Frame`.
- `app/.pytest_cache` shows `test_atn_import.py` failing: pytest was run from inside `app/`, where the test cannot find its files.
- Design gaps, not bugs: nothing links a frame to a user or a recording session, the upload endpoint accepts anyone while `FRAMES_API_TOKEN` is unset, and there is no page that shows frames.
- Plugin: the panel was stuck on "starting...". Two causes produce that exact symptom: `CSInterface.js` missing from `js/`, or Photoshop's Node `module` object making `uploader.js` skip its global export. I fixed the second and the panel now prints which problem it has.
- Plugin limits you should know: `imageChanged` fires on every edit and Generator warns it is expensive, there is no maximum wait, layer name and colour are read slightly after the pixels, and the panel must stay open to upload.

### What is good

- `PsStroke` and `Frame` are correctly modelled: unique `(session_id, seq)`, check constraints, `JSON(none_as_null=True)`, a SHA-256 column that makes re-uploads harmless.
- `POST /api/frames` validates everything it receives (JPEG magic bytes, JSON object, hex colour, safe filename) and never uses a client path.
- The Generator code debounces per document, captures one at a time, and writes `.part` then renames, so no one sees half-written files.
- The panel keeps files on failure and retries; uploads are idempotent, so a retry cannot create duplicates.
- 22 Node tests pass, including a simulated Photoshop panel page and an ExtendScript run with hostile layer names.

## Fix list: get the app running

Replace 9 files, reinstall the dependencies, create the database tables, then run. I applied exactly these steps to a copy of your zip and the app served `/`, `/login`, `/feed` and accepted a frame upload at `/api/frames`.

### Files to replace (sent with this reply)

| File | What was wrong | Replacement |
| --- | --- | --- |
| `app/models.py` | Missing `Frame` | Full set: `User`, `Post`, `PsStroke`, `Frame` |
| `app/routes.py` | Contains model code | The three routes: `/`, `/login`, `/feed` |
| `app/frames_api.py` | Two spaces before line 1 | Same code, indentation fixed |
| `app/__init__.py` | Does not import `frames_api` | Last line imports it |
| `app/cli.py` | Missing | The `flask import-atn` command |
| `app/atn_import.py` | Missing | The `.atn` converter that `cli.py` uses |
| `app/templates/base.html` | A pasted table | Page layout with `{% block content %}` |
| `timelapse.py` | Shell knows only `User`, `Post` | Also knows `PsStroke`, `Frame` |
| `requirements.txt` | UTF-16, incomplete | UTF-8, 16 pinned packages |

### Steps (PowerShell, from the folder that holds `timelapse.py`)

1. Copy the whole folder somewhere as a backup.
2. Put the 9 files in place. Delete `app.db` (it is empty) and `app/.pytest_cache`.
3. Create a virtual environment and install: `python -m venv .venv`, then `.venv\Scripts\Activate.ps1`, then `pip install -r requirements.txt`.
4. Tell Flask which file is the app: `$env:FLASK_APP = "timelapse.py"`.
5. Create the tables: `flask db init`, then `flask db migrate -m "initial"`, then `flask db upgrade`. A `migrations/` folder appears and `app.db` fills up.
6. Run: `flask run`. Open `http://127.0.0.1:5000/feed`. It is empty.
7. Load the strokes: `flask import-atn "C:\path\to\action_test.atn"`, refresh `/feed`.
8. Test the upload without Photoshop. Put any JPEG at `t.jpg` and this text at `t.json`: `{"document":"a.psd","layer":"L1","foreground_color":"#ff8800"}`. Then run `curl.exe -F "frame=@t.jpg" -F "meta=@t.json" http://127.0.0.1:5000/api/frames`. You get `{"id":1,"duplicate":false}`; running it again gives `duplicate: true`.
9. Check the row: `flask shell`, then `db.session.scalars(sa.select(Frame)).all()`.

### Plugin side

1. Download `CSInterface.js` from Adobe's CEP-Resources repository (see Reading list) into `cep-extension/js/`. Without it the panel shows an error on screen.
2. Allow unsigned panels. In PowerShell: `foreach ($v in 9..12) { New-Item -Path "HKCU:\Software\Adobe\CSXS.$v" -Force | Out-Null; New-ItemProperty -Path "HKCU:\Software\Adobe\CSXS.$v" -Name PlayerDebugMode -Value "1" -PropertyType String -Force | Out-Null }`. Restart Photoshop.
3. Use the new `main.js`, `uploader.js` and `index.html` from the latest files, copy the folder to `%APPDATA%\Adobe\CEP\extensions\frame-recorder`, and reopen the panel from Window > Extensions.
4. Create `generator.json` in your user folder: `{"frame-recorder": {"outputFolder": "C:\\frames"}}`. The same file feeds both the Generator and the panel.
5. Read the panel's status line. `watching` means the panel works. Any other text names the missing piece.

## Flask from scratch

Flask is a Python library that waits for HTTP requests and calls the function you registered for that address. Everything else in your project is organisation around that one idea.

### Five ideas to hold

1. **HTTP request and response.** A client (browser, your panel, `curl`) sends text: a method (`GET` reads, `POST` sends data), a path (`/feed`), headers, and sometimes a body. The server answers with a status code, headers and a body. Codes you will meet: 200 OK, 201 Created, 400 you sent something invalid, 401 not allowed, 404 no such route, 500 your code crashed.
2. **The app object.** `app = Flask(__name__)` is a registry: it remembers which function handles which path, and holds the settings.
3. **A route** is a function plus a decorator. `@app.route('/feed')` tells the registry "call this for `GET /feed`". What the function returns becomes the response: `render_template(...)` returns HTML, `jsonify(...)` returns JSON.
4. **Templates (Jinja)** are HTML with holes: `{{ value }}` prints something, `{% for %}` loops. `{% extends "base.html" %}` plus `{% block content %}` is inheritance: `base.html` is the frame (nav bar, `<head>`), each page fills the block. That is why a broken `base.html` blanked every page.
5. **Config and extensions.** `config.py` holds settings, loaded by `app.config.from_object(Config)`. `SQLAlchemy(app)` and `Migrate(app, db)` plug the database in. An extension is a library that attaches itself to your app.

### How your project is organised

| File or folder | Job |
| --- | --- |
| `timelapse.py` | Entry point. `FLASK_APP` points at it; it imports the app and defines what `flask shell` preloads |
| `config.py` | Settings: secret key, database address |
| `app/__init__.py` | Creates `app`, `db`, `migrate`; imports the other modules last |
| `app/models.py` | Tables written as Python classes |
| `app/routes.py` | Pages people see: `/`, `/login`, `/feed` |
| `app/frames_api.py` | The upload endpoint the panel calls |
| `app/cli.py` | Terminal commands (`flask import-atn`) |
| `app/forms.py` | The login form |
| `app/templates/` | Jinja pages |
| `migrations/` | The history of database changes (Alembic) |
| `app.db` | The SQLite database file itself |

Why the imports sit at the bottom of `app/__init__.py`: each module starts with `from app import app, db`, which needs `app` to exist already. So `app` is created first and the modules that use it are imported after. This circular layout is the Mega-Tutorial's; it works, and it is the first thing to restructure when the project grows (see Roadmap, phase 5).

### Walk-through: one frame upload, step by step

1. The panel sends `POST /api/frames`. The body has two parts: `frame` (JPEG bytes) and `meta` (JSON text).
2. Flask looks up `POST /api/frames` and finds `upload_frame`. It is registered only because `frames_api` was imported at startup. No import, no route, a 404.
3. `request.files.get("frame")` returns the first part; `.read()` gives bytes starting `ff d8 ff`. The code checks those three bytes: a JPEG always starts with them. State: `jpeg` = bytes.
4. `json.loads(...)` turns the `meta` text into a Python dict, e.g. `{"layer": "L1", "foreground_color": "#ff8800", ...}`. State: `meta` = dict.
5. `hashlib.sha256(jpeg).hexdigest()` gives 64 hex characters that depend on every byte. State: `digest` = `'9f2c...'`.
6. A `SELECT` asks the database for a frame with that digest. Found: reply 200 `duplicate: true` and stop. Not found (first upload): continue.
7. The code picks a safe filename and writes the bytes to `instance/frames/`. State: file on disk.
8. `Frame(...)` builds an object in memory. `db.session.add(row)` marks it to be saved. `db.session.commit()` runs the `INSERT`. State: `row.id` is now `1`.
9. The function returns `jsonify(id=1, duplicate=False), 201`. Flask turns that into the HTTP response; the panel sees 201 and moves the files to `sent/`.

### Request context and app context

`request` looks like a global variable but Flask swaps its contents for every incoming request. Likewise `db.session` needs to know which app it belongs to. Inside a route both are set up for you. In a plain script you must open one yourself: `with app.app_context(): ...`. `flask shell` and `@app.cli.command` do it for you.

## Database concepts

A table is a spreadsheet whose rules the database enforces. SQLAlchemy lets you describe tables as Python classes, and migrations record every change to them as numbered steps.

### Tables as classes

- `class Frame(db.Model)` is the table `frames`. Each `mapped_column` is a column.
- `so.Mapped[int]` means "never empty". `so.Mapped[Optional[str]]` means the column may hold `NULL` (no value).
- `primary_key=True` is the row's unique id. `unique=True` makes the database refuse a second row with the same value; `Frame.sha256` uses it.
- `index=True` builds a lookup structure, like a book's index, so searching by that column is fast. `captured_at_ms` has one.
- A `CheckConstraint` is a rule on each row. `PsStroke` uses one to say "a `points` stroke must have points".
- A `JSON` column stores nested data (`Frame.meta`, `PsStroke.points`) without needing a column per field. The price: the database cannot index inside it as easily as a normal column.

### The session is a shopping basket

`db.session.add(obj)` puts an object in the basket. `db.session.commit()` writes everything in the basket as one transaction: all of it or none of it. `rollback()` empties the basket. Reading uses `select`:

`db.session.scalars(sa.select(PsStroke).order_by(PsStroke.created_at.desc()).limit(50)).all()`

By hand, with 3 strokes created at 10:00, 10:05 and 10:09:

1. `select(PsStroke)` becomes `SELECT ... FROM ps_strokes`: 3 rows.
2. `order_by(created_at.desc())` sorts newest first: 10:09, 10:05, 10:00.
3. `limit(50)` keeps at most 50: still 3.
4. `.scalars().all()` turns each row into a `PsStroke` object in a Python list. The `/feed` template loops over that list.

### Why migrations exist

The database file has a fixed shape. Adding `class Frame` to Python does not change `app.db`. A migration closes the gap:

1. `flask db migrate` compares your classes with the database and writes a script with an `upgrade()` and a `downgrade()` function.
2. `flask db upgrade` runs the scripts not yet applied.
3. The database remembers the last applied script in a one-row table called `alembic_version`.

By hand, with three scripts A (users, posts), B (ps\_strokes), C (frames): a new database has no `alembic_version`. After `upgrade` it holds `C`, and the tables `user`, `post`, `ps_strokes`, `frames` exist. `downgrade` undoes C: `frames` disappears, version is `B`.

Rules: read each generated script before you upgrade, because autogenerate can miss renames (it sees a drop plus an add and would lose data). Never edit a script that others already applied; add a new one. SQLite cannot alter some things in place, so Flask-Migrate may need batch mode. While you are the only user, deleting `app.db` and `migrations/` and starting over is fine.

### Uniqueness and safe retries

The panel retries failed uploads, so the same frame can arrive twice. `Frame.sha256` is `unique`, and the endpoint looks the hash up first to answer `duplicate: true`. A known gap: two identical uploads arriving at the same instant could both pass the lookup, and the second `commit` would raise `IntegrityError`. Catching that and returning the existing row is a roadmap exercise.

### Files on disk, rows in the database

JPEGs live in `instance/frames/`; the table stores the filename and the metadata. Databases handle large binary files badly and backups get heavy. The cost of this split: a file and its row can drift apart (a deleted file leaves a dead row).

## Photoshop side concepts

No single Photoshop plugin type can both export pixels and read the active layer, so the project uses two and joins them through a folder.

### Why two plugins

- **Generator** is a Node.js program Photoshop starts in the background. It receives events (`imageChanged`) and can export the canvas (`getDocumentPixmap`, `savePixmap`). It has no window and no easy way to ask about the foreground colour.
- **CEP panel** is an HTML page inside Photoshop, with Node.js switched on (`--enable-nodejs`). It has a window and can run ExtendScript, Photoshop's own scripting language, which can read the active layer and foreground colour. It does not receive an event that says "pixels changed".
- The folder (`outputFolder`) is the handoff: Generator writes JPEGs into it, the panel watches it.

### Debounce, by hand

Photoshop fires `imageChanged` many times during one brush stroke. Saving a JPEG for each would flood the disk. A debounce waits for quiet: every event restarts a 500 ms timer, and only a timer that runs out does the work. Events at 0, 100, 300 and 350 ms:

1. t=0: event. Timer set to fire at 500.
2. t=100: event. Old timer cancelled, new one set to fire at 600.
3. t=300: event. Cancelled, new one for 800.
4. t=350: event. Cancelled, new one for 850.
5. No more events. t=850: timer fires, one JPEG is saved.

Four events, one capture. The weakness: a stroke that never pauses for 500 ms produces no capture until it ends. The fix is a maximum wait (capture at least every N seconds); it is a roadmap exercise.

### Safe file handoff

The panel must never read a half-written JPEG. Generator writes `frame_1700000000000_doc3.jpg.part` and, only when the write has finished, renames it to `.jpg`. A rename inside one folder is instant, so the panel sees either no `.jpg` or a complete one. The panel ignores every name that does not match `frame_<digits>_doc<digits>.jpg`.

### ExtendScript and the metadata

ExtendScript is a 1990s-era JavaScript (ES3): no `JSON` object, no `let`, no arrow functions. So `hostscript.jsx` builds the JSON text by hand and escapes quotes, backslashes and control characters in layer names. The panel calls it with `evalScript("getFrameMeta()", callback)`; the result always arrives as a string, and a failure arrives as the text `EvalScript error.`.

The metadata is read when the panel processes the file, not when the pixels were captured. If you switch layer in between, the JSON describes the new layer. For a proof of concept that is acceptable; the clean fix is to have Generator read the metadata itself at capture time.

### How a file is POSTed

A `multipart/form-data` body carries several named parts, each with its own headers, separated by a random boundary string. `uploader.js` builds one with a `frame` part (`image/jpeg`) and a `meta` part (`application/json`). Flask's `request.files["frame"]` and `request.files["meta"]` read them back. Failed uploads retry with growing waits (0.5 s, 1 s, 2 s); a 4xx answer is not retried, because the same request would fail again.

### Debugging in Photoshop

- The panel prints its own status line. `watching` is healthy.
- To open the panel's developer tools, add a `.debug` file to the extension folder (see the CEP cookbook) and browse to the port it names.
- Generator logs go to Photoshop's Generator log; each line from this plugin starts with `frame-recorder:`.
- A frame that fails to upload stays in `outputFolder`. Fix the cause and press Apply: the panel rescans.

## Roadmap to a proof of concept

Freeze the scope at "frames plus metadata, a timelapse, and a stats feed", and work through the phases in order. Each phase ends with a check you can run; do not start the next one before it passes.

**Scope rule.** This project has changed shape several times in a few days: strokes from `.atn` files, Maya, live recording, then frames. Each pivot left unfinished code behind, and the zip shows the cost: a file overwritten with another file's content. You are still learning how Flask is organised. A pivot now teaches you less than finishing one phase. Write new ideas in a `IDEAS.md` file and keep going; revisit it after phase 4.

### Phase 0: green and under version control

Concepts: a virtual environment isolates this project's packages; Git records every state so a damaged file can be restored; `.gitignore` lists what must not be recorded.

- Apply the fix list above until `/feed` and `/api/frames` work.
- `git init`, write a `.gitignore` for `.venv/`, `app.db`, `instance/`, `__pycache__/`, `.pytest_cache/`, `migrations/` stays tracked. Commit. Push to GitHub.
- Hint: after a commit, `git diff` shows exactly what you changed since. Run it before every commit.

Done when: a fresh clone plus the README steps gives a running app.

### Phase 1: change the app yourself

Concepts: query parameters (`request.args`), serving files (`send_from_directory`), `IntegrityError`.

1. A `/frames` page: newest first, each row a thumbnail, layer name, colour swatch and capture time. The thumbnail needs a second route that returns the JPEG by filename. Hint: validate the filename against the same pattern `frames_api.py` uses before touching the disk, otherwise `../` paths escape the folder.
2. `GET /api/frames?limit=20&offset=0` returning JSON. Concept: pagination. Hint: cap `limit` at a maximum, otherwise one request can ask for a million rows.
3. Close the race described under Database concepts. Hint: wrap `commit()` in `try/except IntegrityError`, `rollback()`, re-select the row by hash and return it as a duplicate.

Done when: uploading the same file with `curl.exe` twice shows one thumbnail, and `/api/frames?limit=1` returns one item.

### Phase 2: model sessions and users

Concepts: foreign keys and `relationship`; a session is a run of frames belonging together; hashing secrets.

1. A `RecordingSession` table (id, user, started\_at, document name) and `Frame.session_id`. Decide how a session begins. Simplest: the server starts a new session when the gap since the previous frame of the same document exceeds 30 minutes. Hint: you saw this idea earlier as "gaps and islands"; `lag()` in SQL, or a loop over rows sorted by `captured_at_ms` in Python for a first version.
2. Give each user an API token. Store only its hash. Hint: `secrets.token_urlsafe()` makes the token, `hashlib.sha256` hashes it, and the endpoint hashes the incoming `X-Api-Token` and compares. The panel already sends that header.
3. Browser login with Flask-Login using the `LoginForm` you already have. Hint: Mega-Tutorial chapter 5 does exactly this.

Done when: two users upload frames and each sees only their own on `/frames`.

### Phase 3: the timelapse

Concepts: ffmpeg turns a list of images into video; long work must leave the web request (a request that takes 30 s times out and blocks a worker); a job has a status.

1. A terminal command first: `flask build-timelapse SESSION_ID` that writes an MP4. Hint: sort the session's frames by `captured_at_ms`, write a text list for ffmpeg's `concat` input, set a frame rate. If the canvas size changed mid-session ffmpeg needs every frame scaled to one size.
2. Compress idle time. Real timestamps would make a 3-hour session a 3-hour video. Hint: use the gaps between frames, cap each at 2 s before computing durations.
3. A `TimelapseJob` table (session, status: queued/running/done/failed, output path) and a `POST` endpoint that creates a job. Run the job in a background worker (RQ is the lightest option; see Reading list). Hint: the endpoint returns 202 and a job id; the client polls a `GET` for the status.

Done when: one command and one HTTP call each produce a playable MP4 from the same session.

### Phase 4: stats and the feed

Concepts: SQL aggregation (`GROUP BY`, `COUNT`, `SUM`), window functions, ranking (`RANK` versus `DENSE_RANK`), caching a computed value.

1. Per-session stats: frame count, active minutes (sum of gaps shorter than 2 minutes), distinct layers, distinct colours.
2. A leaderboard page ranking users by active minutes this week. Hint: compute in one query with `GROUP BY user_id` and a date filter first; only cache if it is slow.
3. A feed of recent sessions with a thumbnail from the middle frame and a link to the timelapse.

Decision gate: now choose whether the stroke-geometry work (`PsStroke`, `.atn` import) stays as a side demo or moves to a `legacy/` folder. Frames alone already support the whole product.

Done when: the leaderboard and feed show real numbers from your own Photoshop sessions.

### Phase 5: structure and tests

Concepts: an application factory (`create_app()` builds an app on demand, so tests can build a fresh one); blueprints group routes; fixtures give each test a clean database.

1. Convert `app/__init__.py` to a factory and move routes into two blueprints, `web` and `api`.
2. Write pytest tests for the upload endpoint with the Flask test client and an in-memory SQLite database: valid upload, duplicate, non-JPEG, bad JSON, wrong token, oversize.
3. Add a GitHub Actions workflow that runs the tests on every push.

Done when: `pytest` is green from a fresh clone and the CI badge shows it.

### Phase 6: portfolio polish

- Swap SQLite for PostgreSQL through `DATABASE_URL` (one line of config, plus reading why SQLite cannot alter some columns).
- Run under `gunicorn` in a Docker image; put the token and secret key in environment variables.
- README with a screen recording of drawing in Photoshop and the timelapse appearing, the architecture diagram from this document, and the setup steps.
- Rate-limit and size-limit the upload endpoint; return clear errors.

How to work through all of it: one phase per week at most, one commit per working change, and read a Python traceback from the bottom up: the last line says what went wrong, the lines above say where.

## Reading list and links

Pages I opened on 2026-11-12 to confirm they exist and cover what is described are marked **opened**. The last group I could not open from here; the addresses are the standard ones, so check them yourself.

### Flask

- [The Flask Mega-Tutorial, Part I](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) (opened). Your microblog came from this; re-read the chapters on templates, databases, migrations and logins now that you have a second app to compare.
- [Flask Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/). Routes, requests, responses, in about an hour.
- [Flask tutorial (Flaskr)](https://flask.palletsprojects.com/en/stable/tutorial/). Builds an app with a factory, blueprints and tests: the shape of roadmap phase 5.
- [Application factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) (opened). Why `create_app()` exists.
- [Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/) (opened). Splitting `routes.py` into `web` and `api`.
- [Uploading files](https://flask.palletsprojects.com/en/stable/patterns/fileuploads/) (opened). `request.files`, `secure_filename`, `MAX_CONTENT_LENGTH`.
- [Testing Flask applications](https://flask.palletsprojects.com/en/stable/testing/) (opened). Test client, fixtures, CLI runner.

### Database

- [SQLAlchemy 2.0 Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html) (opened). The reference for `select`, sessions, relationships. Read the ORM parts in order.
- [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/). How `db.Model` and `db.session` attach to the app.
- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) (opened). What migration scripts contain.
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) (opened). The `flask db` commands.

### Web and architecture concepts

- [Overview of HTTP, MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) (opened). Requests, responses, methods, status codes.
- [Event Sourcing, Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html) (opened). The idea behind your frame log: record what happened, derive state from it.
- *Designing Data-Intensive Applications*, Martin Kleppmann (book). Chapters on data models, storage and batch processing; read selectively after phase 4.

### Photoshop and tools (not opened from here)

- [Adobe CEP-Resources](https://github.com/Adobe-CEP/CEP-Resources). Download `CSInterface.js` here; the CEP cookbook is in the same repository.
- [generator-core](https://github.com/adobe-photoshop/generator-core). Source of the Generator API this plugin uses.
- [UXP for Photoshop](https://developer.adobe.com/photoshop/uxp/). Adobe's current plugin platform; CEP is the older one. Read it before deciding whether to port.
- [pytest](https://docs.pytest.org/en/stable/), [RQ](https://python-rq.org/) (background jobs), [ffmpeg](https://ffmpeg.org/ffmpeg.html) (video), [Python venv](https://docs.python.org/3/library/venv.html), [Pro Git book](https://git-scm.com/book/en/v2).
