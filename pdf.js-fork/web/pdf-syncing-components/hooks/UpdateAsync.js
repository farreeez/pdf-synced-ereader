import axios from "axios";

/**
 * Updates data on an API endpoint without relying on React hooks.
 * @param {string} [initialUrl] - Default URL used when one is not provided to put.
 * @returns {{ readonly data: unknown, readonly isLoading: boolean, readonly isError: boolean, put: (url?: string, body?: any, config?: import("axios").AxiosRequestConfig) => Promise<unknown> }}
 */
export default function updateAsync(initialUrl = "") {
  const state = {
    data: null,
    isLoading: false,
    isError: false,
  };

  const put = async (url = initialUrl, body, config = {}) => {
    state.isLoading = true;
    state.isError = false;

    try {
      const response = await axios.put(url, body, config);
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
    put,
  };
}
