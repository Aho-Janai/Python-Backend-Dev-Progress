> [!quote] YOU

> [!note] SKILL loaded: teach


> [!question] Question
> What topic or concept would you like to understand today? Feel free to be as specific or broad as you like.
>
> Your answer will help me tailor the teaching process to your goal.


> [!example] Answer
> I need to learn python backend development


> [!question] Quiz
> What will be the output of the following Python code?
> ```python
> x = [1, 2, 3]
> print(x[1])
> ```
>
> 1. 1
> 2. 2
> 3. 3
> 4. Error


> [!success] Quiz — correct ✓
> Your answer: 2. 2
> Correct answer: 2
>
> Python lists are zero-indexed, so x[1] refers to the second element, which is 2.


> [!question] Quiz
> What will be the output of this Python code?
> ```python
> def add(a, b):
>     return a + b
> print(add(2, 4))
> ```
>
> 1. 6
> 2. 8
> 3. 4
> 4. Error


> [!success] Quiz — correct ✓
> Your answer: 1. 6
> Correct answer: 1
>
> The function `add` returns the sum of its two arguments. Calling `add(2,4)` returns 6.


> [!question] Quiz
> What does the following code produce?
> ```python
> result = [x*2 for x in range(5)]
> print(result)
> ```
>
> 1. [0, 2, 4, 6, 8]
> 2. [1, 2, 3, 4, 5]
> 3. [2, 4, 6, 8, 10]
> 4. Error


> [!warning] Quiz — unavailable
> quiz correctAnswer "0" does not match any option value ("[0, 2, 4, 6, 8]", "[1, 2, 3, 4, 5]", "[2, 4, 6, 8, 10]", "Error")


> [!question] Quiz
> What does the following code produce?
> ```python
> result = [x*2 for x in range(5)]
> print(result)
> ```
>
> 1. [0, 2, 4, 6, 8]
> 2. [1, 2, 3, 4, 5]
> 3. [2, 4, 6, 8, 10]
> 4. Error


> [!warning] Quiz — unavailable
> quiz correctAnswer "0" does not match any option value ("[0, 2, 4, 6, 8]", "[1, 2, 3, 4, 5]", "[2, 4, 6, 8, 10]", "Error")


> [!question] Quiz
> How many elements are in the list created by this code?
> ```python
> result = [x*2 for x in range(5)]
> print(len(result))
> ```
>
> 1. 5
> 2. 4
> 3. 6
> 4. Error


> [!failure] Quiz — incorrect ✗
> Your answer: 4. Error
> Correct answer: 1
>
> `range(5)` yields 0,1,2,3,4, so the list comprehension creates five elements; `len(result)` is 5.


> [!question] Quiz
> What sequence does `range(5)` produce in Python?
>
> 1. 0, 1, 2, 3, 4
> 2. 1, 2, 3, 4, 5
> 3. 0, 1, 2, 3, 4, 5
> 4. Error


> [!success] Quiz — correct ✓
> Your answer: 1. 0, 1, 2, 3, 4
> Correct answer: 1
>
> `range(5)` yields a sequence starting at 0 up to (but not including) 5: 0,1,2,3,4.


> [!question] Quiz
> Does the statement `import math` make the function `math.sqrt` available for use?
>
> 1. Yes
> 2. No
> 3. Only for built‑in types
> 4. Error


> [!success] Quiz — correct ✓
> Your answer: 1. Yes
> Correct answer: 1
>
> `import math` imports the standard library module `math`, making its functions available via the `math.` prefix.


> [!question] Quiz
> Which command installs the `virtualenv` package using pip?
>
> 1. pip install virtualenv
> 2. virtualenv create
> 3. python -m venv
> 4. conda create


> [!success] Quiz — correct ✓
> Your answer: 1. pip install virtualenv
> Correct answer: 1
>
> `pip install virtualenv` installs the `virtualenv` package, which can then be used to create isolated environments via the `virtualenv env_name` command.


> [!question] Quiz
> What response body will Flask send for this code?
> ```python
> from flask import Flask
> app = Flask(__name__)
>
> @app.route('/')
> def hello():
>     return "Hello, World!"
> ```
>
> 1. Hello, World!
> 2. /
> 3. Error
> 4. Nothing


> [!success] Quiz — correct ✓
> Your answer: 1. Hello, World!
> Correct answer: 1
>
> The route `@app.route('/')` matches the root URL and returns the string `'Hello, World!'`, which Flask sends as the HTTP response body.


