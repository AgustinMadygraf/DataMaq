<!-- dashboard.php -->
<?php
require 'db_functions.php';
date_default_timezone_set('America/Argentina/Buenos_Aires');
setlocale(LC_TIME, "spanish");
$segundos = 60; // Refrescar cada 60 segundos


// Variable que registra qué período de tiempo mostrar por defecto
$periodo = 'semana';
$ls_periodos = ['semana' => 15552000, 'turno' => 7776000, 'hora' => 2592000];
$ls_class = ['semana' => [1, 0, 0], 'turno' => [0, 1, 0], 'hora' => [0, 0, 1]];
$ref_class = ['presione', 'presado'];
$menos_periodo = ['semana' => 'turno', 'turno' => 'hora', 'hora' => 'hora'];

// Comprobar si se cambió el período a través de GET
if ($_GET && array_key_exists("periodo", $_GET)) {
    if (array_key_exists($_GET["periodo"], $ls_periodos)) {
        $periodo = $_GET["periodo"];
    }
}
$class = $ls_class[$periodo];

function sql_query($campo) {
    return "SELECT `unixtime`, `$campo` FROM `intervalproduction_d`  ORDER BY `unixtime` DESC LIMIT 1";
}

$res = getArraySQL(sql_query("HR_COUNTER1"));
$vel_ult = $res[0]['HR_COUNTER1'] ;
$unixtime = $res[0]['unixtime'] ;




// Si la variable 'test' aparece en $_GET, el refresco se hace cada segundo en vez de cada 20 segundos.
header("Refresh:" . $segundos);

// Valores para la ubicación del degradado de advertencia
$d = array();
for ($i = 0; $i < 4; $i++) {
    $d[$i] = 350 - $pot - 10 * $i;
}

$date = date(DATE_RFC2822);
$newDate = date("D, d M Y" . (" 00:00:00") . " O");

$valorInicial = $unixtime * 1000;
$conta = $valorInicial;
if ($_GET && array_key_exists("conta", $_GET)) {
    $conta = $_GET["conta"];
    if ($conta > $valorInicial) {
        $conta = $valorInicial;
    }
}

$tiempo1 = ($conta/1000) - $ls_periodos[$periodo] - 80*60;
$tiempo2 = $conta/1000 ;
$sql = "SELECT `unixtime`, `HR_COUNTER1`, `HR_COUNTER2`  from `intervalproduction_d` WHERE  unixtime > " . $tiempo1 . " AND unixtime <= " . $tiempo2 . " ORDER BY `unixtime` ASC ;";
$rawdata = getArraySQL($sql);



?>
