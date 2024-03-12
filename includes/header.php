<?php 
//header.php

echo '<!DOCTYPE html><html><head> <meta charset="UTF-8"> <link rel="stylesheet" type="text/css" href="CSS/index.css"> <link rel="stylesheet" type="text/css" href="CSS/header.css"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon"> <link rel="icon" href="/imagenes/favicon.ico" type="image/x-icon"> </head><body>';
echo "<header> <br><br><br> <div class='topnav'> <ul>";

// Identificar la página actual
$paginaActual = basename($_SERVER['PHP_SELF']);

// Clase para el enlace activo
$claseActiva = "class='active'";

echo "<li><a href='index.php' ".($paginaActual == 'index.php' ? $claseActiva : "").">DataMaq</a></li>";
echo "<li><a href='PanelControlModbus.php' ".($paginaActual == 'PanelControlModbus.php' ? $claseActiva : "").">Estado del Equipo</a></li>";
echo "<li><a href='/Bolsas/index.php' ".($paginaActual == 'Bolsas/index.php' ? $claseActiva : "").">Costos Bolsas</a></li>";
echo "<li><a href='/horas/index.php' ".($paginaActual == '/horas/index.php' ? $claseActiva : "").">Horas</a></li>";
echo "<li><a href='/DataMaq/index.php' ".($paginaActual == '/DataMaq/index.php' ? $claseActiva : "").">DataMaq</a></li>";
echo "<li><a href='/phpMyAdmin/' target='_blank'>PHP MyAdmin</a></li>";

echo "</ul></div></header>";