> [!question] Quiz
> When using Flask, what Python type does `request.get_json()` return after receiving a JSON payload?
>
> 1. dict
> 2. list
> 3. str
> 4. None


> [!success] Quiz — correct ✓
> Your answer: 1. dict
> Correct answer: 1
>
> `request.get_json()` parses the JSON payload and returns a Python dictionary representing the data.


> [!question] Quiz
> Given this SQLAlchemy model, what is the Python class name representing the table?
> ```python
> class User(db.Model):
>     id = db.Column(db.Integer, primary_key=True)
>     name = db.Column(db.String(80))
> ```
>
> 1. User
> 2. users
> 3. user_table
> 4. None


> [!success] Quiz — correct ✓
> Your answer: 1. User
> Correct answer: 1
>
> In the model definition, the class name `User` becomes the table name (by default lowercased) and defines its schema.


> [!question] Quiz
> Flask applications are based on which Python web server interface?
>
> 1. WSGI
> 2. ASGI
> 3. CGI
> 4. RPC


> [!question] Quiz — I don't know
> Your answer: I don't know
> Correct answer: 1
>
> Flask is built on WSGI, a synchronous interface for Python web apps; ASGI is for async frameworks like FastAPI.


> [!abstract] PI

**Phase 2 — Plan**

Below is the teaching plan that ties together what you already know with the pieces you’re still missing. It follows the two teaching principles:

* **Unconditional truths first** – we’ll start with a few rock‑solid facts about how web servers work.
* **“How could I have discovered this?”** – each new idea will be motivated by a concrete problem you’d face when building a Python backend.

---  

### 1. What we’ll cover (in this order)

1. **Unconditional truth #1** – *All HTTP communication between a client and a server is performed via a request‑response cycle.*  
2. **Unconditional truth #2** – *A Python web framework must expose a callable that a web server can invoke for each request.*  
3. **Node A – WSGI** – What WSGI is, why Flask uses it, and how it connects truth #2 to Flask.  
4. **Node B – ASGI (the async alternative)** – How asynchronous servers differ, and when you’d choose it (e.g., FastAPI).  
5. **Node C – Deploying a Flask app with a WSGI server** – Using `gunicorn` (or `uwsgi`) in production.  
6. **Node D – Connecting to a database with SQLAlchemy** – Briefly revisiting the model you already know, now in the context of a live server.  
7. **Node E – Basic testing of routes** – Using `pytest` and Flask’s test client.  

Each node will be **motivated**, **established**, **connected** to the previous nodes, and then **checked** with a quick quiz (per the teaching loop).

---  

### 2. Dependency map (DAG)

```mermaid
graph LR
    UT1[Uncond. Truth #1: HTTP is request/response] --> UT2[Uncond. Truth #2: Framework must expose a callable]
    UT2 --> WSGI[Node A: WSGI interface]
    WSGI --> ASGI[Node B: ASGI (async) interface]
    WSGI --> Deploy[Node C: Deploying with a WSGI server]
    Deploy --> DB[Node D: DB access via SQLAlchemy]
    DB --> Test[Node E: Testing routes]
```

*The arrows show “depends on”.*  
For example, **Node C** (deployment) can only be understood once we know **Node A** (WSGI), which itself rests on the two unconditional truths.

---  

### 3. Why this ordering works for you

* You already have the **foundational Python skills** (variables, functions, modules, basic Flask routing, and SQLAlchemy models).  
* The only **missing edge** we discovered is the *WSGI* concept that powers Flask’s request handling, plus a brief look at the async alternative (**ASGI**) and how those affect deployment.  
* By cementing those unconditional truths first, every later step (deployment, testing, async alternatives) will hang securely on something you can accept *as‑is*.

---

**Please review the plan and the dependency graph.**  
If anything looks off (e.g., you’d prefer to skip the ASGI comparison or dive deeper into testing), let me know and I’ll adjust the roadmap before we start the teaching loop.  

*Just reply “OK, let’s start” or tell me what you’d like to modify.*


> [!quote] YOU

the plan is fine, just make sure not to spend to much time on WSGI and ASGI. they don't seem to relevent. let's start


> [!question] Quiz
> True or false: In HTTP, a client sends a request and receives exactly one response for that request.
>
> 1. True
> 2. False


> [!failure] Quiz — incorrect ✗
> Your answer: 2. False
> Correct answer: 1
>
> HTTP operates as a request‑response protocol: the client sends a request, the server returns a single response, then the exchange ends.


> [!abstract] PI

**Unconditional Truth #1 – The request/response nature of HTTP**

