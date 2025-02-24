<?php
/*
Path: backend/api/dashboard_test.php
Versión experimental del endpoint de dashboard para pruebas.
*/

// Configuración básica y carga de dependencias
require_once __DIR__ . '/../config/error_config.php';
require_once __DIR__ . '/../controllers/DashboardController.php';

try {
    // Centralizar la extracción y saneamiento de parámetros
    $params = filter_input_array(INPUT_GET, [
        'periodo' => FILTER_SANITIZE_STRING,
        'conta'   => FILTER_SANITIZE_NUMBER_INT,
    ]);

    if (isset($params['periodo'])) {
        $_GET['periodo'] = $params['periodo'];
    }
    if (isset($params['conta'])) {
        $_GET['conta'] = $params['conta'];
    }

    $controller = new DashboardController();
    $controller->index(true); // salida en formato JSON
} catch (Exception $e) {
    error_log("dashboard_test.php API error: " . $e->getMessage());
    header('Content-Type: application/json; charset=utf-8', true, 500);
    echo json_encode(['status' => 'error', 'message' => "Ocurrió un error. Consulte los logs."]);
    exit;
}
