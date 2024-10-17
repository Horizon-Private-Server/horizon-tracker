# Horizon Tracker Backend

This repository is for the backend for the Horizon Private Server's tracker for Retched and Clank: Up Your Arsenal and Ratchet: Deadlocked.
This backend is designed as a proxy for the production Horizon database and middleware.
This interface is designed to ingest player data and store it in a more usable format for improved data analytics.

This backend serves as an API to drive the following game features.

### Ratchet and Clank: Up Your Arsenal

1. Stats
   1. Leaderboards
   2. Player cards
   3. Account Aggregations (account merging)
2. In-Game Real-Time Updates (Based on the UYA Tracker by Nick1)

### Ratchet Deadlocked

1. Stats
   1. Leaderboards
   2. Custom Leaderboards
   3. Player Cards + Survival Player Cards
2. Games
   1. Game History
3. Tracker (TBD)

## Structure

1. `app/` - Root folder for the horizon tracker application.
   1. `models/` - SQLAlchemy ORM model files.
   2. `routers/` - API Create, Read, Update, Delete (CRUD) routes.
   3. `schemas/` - SQLAlchemy ORM schema files.
2. `horizon/` - Horizon utility code module. General module that may be converted into a PyPI module in the future.
   1. `parsing/` - Collection of utilities for processing data from the Horizon production servers. This is separate from `utils/` as a place to incorporate existing code.
   2. `rank/` - Utilities for computing rank in UYA and DL.

## Setup

