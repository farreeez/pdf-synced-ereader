import { getJson } from "./requestHelper.js";

/**
 * Fetches data from an API endpoint without React state.
 * @param {string} [initialUrl] - Default URL used when one is not provided to etch.
 * @returns {{ readonly data: unknown, readonly isLoading: boolean, readonly isError: boolean, fetch: (url?: string, config?: { headers?: Record<string,string> }) => Promise<unknown> }}
 */
export default function getAsync(initialUrl = "") {
  const state = {
    data: null,
    isLoading: false,
    isError: false,
  };

  const fetch = async (url = initialUrl, config = {}) => {
    state.isLoading = true;
    state.isError = false;

    try {
      const response = await getJson(url, config);
      state.data = response.data;
      return response.data;
    } catch (error) {
      state.isError = true;
      const message =
        error?.response?.data?.message ||
        error?.message ||
        "An unexpected error occurred";
      throw typeof message === "string" ? new Error(message) : new Error();
    } finally {
      state.isLoading = false;
    }
  };

  return {
    get data() {
      return state.data;
    },
    get isLoading() {
      return state.isLoading;
    },
    get isError() {
      return state.isError;
    },
    fetch,
  };
}
