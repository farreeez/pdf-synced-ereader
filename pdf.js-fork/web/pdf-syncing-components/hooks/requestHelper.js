// Shared request helper to unify fetch-based HTTP verbs with axios-like response + error shape.

/**
 * Core request used by specific verb helpers.
 * @param {string} method
 * @param {string} url
 * @param {any} body
 * @param {{ headers?: Record<string,string> }} config
 * @returns {Promise<{ data: any, status: number, headers: Headers }>}
 */
async function coreRequest(method, url, body, config = {}) {
  const headers = new Headers(config.headers || {});
  // Auto-add JSON header if body is plain object and no explicit Content-Type
  if (
    body !== undefined &&
    !(body instanceof FormData) &&
    !headers.has("Content-Type")
  ) {
    if (
      typeof body === "object" &&
      !(body instanceof Blob) &&
      !(body instanceof ArrayBuffer)
    ) {
      headers.set("Content-Type", "application/json");
    }
  }

  const preparedBody =
    body === undefined
      ? undefined
      : headers.get("Content-Type")?.includes("application/json") &&
          typeof body !== "string"
        ? JSON.stringify(body)
        : body;

  const response = await fetch(url, { method, headers, body: preparedBody });

  let data = null;
  const contentType = response.headers.get("Content-Type") || "";
  if (contentType.includes("application/json")) {
    try {
      data = await response.json();
    } catch (_) {
      data = null;
    }
  } else {
    try {
      data = await response.text();
    } catch (_) {
      data = null;
    }
  }

  if (!response.ok) {
    const message =
      data && typeof data === "object" && "message" in data
        ? data.message
        : `HTTP ${response.status}`;
    const error = new Error(
      typeof message === "string" ? message : "Request failed"
    );
    error.response = {
      data,
      status: response.status,
      headers: response.headers,
    };
    throw error;
  }

  return { data, status: response.status, headers: response.headers };
}

export function getJson(url, config) {
  return coreRequest("GET", url, undefined, config);
}
export function postJson(url, body, config) {
  return coreRequest("POST", url, body, config);
}
export function putJson(url, body, config) {
  return coreRequest("PUT", url, body, config);
}
export function deleteJson(url, config) {
  return coreRequest("DELETE", url, undefined, config);
}
