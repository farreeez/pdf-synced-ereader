"""Service layer package.

Each module here focuses on one *domain capability* (e.g. audio operations,
transcription, syncing). Flask blueprints call into these pure functions so
business logic stays decoupled from HTTP + request/response objects.

Guidelines:
- Keep functions deterministic where possible.
- Avoid using `flask.current_app` inside services; pass config values in.
- Make it easy to unit test these functions without needing an app context.
"""

from .projects import create_project, list_projects
from .transcription import transcribe_audio
from .alignment import coarsely_align_book_transcription, retreive_json_data, persist_alignment_data, check_if_alignment_data_exists, get_existing_alignment_data

__all__ = ["create_project", "list_projects", "transcribe_audio", "coarsely_align_book_transcription", "retreive_json_data", "persist_alignment_data", "check_if_alignment_data_exists", "get_existing_alignment_data"]
