import {
  createProjectApi,
  getProjectNamesApi,
  transcribeAudioBookApi,
} from "./api/syncedEreaderApi.js";

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
      // console.log("getting text for highlighting");

      // if (!this.#texts || this.#texts.length == 0) {
      //   this.#texts = await PDFViewerApplication.pdfViewer.getAllText(true);
      // }

      // PDFViewerApplication.pdfViewer.currentPageNumber = 300;

      // console.log(this.#texts);

      console.log("Testing endpoints");

      const { createProject, data, isLoading, isError } = createProjectApi();
      const { getProjectNames } = getProjectNamesApi();
      const { transcribeAudioBook } = transcribeAudioBookApi();

      // const createdProjectName = await createProject("big-book");
      const existingProjectNames = await getProjectNames();
      // Call transcribe audiobook endpoint (projectName, isSingleFile, absoluteAudioPath)
      const transcribedAudioOutput = await transcribeAudioBook(
        "test",
        true,
        "C:/Users/xxfar/OneDrive/Desktop/coding/projects/pdf-synced-ereader/books/Sam Walton, made in America my story - Sam Walton/audio/Sam Walton Made in America (Unabridged) - 01.m4b"
      );

      // console.log(createdProjectName);
      console.log(existingProjectNames);
      console.log(transcribedAudioOutput);
    });
  }

  reset() {
    console.log("cleaning up");
  }
}

export { HighlightingText };