**Motivation**  
Whenever a web browser (or any HTTP client) talks to a server, the whole interaction is a *single* transaction: the client asks for something, the server replies, and then the exchange is finished. Understanding this pattern is the foundation for every backend you’ll write – it tells you why a function only runs once per request and why you never “keep a response open” unless you use special techniques.

**Establishment**  
*True*: In HTTP, a client sends **one** request and receives **exactly one** response for that request. After the response is sent, the connection either closes or moves on to the next request‑response pair.

**Connection**  
This fact will let us treat a Flask view function (the `def hello(): …` you already wrote) as the code that *produces* that single response for a single request.

**Quick check** – you already saw the quiz; the correct answer is **True**. If you thought it was false, remember that HTTP does not stream multiple responses for a single request unless you explicitly employ techniques like Server‑Sent Events, which are built on top of the basic request/response model.

---

**Unconditional Truth #2 – A web framework must expose a callable that a web server can invoke for each request**

**Motivation**  
The server (e.g., `gunicorn` or the development server Flask ships with) cannot magically know how to produce a response. It needs a **function** it can call every time a new request arrives. That function receives the request data and returns a response object.

**Establishment**  
*Every* Python web framework – Flask, Django, FastAPI, etc. – ultimately provides **one callable** (often called an *application* or *app* object) that the underlying web server calls for each incoming request.

**Connection**  
In Flask, the `app` object you created (`app = Flask(__name__)`) *is* that callable. When the WSGI server receives a request, it hands the request information to `app`, which then routes it to the appropriate view function you defined.

**Quick check**


> [!question] Quiz
> In Flask, which object is the callable that a WSGI server invokes for each incoming HTTP request?
>
> 1. app
> 2. run
> 3. request
> 4. None of the above


> [!success] Quiz — correct ✓
> Your answer: 1. app
> Correct answer: 1
>
> In Flask, the `Flask` instance (`app = Flask(__name__)`) is the callable that WSGI servers invoke for each request.


> [!question] Quiz
> What is the name of the standard Python interface that connects Flask to a production web server?
>
> 1. WSGI
> 2. ASGI
> 3. CGI
> 4. HTTP


> [!success] Quiz — correct ✓
> Your answer: 1. WSGI
> Correct answer: 1
>
> WSGI (Web Server Gateway Interface) is a simple, synchronous specification that lets a Python web framework like Flask communicate with any WSGI‑compatible server (e.g., gunicorn, uWSGI).


> [!abstract] PI

### Brief note on **ASGI** (only for context)

You asked to keep the focus on what matters for a typical Flask backend.  
**ASGI** (Asynchronous Server Gateway Interface) is the newer, async‑compatible counterpart to WSGI. It lets a framework handle many connections concurrently (e.g., FastAPI). Flask itself is built on **WSGI**, so for now we’ll stay with the synchronous model. If you later need high‑concurrency or websockets, you can switch to an ASGI‑compatible framework – but that’s a separate learning path.

---

## Node C – Deploying a Flask app with a WSGI server (e.g., **gunicorn**)

### Motivation
Your development server (`app.run(debug=True)`) is convenient for testing but not suited for production: it handles only one request at a time, lacks robust process management, and doesn’t gracefully reload code. A *WSGI server* like **gunicorn** runs multiple worker processes and talks to Flask through the callable we just identified (`app`). That gives you reliability, concurrency, and easy integration with system services (systemd, Docker, etc.).

### Establishment
1. **Install gunicorn**  
   ```bash
   pip install gunicorn
   ```
