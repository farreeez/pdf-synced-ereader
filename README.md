# PDF Synced E-Reader

![Status](https://img.shields.io/badge/status-work_in_progress-yellow.svg)

An application to synchronize PDF documents with audio narration, highlighting text as it's spoken to create an immersive reading experience.

## About The Project

This project aims to bridge the gap between traditional PDF ebooks and audiobooks. By leveraging machine learning for audio transcription and the web-native capabilities of PDF.js, the PDF Synced E-Reader will allow users to load a PDF and a corresponding audio file. As the audio plays, the application will highlight the exact words in the PDF in real-time, providing a powerful tool for learning, accessibility, and immersive reading.

## How It Works

The synchronization is achieved through a three-stage pipeline:

### 1. Audio Transcription

The process begins with a Python script located in the `/whisper-transcription` directory.

- It uses OpenAI's **Whisper** speech-to-text model to transcribe the audio file.
- The audio is first broken down into manageable chunks to handle large files efficiently.
- The model generates a structured JSON output containing text segments with precise `start` and `end` timestamps.

### 2. PDF Text Layer Extraction

The application uses a forked version of Mozilla's **PDF.js** library to handle PDF rendering and text extraction.

- PDF.js renders each page of the document onto an HTML `<canvas>` element.
- Crucially, it also creates a transparent "text layer" on top of the canvas. This layer contains individual `<span>` elements for words or small groups of words, positioned exactly over their visual representation in the PDF.
- The core of the current development work involves accessing this text layer to extract its content and create a map between the text and its corresponding DOM element.

### 3. Text Matching and Synchronization

This is the heart of the application, where the transcribed audio text is aligned with the PDF's text layer. This is planned as a two-phase process:

1.  **Coarse Alignment:** To quickly find the general location of an audio segment within the PDF, a **TF-IDF (Term Frequency-Inverse Document Frequency)** algorithm will be used. This will help identify which page or paragraph of the PDF is the best match for a given chunk of transcribed text.
2.  **Fine-Grained Alignment:** Once a coarse match is found, a **fuzzy search** or a similar string alignment algorithm (like the Smith-Waterman algorithm) will be used to find the exact sequence of `<span>` elements in the text layer that corresponds to the transcribed text.

Once the exact spans are identified, they can be highlighted in time with the audio playback, using the timestamps from the Whisper transcription.

## Current Status

This project is currently a **work in progress**.

-   **Completed:** The audio transcription pipeline using Python and Whisper is functional.
-   **In Progress:** The primary focus is on the PDF.js integration. The current work involves programmatically accessing the text layer for each page, extracting the text content, and building a data structure that links the text to the DOM elements that can be styled for highlighting.

## Project Structure

```
.
├── /pdf.js-fork/           # A modified version of PDF.js for rendering and text extraction.
├── /whisper-transcription/   # Python module for audio transcription via Whisper.
├── /books/                   # Example directory for PDF and audio files.
└── README.md                 # This file.
```

## Future Goals (Roadmap)

-   Implement the TF-IDF and fuzzy matching algorithms for text alignment.
-   Develop a user interface for loading a PDF and its corresponding audio file.
-   Create a media player interface with playback controls (play, pause, seek).
-   Implement the real-time highlighting feature on the PDF.js viewer.
-   Package the application for broader use.