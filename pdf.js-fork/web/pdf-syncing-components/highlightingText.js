import { PDFViewerApplication } from "../app.js";
import { coarselyAlignTextApi } from "./api/syncedEreaderApi.js";

class HighlightingText {
  #opts;
  #eventBus;
  #texts = null;
  #alignmentData = null;

  constructor(options, eventBus) {
    this.#opts = options;
    this.#eventBus = eventBus;
    this.#bindListeners();
  }

  #bindListeners() {
    this.#eventBus._on("getText", async evt => {
      console.log("getting text for highlighting");

      if (!this.#texts || this.#texts.length == 0) {
        this.#texts = await PDFViewerApplication.pdfViewer.getAllText(true);
      }

      const { coarselyAlignText } = coarselyAlignTextApi();

      if (!this.#alignmentData) {
        console.log("Testing endpoints");
        const alignmentDataObject = await coarselyAlignText("sam", this.#texts);
        this.#alignmentData = alignmentDataObject.alignment_data;
      }

      // console.log(this.#alignmentData);
      // manage highlighting text
      this._highlightText(this.#alignmentData[0]);
    });
  }
  // "sentence": sent,
  // "page_index": best_chunk["page_index"],
  // # Coarse alignment outputs
  // "similarity": best_score,
  // "char_start": best_chunk["char_start"],
  // "char_end": best_chunk["char_end"],
  // # Fine alignment outputs
  // "fine_char_start": fine_char_start,
  // "fine_char_end": fine_char_end,
  // "fine_similarity": local_score,
  // "fine_text": fine_text,
  // # Additional metadata
  // "start_time": transcript_start_times[s_idx],

  _highlightText(alignmentData) {
    const pageIndex = alignmentData.page_index;
    const pdfViewer = PDFViewerApplication.pdfViewer;
    // scroll to page if not on page.
    if (pdfViewer.currentPageNumber != pageIndex) {
      pdfViewer.currentPageNumber = 100;
      setTimeout(() => {}, 1000);
    }

    // starts from 0
    const pageView = pdfViewer.getPageView(99);

    console.log(pageView);
    console.log(alignmentData.page_index);
    console.log(alignmentData);
    // find text within the alignment data and highlight.
  }

  reset() {
    console.log("cleaning up");
  }
}

export { HighlightingText };
