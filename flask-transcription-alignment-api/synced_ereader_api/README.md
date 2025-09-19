# synced_ereader_api

synced_ereader_api description

## Quick Start

Run the application (Windows focused Makefile):

```
make venv   # first time only (or after dependency changes)
make run
```

Then open: [http://localhost:5000/](http://localhost:5000/)

## Prerequisites

Python >=3.11

## Development environment

- `make venv`: creates a virtualenv in `venv/` with dependencies and this
  application installed in editable (development) mode

- `make run`: runs a development server in debug mode (changes in source code
  are reloaded automatically)

- `make format`: reformats code

- `make lint`: runs flake8

- `make mypy`: runs type checks by mypy

- `make test`: runs tests (see also: [Testing Flask Applications](https://flask.palletsprojects.com/en/3.0.x/testing/))

- `make dist`: creates a wheel distribution (will run tests first)

- `make clean`: removes virtualenv and build artifacts

- add application dependencies in `pyproject.toml` under `project.dependencies`;
  add development dependencies under `project.optional-dependencies.*`; run
  `make clean && make venv` to reinstall the environment.

### Manual installation (alternative to Makefile)

PowerShell:

```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
python -m pip install --upgrade pip
pip install -e .
pip install -e ."[dev]"
```

If a platform requires `requirements.txt`, it mirrors the runtime dependencies in `pyproject.toml`.

### Upgrading from Python 3.10

If you previously created a virtual environment with Python 3.10:

1. Deactivate it (if active):

- PowerShell: `deactivate` (if using the built-in deactivate script)

2. Remove the old environment directory (`venv` or `.venv`).
3. Ensure Python 3.11 is on your PATH: `python --version` should report 3.11.x.
4. Recreate the environment (or simply run `make venv`):

make clean
make venv

or manually:

```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
pip install --upgrade pip
pip install -e .
pip install -e ."[dev]"
```

5. Run tests to confirm everything still passes: `pytest -q`.

## Configuration

Default configuration is loaded from `synced_ereader_api.defaults` and can be
overriden by environment variables with a `FLASK_` prefix. See
[Configuring from Environment Variables](https://flask.palletsprojects.com/en/3.0.x/config/#configuring-from-environment-variables).

Consider using
[dotenv](https://flask.palletsprojects.com/en/3.0.x/cli/#environment-variables-from-dotenv).

## Deployment

See [Deploying to Production](https://flask.palletsprojects.com/en/3.0.x/deploying/).

You may use the distribution (`make dist`) to publish it to a package index,
deliver to your server, or copy in your `Dockerfile`, and insall it with `pip`.

You must set a
[SECRET_KEY](https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/#configure-the-secret-key)
in production to a secret and stable value.

## Project Structure (Blueprint + Service Example)

The codebase now demonstrates a common pattern: keep HTTP layer (blueprints)
thin and push logic into a service layer. This makes unit testing easier and
keeps responsibilities clear.

```
synced_ereader_api/
  __init__.py                # app factory registers blueprints
  logging.py                 # logging configuration
  defaults.py                # base config values
  views.py                   # (legacy example, now deprecated)
  blueprints/
    api/
      routes.py              # JSON endpoints under /api
    site/
      routes.py              # HTML pages (index, etc.)
    __init__.py              # exports api_bp, site_bp
  services/
    transcription.py         # dummy transcription logic (future: whisper)
    audio.py                 # audio metadata helpers
    __init__.py
  templates/
    index.html
  static/
    styles.css
```

### Blueprints
- `site_bp` serves the landing page at `/`.
- `api_bp` serves JSON endpoints such as:
  - `GET /api/health` – simple health probe
  - `POST /api/transcribe` – returns a dummy transcription + metadata

### Services
Pure Python functions with no Flask context usage:
`services.transcription.transcribe_dummy(audio_path)` returns a fake model
payload; later you can replace the body with real whisper calls.

Keep services:
- Stateless where possible
- Accept plain arguments / return plain dicts or dataclasses
- Handle errors and raise domain exceptions (you can map these to HTTP codes
  inside blueprints)

### Adding a New Feature (Example)
Suppose you want an endpoint to list available audio files:
1. Add a function in `services/audio.py`:
   ```python
   def list_audio_files(directory: str) -> list[str]:
       return [p.name for p in Path(directory).glob('*.wav')]
   ```
2. Import and expose it in `services/__init__.py` if desired.
3. Add a route in `blueprints/api/routes.py`:
   ```python
   from ...services import list_audio_files

   @api_bp.get('/audio')
   def list_audio():
       files = list_audio_files('media')
       return jsonify({'files': files})
   ```

### Testing
`tests/test_api.py` shows how to call the new API blueprint. For service-only
tests, you can import functions directly—no need to create a Flask app.

### Migrating Away From `views.py`
`views.py` is left only as a reference. New code should live under
`blueprints/` + `services/`. After you are comfortable you can delete
`views.py` entirely.

Feel free to ask for more scaffolding (DB integration, background tasks, auth,
etc.) when you need it.
