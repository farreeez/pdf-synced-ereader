import axios from "axios";
import { useState } from "react";

/**
 * React hook: posts data to an API endpoint.
 * @param initialUrl
 * @returns {{data: unknown, isLoading: boolean, isError: boolean, post: ((function(*): Promise<any|undefined>)|*)}}
 */
export default function useCreateAsync(initialUrl = "") {
  const [data, setData] = useState(null);
  const [isLoading, setLoading] = useState(false);
  const [isError, setError] = useState(false);

  const post = async (url = initialUrl, body, config = {}) => {
    setLoading(true);
    setError(false);

    try {
      const response = await axios.post(url, body, config);
      setData(response.data);
      setLoading(false);
      return response.data;
    } catch (error) {
      setError(true);
      setLoading(false);
      throw error.response?.data?.message || "An unexpected error occurred";
    }
  };

  return { data, isLoading, isError, post };
}
