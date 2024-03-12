<!-- index.php -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Control y Registro de la Producción</title>
    <link rel="stylesheet" type="text/css" href="CSS/index.css">
    <link rel="stylesheet" type="text/css" href="CSS/header.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <link rel="icon" href="/imagenes/favicon.ico" type="image/x-icon">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/series-label.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/modules/export-data.js"></script>
    <script src="https://code.highcharts.com/modules/accessibility.js"></script>
    <script src="https://www.gstatic.com/charts/loader.js"></script>
    <style>
        /* Estilos para la tabla */
        table {
        border-collapse: collapse; /* Combina los bordes de las celdas */
        width: 100%;
        }

        /* Estilo para todas las celdas */
        table, th, td {
        border: 2px solid black; /* Define el grosor y el color del borde */
        }

        /* Estilo para las celdas de encabezado (th) */
        th {
        background-color: #f2f2f2; /* Color de fondo para las celdas de encabezado */
        }
    </style>
</head>
<body>

    <br>
    <br>
    <?php 
        require "includes/dashboard_2.php";
        require "includes/header.php";
        require "includes/info_display.php";
        require "includes/chart_viewer_2.php"; 
        ?>     
</body>
</html>
