import axios from "axios";

/**
 * Posts data to an API endpoint without relying on React state.
 * @param {string} [initialUrl] - Default URL used when one is not provided to post.
 * @returns {{ readonly data: unknown, readonly isLoading: boolean, readonly isError: boolean, post: (url?: string, body?: any, config?: import("axios").AxiosRequestConfig) => Promise<unknown> }}
 */
export default function createAsync(initialUrl = "") {
  const state = {
    data: null,
    isLoading: false,
    isError: false,
  };

  const post = async (url = initialUrl, body, config = {}) => {
    state.isLoading = true;
    state.isError = false;

    try {
      const response = await axios.post(url, body, config);
      state.data = response.data;
      return response.data;
    } catch (error) {
      state.isError = true;
      const message =
        error?.response?.data?.message || "An unexpected error occurred";
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
    post,
  };
}
