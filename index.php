<?php
require_once __DIR__ . '/backend/config/error_config.php';
require_once __DIR__ . '/backend/core/ViewRenderer.php';
require_once __DIR__ . '/backend/helpers/CsrfHelper.php';

// Inicializar variables
$periodo = 'semana';
$ls_periodos = ['semana' => 604800, 'turno' => 28800, 'hora' => 7200];
$ls_class = ['semana' => [1, 0, 0], 'turno' => [0, 1, 0], 'hora' => [0, 0, 1]];
$ref_class = ['presione', 'presado'];
$menos_periodo = ['semana' => 'turno', 'turno' => 'hora', 'hora' => 'hora'];

// Validar y procesar parámetros GET
if ($_GET && array_key_exists("periodo", $_GET)) {
    if (array_key_exists($_GET["periodo"], $ls_periodos)) {
        $periodo = $_GET["periodo"];
    }
}
$class = $ls_class[$periodo];

// Obtener datos del controlador
require_once __DIR__ . '/backend/controllers/DashboardController.php';
$controller = new DashboardController();
$data = $controller->index();
extract($data);

// Asegurarse de que todas las variables necesarias estén definidas
if (!isset($gradient)) {
    $gradient = [25, 50, 75, 100]; // valores por defecto
}

if (!isset($formatoData)) {
    $formatoData = [
        'formato' => 'No disponible',
        'ancho_bobina' => 'No disponible'
    ];
}

if (!isset($vel_ult_calculada)) {
    $vel_ult_calculada = '0';
}

// Renderizar la botonera
$botoneraHtml = ViewRenderer::render(__DIR__ . '/frontend/templates/botonera.html', [
    'csrfToken' => CsrfHelper::generateToken(),
    'periodo' => $periodo,
    'conta' => $conta,
    'refClass0' => $ref_class[$class[0]],
    'refClass1' => $ref_class[$class[1]],
    'refClass2' => $ref_class[$class[2]],
    'preConta' => $conta - 1000 * $ls_periodos[$periodo],
    'postConta' => $conta + 1000 * $ls_periodos[$periodo]
]);

$infoDisplayHtml = ViewRenderer::render(__DIR__ . '/frontend/templates/info_display.html', [
    'vel_ult_calculada' => $vel_ult_calculada,
    'formato' => $formatoData['formato'],
    'ancho_bobina' => $formatoData['ancho_bobina'],
    'botonera' => $botoneraHtml,  // Añadimos la botonera aquí
    'estiloFondo' => sprintf(
        "background: linear-gradient(195deg, rgba(107,170,34,0.9) %d%%, rgba(255,164,1,0.9) %d%%, rgba(234,53,34,0.9) %d%%, rgba(100,10,5,0.9) %d%%);",
        $gradient[3], $gradient[2], $gradient[1], $gradient[0]
    )
]);

// Renderizar las diferentes partes de la página
$headerHtml = ViewRenderer::render(__DIR__ . '/frontend/templates/header.html', [
    'menuItems' => ViewRenderer::render(__DIR__ . '/frontend/templates/menu_items.html', [
        'paginaActual' => basename($_SERVER['PHP_SELF'])
    ])
]);

// Renderizar la plantilla principal
echo ViewRenderer::render(__DIR__ . '/frontend/templates/main.html', [
    'header' => $headerHtml,
    'infoDisplay' => $infoDisplayHtml,
    'chartData' => json_encode([
        'conta' => $conta,
        'rawdata' => $rawdata,
        'ls_periodos' => $ls_periodos,
        'menos_periodo' => $menos_periodo,
        'periodo' => $periodo
    ])
]);
?>