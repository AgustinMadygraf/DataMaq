<!--includes/SendData_python.php-->
<?php
require_once __DIR__ . '/../backend/core/Database.php';

// Obtener el último registro de la base de datos local
function obtenerUltimoRegistro() {
    $database = Database::getInstance();
    $conexion = $database->getConnection();
    
    $sql = "SELECT unixtime, HR_COUNTER1, HR_COUNTER2 FROM intervalproduction ORDER BY unixtime DESC LIMIT 1";
    $result = $conexion->query($sql);
    $data = array();
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()){
            $data[] = $row;
        }
    }
    return $data;
}

// Enviar datos a la base de datos remota
function enviarDatosRemotos($unixtime, $HR_COUNTER1, $HR_COUNTER2) {
    $url = "http://10.176.61.55/DataMaq/includes/receiveAndUpdateDB.php?unixtime=$unixtime&HR_COUNTER1=$HR_COUNTER1&HR_COUNTER2=$HR_COUNTER2";
    
    // Mostrar los datos y la URL en pantalla
    echo "Unixtime: <br>$unixtime<br><br>";
    echo "HR_COUNTER1: <br>$HR_COUNTER1<br><br>";
    echo "HR_COUNTER2: <br>$HR_COUNTER2<br><br>";
    echo "URL: <br>$url<br><br>";

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    return $response;
}

// Procesar y enviar el último registro
$ultimoRegistro = obtenerUltimoRegistro();
if ($ultimoRegistro) {
    $registro = $ultimoRegistro[0]; // Obtener el primer (y único) elemento
    $response = enviarDatosRemotos($registro['unixtime'], $registro['HR_COUNTER1'], $registro['HR_COUNTER2']);

    if ($response !== false) {
        echo "<br>Respuesta del servidor remoto: $response<br>";
    } else {
        echo "Error al enviar datos.<br>";
    }
} else {
    echo "No se encontraron registros para enviar.<br>";
}
?>