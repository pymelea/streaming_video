/**
 * API utilities for making HTTP requests
 */
import config from '../config';

/**
 * Generic fetch function with error handling and retries
 * @param {string} endpoint - API endpoint to fetch from
 * @param {Object} options - Fetch options
 * @param {Object} customConfig - Override default config
 * @returns {Promise} - Response data or error
 */
async function fetchApi(endpoint, options = {}, customConfig = {}) {
  const { timeout = config.api.timeout, retries = config.api.retries } = customConfig;

  // Create an AbortController for timeout handling
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  // Add signal to options if not already present
  const fetchOptions = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    signal: options.signal || controller.signal,
  };

  let lastError;

  // Retry logic
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const response = await fetch(`${config.api.baseUrl}${endpoint}`, fetchOptions);

      // Clear timeout since fetch completed
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          JSON.stringify({
            status: response.status,
            statusText: response.statusText,
            data: errorData,
          })
        );
      }

      return await response.json();
    } catch (error) {
      lastError = error;

      // Don't retry if we aborted or if it's the last attempt
      if (error.name === 'AbortError' || attempt === retries) {
        break;
      }

      // Wait before retrying (exponential backoff)
      const delay = Math.min(1000 * 2 ** attempt, 10000);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  // Clear timeout if all attempts failed
  clearTimeout(timeoutId);

  console.error('API request failed after retries:', lastError);
  throw lastError;
}

/**
 * HTTP GET request
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Additional fetch options
 * @param {Object} customConfig - Override default config
 * @returns {Promise} - Response data
 */
const get = (endpoint, options = {}, customConfig = {}) => {
  return fetchApi(endpoint, {
    method: 'GET',
    ...options,
  }, customConfig);
};

/**
 * HTTP POST request
 * @param {string} endpoint - API endpoint
 * @param {Object} data - Data to send in request body
 * @param {Object} options - Additional fetch options
 * @param {Object} customConfig - Override default config
 * @returns {Promise} - Response data
 */
const post = (endpoint, data, options = {}, customConfig = {}) => {
  return fetchApi(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
    ...options,
  }, customConfig);
};

/**
 * HTTP PUT request
 * @param {string} endpoint - API endpoint
 * @param {Object} data - Data to send in request body
 * @param {Object} options - Additional fetch options
 * @param {Object} customConfig - Override default config
 * @returns {Promise} - Response data
 */
const put = (endpoint, data, options = {}, customConfig = {}) => {
  return fetchApi(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
    ...options,
  }, customConfig);
};

/**
 * HTTP DELETE request
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Additional fetch options
 * @param {Object} customConfig - Override default config
 * @returns {Promise} - Response data
 */
const del = (endpoint, options = {}, customConfig = {}) => {
  return fetchApi(endpoint, {
    method: 'DELETE',
    ...options,
  }, customConfig);
};

export { fetchApi, get, post, put, del };
