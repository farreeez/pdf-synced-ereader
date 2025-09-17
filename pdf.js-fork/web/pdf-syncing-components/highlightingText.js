class HighlightingText {
  #opts;
  #eventBus;

  constructor(options, eventBus) {
    this.#opts = options;
    this.#eventBus = eventBus;
    this.#bindListeners();
  }

  #bindListeners() {
    this.#eventBus._on("getText", evt => {
      console.log("getting text for highlighting");
    });
  }

  reset() {
    console.log("cleaning up");
  }
}

export { HighlightingText };
