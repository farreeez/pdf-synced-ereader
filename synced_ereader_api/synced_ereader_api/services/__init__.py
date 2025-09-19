"""Service layer package.

Each module here focuses on one *domain capability* (e.g. audio operations,
transcription, syncing). Flask blueprints call into these pure functions so
business logic stays decoupled from HTTP + request/response objects.

Guidelines:
- Keep functions deterministic where possible.
- Avoid using `flask.current_app` inside services; pass config values in.
- Make it easy to unit test these functions without needing an app context.
"""

# from .alignment import load_audio_metadata

# __all__ = [
# ]