2. **Run your Flask app** with gunicorn, telling it where the callable lives (`myapp:app` means “module `myapp.py`, variable `app`”).  
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 myapp:app
   ```
   * `-w 4` – start 4 worker processes (each can handle a request).  
   * `-b 0.0.0.0:8000` – bind to port 8000 on all interfaces.  

3. **Result** – gunicorn accepts HTTP connections, translates each request into a WSGI call, invokes `app`, gets a response, and sends it back.

### Connection
This step ties together:
* **Unconditional truth #1** (request/response) – each worker handles one request at a time.  
* **Unconditional truth #2** (callable) – gunicorn calls the `app` object.  
* **Node A (WSGI)** – gunicorn implements the WSGI spec, so the hand‑off is well‑defined.

### Quick check
Let’s make sure the command line pieces are clear.


> [!question] Quiz
> In the gunicorn command `gunicorn -w 4 -b 0.0.0.0:8000 myapp:app`, what does the `-w 4` flag control?
>
> 1. -w 4
> 2. -b 0.0.0.0:8000
> 3. -k gevent
> 4. --reload


> [!failure] Quiz — incorrect ✗
> Your answer: 2. -b 0.0.0.0:8000
> Correct answer: 1
>
> `-w 4` tells gunicorn to start four worker processes, giving the app the ability to handle four requests concurrently.


> [!abstract] PI

**Why the answer matters**

`-w` *means* **workers**. Each worker is a separate Python process that can handle one request at a time. By launching several workers you get **concurrency** without changing any of your Flask code. The `-b` flag just tells gunicorn **where** to listen; it doesn’t affect how many requests can be processed in parallel.

Now that the deployment piece is clear, let’s move on.

---

## Node D – Connecting to a database with **SQLAlchemy** in a running Flask app

### Motivation
A backend rarely just returns static strings; it persists and retrieves data. You already wrote a simple `User` model. The next step is to see how that model works when the app is serving real HTTP requests.

### Establishment
1. **Configure the DB** (e.g., SQLite for simplicity) in `myapp.py`  

   ```python
   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy

   app = Flask(__name__)
   app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
   db = SQLAlchemy(app)

   class User(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(80), nullable=False)

   # Create tables (run once)
   with app.app_context():
       db.create_all()
   ```

2. **Add a route that creates a user**  

   ```python
   @app.route("/users/create/<name>")
   def create_user(name):
       u = User(name=name)
       db.session.add(u)
       db.session.commit()
       return f"User {name} created with id {u.id}"
   ```

3. **Add a route that lists users**  

   ```python
   @app.route("/users")
   def list_users():
       users = User.query.all()
       return ", ".join(f"{u.id}:{u.name}" for u in users)
   ```

When gunicorn runs the app, each request hits these routes, which in turn call the SQLAlchemy session to talk to the SQLite file. The **dependency** here is:

* **Unconditional truth #1 & #2** – request handling.  
* **Node A (WSGI)** – gunicorn passes the request to Flask.  
* **Node D** – Flask code now uses the `db` object to persist data.

### Quick check
Which line creates the actual tables in the SQLite file the first time the app starts?


> [!question] Quiz
> Which command actually creates the tables defined by SQLAlchemy models?
>
> 1. db.create_all()
> 2. User.__table__.create()
> 3. db.session.commit()
> 4. None of the above


> [!success] Quiz — correct ✓
> Your answer: 1. db.create_all()
> Correct answer: 1
>
> `db.create_all()` looks at the model definitions and creates the corresponding tables in the configured database if they don’t already exist.


> [!abstract] PI

## Node E – Testing Flask routes with the built‑in test client (and **pytest**)

### Motivation
Before you push the service to production, you want confidence that each endpoint behaves as expected—returns the right status code, creates a record, etc. Writing automated tests lets you verify that *future* changes won’t break existing behavior.

### Establishment
1. **Install pytest** (if you haven’t already)  

   ```bash
   pip install pytest
   ```

2. **Create a test file** `test_app.py` in the same directory as `myapp.py`  

   ```python
   import pytest
   from myapp import app, db, User

   @pytest.fixture
   def client():
       # Use the Flask test client, with an isolated in‑memory database
       app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
       app.config["TESTING"] = True
       with app.test_client() as client:
           with app.app_context():
               db.create_all()
           yield client

   def test_hello_route(client):
       resp = client.get("/")
       assert resp.status_code == 200
       assert resp.data == b"Hello, World!"

   def test_create_user(client):
       resp = client.get("/users/create/Alice")
       assert resp.status_code == 200
       assert b"Alice" in resp.data

       # Verify the user really exists in the DB
       with app.app_context():
           alice = User.query.filter_by(name="Alice").first()
           assert alice is not None
   ```

3. **Run the tests**  

   ```bash
   pytest -q
   ```

   You should see all tests pass (`..`), confirming that the root route and the user‑creation route work as intended.

### Connection
* The test client **simulates** an HTTP request → satisfies **Unconditional truth #1**.  
* Because the test client calls the Flask `app` object directly, it exercises the **WSGI callable** without launching an external server (a convenient shortcut for unit tests).  
* The in‑memory SQLite database shows how **Node D** (SQLAlchemy) behaves in isolation.

### Quick check
Which fixture configures Flask to use an **in‑memory** SQLite database for the tests?


> [!question] Quiz
> Which line makes the test suite use an in‑memory SQLite database?
>
> 1. app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
> 2. app.config["TESTING"] = True
> 3. db.create_all()
> 4. None of the above
