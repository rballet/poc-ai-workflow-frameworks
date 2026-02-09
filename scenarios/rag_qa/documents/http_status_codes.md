# HTTP Status Codes

HTTP status codes are three-digit numbers returned by a server to indicate the result of a client's request. They are grouped into five categories.

## 1xx Informational

These indicate that the request was received and the server is continuing to process it. `100 Continue` tells the client to proceed with sending the request body. These are rarely encountered in typical web development.

## 2xx Success

The request was successfully received, understood, and accepted. `200 OK` is the standard success response. `201 Created` means a new resource was successfully created (common in REST APIs after POST requests). `204 No Content` indicates success but with no response body (used for DELETE operations).

## 3xx Redirection

The client must take additional action to complete the request. `301 Moved Permanently` means the resource has permanently moved to a new URL. Clients and search engines should update their references. `302 Found` (commonly used as a temporary redirect) means the resource is temporarily at a different URL, and the client should continue using the original URL for future requests. `304 Not Modified` indicates the cached version is still valid.

## 4xx Client Errors

The request contains an error on the client side. `400 Bad Request` means the server cannot process the request due to malformed syntax. `401 Unauthorized` means authentication is required and has either failed or not been provided. `403 Forbidden` means the server understood the request but refuses to authorize it (different from 401 -- the identity is known but lacks permission). `404 Not Found` means the server cannot find the requested resource. The URL may be wrong, or the resource may have been removed without a redirect. `429 Too Many Requests` indicates rate limiting.

## 5xx Server Errors

The server failed to fulfill a valid request. `500 Internal Server Error` is a generic server-side error. `502 Bad Gateway` means a gateway or proxy received an invalid response from an upstream server. `503 Service Unavailable` means the server is temporarily unable to handle the request, often due to maintenance or overload.