The following guide assumes that you are familiar with general programming concepts as well as general Python programming.
We strongly recommend that you use the [JetBrains PyCharm IDE](https://www.jetbrains.com/pycharm/download/?section=windows) as your editor and environment manager.
PyCharm will make the setup process vastly simpler and will lead to fewer setup headaches.
If you choose to use a different IDE (e.g., VS Code with the Python extension), the setup process will follow the same general setup strategy, but the steps will look very different.
This setup guide will be written from the context of using PyCharm.
The backend will work on both Windows and Linux systems, the main OS differences will be installing dependencies and setting up the virtual environment.
The guide will primarily focus on Windows setup, but Linux setup should be fairly straightforward assuming you are using a common distro.

### Clone this Repository

If you haven't already, clone this repository to your local system.
We recommend always using SSH cloning instead of HTTPS cloning, if you are new to using SSH keys, GitHub provides detailed [documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) on how to setup SSH Keys and ssh-agents.

If you haven't already, you will also need to install [Git](https://git-scm.com/).

> If you are not familiar with Git, including common Git practices and workflows, we encourage you to gain familiarity before contributing code.
> The `main` branch of this the `horizon-tracker` application is push protected, meaning you will be unable to commit and push to `main` directly.
> All code contributions will go through a Pull Request with repository maintainers attached.

### Python Installation and Project Setup

The backend is written in Python and will require a local Python interpreter to work.
We recommend downloading and installing the latest LTS version of [Python](https://www.python.org/downloads/).
> Minimum require Python version is 3.12.

Once installed verify that Python is working by running the Terminal/PowerShell command `python --version`.
> Note: For Windows users, you may need to restart Windows Explorer or perform a system reboot if the Python installer does not update your environment variables.
> This is unlikely on any Windows 10+ systems.

> For systems where multiple versions of Python are present, you will need to configure the correct version within your IDE or through the `virtualenv` command.
> Managing multiple environments is beyond the scope of this setup guide, if you have multiple environments, we'll assume you know what you're doing!

### PyCharm Installation (Recommended)

The next step is to set up your IDE.
This guide will focus on PyCharm as it is a fully featured Python IDE that has a free community edition and robust support for managing Python virtual environments.

Download PyCharm from the JetBrains Website and install it.
Debian-based Linux systems can install PyCharm using snap (`snap install --classic pycharm-ce`).

Once installed, run PyCharm and navigate through the welcome screens.
These will include items such as IDE theme (dark mode/light mode) as well as settings to import from other IDEs.
Select your preferred settings on these screens.

_The remaining PyCharm project setup will be continued below._

### Postgres Setup

The Horizon Tracker application uses a Postgres as its database.
Postgres was chosen for its performance and rich feature-set among relational databases.
It is possible to use SQLite or another common relational database, but we strongly encourage you to use Postgres to minimize the differences between your development environment and the production environment.

Download and install the latest [LTS Postgres Version](https://www.postgresql.org/download/) for your operating system of choice.
Linux users can install postgres through their distro's package manager (e.g., `sudo apt install postgresql`).

During the installation process for both Windows and Linux, the installer will ask you to set a default password.
We STRONGLY recommend you make this password simple (e.g., `123` or `password` or something similar).
This database will store no sensitive data and it's always a pain to reset the master password on a DB instance.

Once installed, make sure the Postgres service is running by making a test connection to it.
On Windows you can go to `C:\Program Files\PostgreSQL\16\scripts` and launch `runpsql.bat`, this will open a command prompt and allow you to enter in the following config information.
```bash
Server [localhost]: # default is correct, hit enter
Database [postgres]: # default is correct, hit enter
Port [5432]: # default is correct, hit enter
Username [postgres]: # default is correct, hit enter
Password for user postgres: # enter the master password you set here.
```

You can perform the same test on Linux by running the `psql` command ([documentation](https://www.postgresql.org/docs/current/app-psql.html)).

### Redis Setup

TBD Redis might be required as a WebSocket application broker.
Need to investigate Starlette a bit more first.

### Pycharm Project Setup

With all of the dependencies installed, you can finish importing the project into your IDE.

#### Import Project
Within PyCharm, select `File` < `Open`, then select the cloned `horizon-tracker` folder. Ensure that both the `app` folder and `horizon` folder are at the root of the selected folder.

#### Create Python Virtual Environment

Once the project is opened, you will need to create a Python Virtual Environment.

In PyCharm, navigate to `File` < `Settings` < `Project:horizon-tracker` < `Project Interpreter`.
This menu will allow you to select your Python base environment and install dependencies.

1. At the very top should be a lookup bar with a settings button to the right. This field should initially be empty.
2. Click on the settings button and select the `Add...` option to bring up a list of base interpreters.
3. Under the `New Environment` section, select the `Browse` button (button with the folder icon).
4. Navigate to your Python Base interpreter. In Windows this is typically `C:\Users\<YourUser>\AppData\Local\Programs\Python\Python<XYY>\python.exe`. In Linux this is typically `/usr/bin/python`.
5. Select your base interpreter `python.exe`/`python` and then select `Ok`. PyCharm will then create a new virtual environment for you.

> The __manual alternative__ to this process is to use the `virtualenv` (or `python -m venv`) command ([documentation](https://docs.python.org/3/library/venv.html)).
> Once the virtual environment is created, you will need to manually activate this virtual environment using the `source` command (i.e., `source venv/bin/activate`) on Linux or activation batch file on Windows (`venv\Scripts\activate.bat`).
> You will know an environment is activated because the token `(venv)` will appear at the front of your command prompt window.
> If you are doing this manually, you will need to make sure you have this environment active when installing dependencies and running any of the code.

#### Install Module Dependencies

Once your virtual environment is create, you can install all of the project dependencies.
In PyCharm open up the file `requirements.txt`.
Once open there will be a warning banner asking you to install missing dependencies.
Select the install option and wait for everything to install.

> The __manual alternative__ to this process is to activate your virtual environment then run the pip install manually (`python -m pip install -r requirements.txt`).

> The running philosophy behind package management for the Horizon Tracker is that dependencies should be kept as up-to-date as possible.
> It is a common practice to install from a `pip freeze` output to ensure consistency among developers.
> In our case, the Horizon priority is on importing updated code to receive security fixes and features.
> This also has the advantage of keeping the requirements file very simple and clean.
> It is up to individual contributors to ensure that they keep dependencies up-to-date.
> The only dependencies that will be held back are core dependencies through major versions which may have breaking changes (e.g., fast-api:0.x.x -> fastapi:1.x.x).
> If these limitations exist, they will be reflected in updated versions of the requirements file.

#### Configure Variables and Credentials

The development backend attempts to mimic the behavior of the production server as closely as possible.
This means that the development backend uses an environment file to determine credentials and data source paths.

> Note: You will need to get credentials from the Horizon middleware maintainers.

Create a file called `env.json` in the root directory of the `horizon-tracker` folder.
and paste in the following contents.
```json
{
  "region": "us-east-1",
  "environment": "tracker/credentials/dev",
  "database_host": "localhost",
  "database_port": 5432,
  "database_name": "horizon_tracker",
  "database_username": "postgres",
  "database_password": "123",
  "horizon_middleware_protocol": "https",
  "horizon_middleware_host": <horizon_middleware_host>,
  "horizon_middleware_username": <your_horizon_middleware_username>,
  "horizon_middleware_password": <your_horizon_middleware_password>,
  "dl": {
    "horizon_middleware_protocol": "https",
    "horizon_middleware_host": <horizon_middleware_host>,
    "horizon_middleware_username": <your_horizon_middleware_username>,
    "horizon_middleware_password": <your_horizon_middleware_password>,
    "horizon_app_id": 11184
  },
  "uya": {
    "horizon_middleware_protocol": "https",
    "horizon_middleware_host": <horizon_middleware_host>,
    "horizon_middleware_username": <your_horizon_middleware_username>,
    "horizon_middleware_password": <your_horizon_middleware_password>,
    "horizon_app_id": 10684
  }
}
```

> __WARNING:__ Please do not commit your env.json file to the repository under ANY circumstances.
> This could compromise security aspects of the Horizon Production Middleware.
> The file is flagged as part of the `.gitignore`, so this should not be a problem, BUT, if you don't have your Git repo configured correctly, it might not be reading the `.gitignore` correctly.
> Please be careful with this file.

> Note: The production server does not store any credentials on-machine, this is only a convenience used for local development.
> Instead, the environment will reach out to the appropriate AWS Secrets Manager repository for the appropriate credentials.
> The production environment will will have a single entry `environment`.
> The application will check to see if the name `environment` ends with `dev`. If so, it will scan the same JSON file for the remaining fields, otherwise, it will reach out to AWS.

### Run Development Application

To launch the application, open a terminal window in IDE or in browser.
Ensure that the virtual environment is activated (this should be activated by default if in an IDE).
Run the command `fastapi dev app/main.py`

> When in development mode, any time a file is modified (saved), the development server will reload (killing any active connections, including WebSocket connections).

### Style Guide Recommendation

When contributing to this repository, it is important to keep a consistent style to maintain code readability.
Here are a few points to help keep this repository easily readable.

1. Format appropriately and listen to your linter. There's no excuse for poorly formatted code with auto-formatters readily available.
2. __Please don't hang your line endings.__
   1. This is a super common autoformat variant and is absolutely horrible to read. For example.
   
   ```python
      a: int = compute_a_number_from_this_super_long_function_name(
                                                                    variable_1, variable_2,
                                                                    variable_3, variable_4
                                                                  )
   ```
   
   2. Properly wrap them instead

   ```python
      a: int = compute_a_number_from_this_super_long_function_name(
          variable_1, variable_2, variable_3, variable_4
      )
   ```

   3. Most IDEs feature wrap settings, this is an adjustable setting.   

3. Please make liberal use of [Type Hints](https://docs.python.org/3/library/typing.html).
   1. Type hints help detect errors before they happen.
   2. FastAPI is specifically built to leverage type hints.
   3. More specificity is usually better than less specificity.
   4. Avoid using primitive or collection types from the `typing` module.
      1. (i.e., `my_list: list[str] = list()` instead of `my_list: List[str] = list()`).
4. Please minimize the use of complex list comprehensions and dictionary comprehensions.
   1. One-liners are great, but if you need to stick a debug breakpoint in the middle, consider making it a traditional loop instead.
5. Please write docstrings for your functions and for your API views.
   1. FastAPI uses docstrings to generate OpenAPI/Swagger documentation.
   2. Docstrings really help expedite development and force you to write better code.
   3. When writing DocStrings, the preferred format is the `reStructuredText` format ([documentation](http://daouzli.com/blog/docstring.html)).
   4. Please use triple, double-quotes for DocStrings.
6. Strings
   1. Please denote strings with double-quotes instead of single quotes. 
   2. Please use f-strings instead of `string.format()`.
   3. `pathlib` is preferable to string paths when working with file I/O or networking.

### Generating Database Migrations with Alembic
Run:
```
alembic revision --autogenerate
```
That will make a file under alembic/versions, in that file is the revision ID on line 3, that ID is a hash of the revision which is used to track versioning.

If you get an error running this, you need to upgrade:
```
alembic upgrade head
```

Run
```
alembic upgrade <revision_id>
```

### Migrating the Database Version

TBD


### Docker Compose
Docker setup

First set up your `env.json` file with the correct setup.


Initialization:
1. Install Docker
2. Edit the environment variables on your machine to add the following:
```
SOCKET_IP=PRODUCTION_UYA_SERVER_IP
TRACKER_POSTGRES_USER=YOURPOSTGRES_USER_IN_ENVJSON
TRACKER_POSTGRES_PASSWORD=YOURPOSTGRES_PW_IN_ENVJSON
TRACKER_POSTGRES_DB=YOURPOSTGRES_DB_IN_ENVJSON
```
3. Run:
```
docker compose up --build 
```

Fill up db with data (you may need to pip install some things, and may need to install postgres driver locally). Run these commands on a local python terminal (not docker):
1. Pull stats from production to local
```
python -m scripts.pull_stats
```
2. Ingest the downloaded JSON files into the db:
```
python -m scripts.dataloader
```

If you want to test the live websocket:
```
cd scripts
python test_websocket.py
```