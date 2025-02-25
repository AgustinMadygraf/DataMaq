<?php
/*
Path: backend/api/Router.php
*/

$requestMethod = $_SERVER['REQUEST_METHOD'];
$requestUri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Remove base path if necessary. Adjust this prefix based on your deployment.
$basePath = '/DataMaq/backend/api';
$endpoint = '/' . ltrim(substr($requestUri, strlen($basePath)), '/');

// Route API calls if endpoint starts with "/endpoints"
if (strpos($endpoint, '/endpoints') === 0) {
    // Construir ruta dinámica al archivo del endpoint.
    $apiFile = __DIR__ . $endpoint . '.php';
    if (file_exists($apiFile)) {
        require_once $apiFile;
    } else {
        header("HTTP/1.0 404 Not Found");
        echo json_encode(['status' => 'error', 'message' => 'Endpoint not found']);
    }
    exit;
}

switch ($endpoint) {
    default:
        header("HTTP/1.0 404 Not Found");
        echo json_encode(['status' => 'error', 'message' => 'Endpoint not found']);
        break;
}
