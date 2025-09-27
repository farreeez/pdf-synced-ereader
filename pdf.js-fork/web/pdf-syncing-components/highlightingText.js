import { coarselyAlignTextApi } from "./api/syncedEreaderApi.js";

class HighlightingText {
  #opts;
  #eventBus;
  #texts = null;

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

      console.log("Testing endpoints");

      const { coarselyAlignText } = coarselyAlignTextApi();

      const response = coarselyAlignText("big-book", this.#texts);

      console.log(response);
    });
  }

  reset() {
    console.log("cleaning up");
  }
}

export { HighlightingText };
