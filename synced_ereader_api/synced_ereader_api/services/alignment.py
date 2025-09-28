import json
import re
import difflib
from typing import Any, Dict, List, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer

from .shared import validate_request_data


def _validate_inputs(pages: Any, transcript_sentences: Any, transcript_start_times: Any) -> Tuple[List[str], List[str], List[float]]:
    if not isinstance(pages, list) or not all(isinstance(item, str) for item in pages):
        raise ValueError("request data provided is not a list of string.")

    if not isinstance(transcript_sentences, list) or not all(
        isinstance(s, str) for s in transcript_sentences
    ):
        print(transcript_sentences)
        raise ValueError("transcriptSentences must be a list of strings.")

    if not isinstance(transcript_start_times, list) or not all(
        isinstance(s, float) for s in transcript_start_times 
    ):
        raise ValueError("transcriptStartTimes must be a list of floats.")

    return pages, transcript_sentences, transcript_start_times


def _clean_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _word_spans(text: str) -> List[Tuple[int, int]]:
    """Return a list of (start, end) char spans for each whitespace-separated token."""
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def _normalize_for_local(s: str) -> str:
    """Lowercase and collapse whitespace for local alignment comparisons."""
    return _clean_spaces(s).lower()


def _best_local_alignment(
    sentence: str,
    chunk_text: str,
    min_window_words: Optional[int] = None,
    max_window_words: Optional[int] = None,
) -> Tuple[int, int, float]:
    """Find the best matching substring of chunk_text for sentence.

    Returns (local_start, local_end, score) where local_* are indices
    relative to the provided chunk_text. If chunk_text is empty, returns
    (0, 0, 0.0).

    Strategy: token-window sliding over chunk_text using word spans. For each
    window size around the sentence length (± up to 3 tokens by default),
    compute a difflib.SequenceMatcher ratio against the normalized sentence.
    """
    if not chunk_text:
        return 0, 0, 0.0

    sentence_norm = _normalize_for_local(sentence)
    if not sentence_norm:
        return 0, 0, 0.0

    spans = _word_spans(chunk_text)
    n = len(spans)
    if n == 0:
        return 0, 0, 0.0

    # Estimate sentence length in words
    sent_words = len(_word_spans(sentence_norm))
    if sent_words <= 0:
        sent_words = 1

    # Determine window sizes to try around the sentence length
    if min_window_words is None:
        min_window_words = max(1, sent_words - 3)
    if max_window_words is None:
        max_window_words = min(n, sent_words + 3)
    if min_window_words > max_window_words:
        min_window_words, max_window_words = max_window_words, min_window_words

    best_score = -1.0
    best_cs, best_ce = 0, 0

    for win in range(min_window_words, max_window_words + 1):
        if win <= 0:
            continue
        for i in range(0, n - win + 1):
            cs = spans[i][0]
            ce = spans[i + win - 1][1]
            cand = chunk_text[cs:ce]
            cand_norm = _normalize_for_local(cand)
            if not cand_norm:
                continue
            score = difflib.SequenceMatcher(None, sentence_norm, cand_norm).ratio()
            if score > best_score:
                best_score = score
                best_cs, best_ce = cs, ce

    if best_score < 0:
        return 0, 0, 0.0
    return best_cs, best_ce, float(best_score)


def _build_sliding_chunks(
    pages: List[str], window_words: int, stride_words: int
) -> List[Dict[str, Any]]:
    """Create sliding-window chunks over all pages.

    Each chunk is a dict with:
    - page_index: int
    - char_start: int (page-level character index)
    - char_end: int (page-level character index)
    - text: str (substring of the page)
    """
    chunks: List[Dict[str, Any]] = []
    for p_idx, page_text in enumerate(pages):
        spans = _word_spans(page_text)
        n = len(spans)
        if n == 0:
            continue

        if n <= window_words:
            cs, ce = spans[0][0], spans[-1][1]
            chunks.append(
                {
                    "page_index": p_idx,
                    "char_start": cs,
                    "char_end": ce,
                    "text": page_text[cs:ce],
                }
            )
            continue

        i = 0
        while i < n:
            end_word = min(i + window_words, n)
            cs, ce = spans[i][0], spans[end_word - 1][1]
            chunks.append(
                {
                    "page_index": p_idx,
                    "char_start": cs,
                    "char_end": ce,
                    "text": page_text[cs:ce],
                }
            )
            if end_word == n:
                break
            i += stride_words
            if i >= n:
                break
    return chunks


def coarsely_align_book_transcription(request_data: json, transcriptSentences: list, transcriptStartTimes: list):
    try:
        validate_request_data(request_data, ["pages"])
    except ValueError as e:
        raise e

    pages, transcript_sentences , transcript_start_times = _validate_inputs(
        request_data.get("pages"), transcriptSentences, transcriptStartTimes
    )

    if len(pages) == 0 or len(transcript_sentences) == 0:
        return []

    # Chunking parameters (defaults; can be overridden in request_data)
    window_words = int(request_data.get("chunk_window_words", 80))
    stride_words = int(request_data.get("chunk_stride_words", 40))
    if window_words <= 0 or stride_words <= 0:
        raise ValueError("chunk_window_words and chunk_stride_words must be positive integers.")

    chunks = _build_sliding_chunks(pages, window_words, stride_words)
    if len(chunks) == 0:
        return []

    # Fit TF-IDF on chunks
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), norm="l2")
    X_chunks = vectorizer.fit_transform([_clean_spaces(c["text"]) for c in chunks])
    X_sents = vectorizer.transform([_clean_spaces(s) for s in transcript_sentences])

    # Cosine similarity using L2-normalized vectors
    similarity = X_chunks @ X_sents.T  # (n_chunks, n_sents)

    alignments: List[Dict[str, Any]] = []
    for s_idx, sent in enumerate(transcript_sentences):
        sims_column = similarity[:, s_idx].toarray().ravel()
        best_chunk_idx = int(sims_column.argmax())
        best_score = float(sims_column[best_chunk_idx])
        best_chunk = chunks[best_chunk_idx]

        # to remove text not in the pdf.
        if best_score >= 0.25:
            # Fine local alignment within the best chunk text
            chunk_text = best_chunk["text"]
            local_cs_rel, local_ce_rel, local_score = _best_local_alignment(sent, chunk_text)
            fine_char_start = best_chunk["char_start"] + local_cs_rel
            fine_char_end = best_chunk["char_start"] + local_ce_rel if local_ce_rel > 0 else best_chunk["char_end"]
            fine_text = request_data["pages"][best_chunk["page_index"]][fine_char_start:fine_char_end]

            alignments.append(
                {
                    "sentence": sent,
                    "page_index": best_chunk["page_index"],
                    # Coarse alignment outputs
                    "similarity": best_score,
                    "char_start": best_chunk["char_start"],
                    "char_end": best_chunk["char_end"],
                    # Fine alignment outputs
                    "fine_char_start": fine_char_start,
                    "fine_char_end": fine_char_end,
                    "fine_similarity": local_score,
                    "fine_text": fine_text,
                    # Additional metadata
                    "start_time": transcript_start_times[s_idx],
                    "chunk_text": chunk_text,
                }
            )

    return alignments
