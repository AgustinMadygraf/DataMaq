<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estado del Equipo</title>
    <link rel="stylesheet" type="text/css" href="CSS/index.css">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; }
        .table { margin-top: 20px; }
    </style>
</head>
<body>
    <?php
        require "includes/header.php";
    ?>
    <div class="container">
        <h1 class="text-center">Estado del Equipo - Registros Modbus</h1>

        <table class="table table-striped">
            <thead class="thead-dark">
                <tr>
                    <th>Direccion Modbus</th>
                    <th>Registro</th>
                    <th>Descripcion</th>
                    <th>Valor</th>                    
                </tr>
            </thead>
            <tbody>
                <!-- Los datos se cargarán aquí a través de AJAX -->
            </tbody>
        </table>
    </div>

    <!-- Bootstrap JS y dependencias -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    
    <script>
        $(document).ready(function(){
            function actualizarDatos() {
                $.ajax({
                    url: 'includes/fetch_data.php', // Asegúrate de que esta ruta es correcta
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        var filas = '';
                        $.each(data, function(key, registro) {
                            filas += '<tr>' +
                                        '<td>' + registro.direccion_modbus + '</td>' +
                                        '<td>' + registro.registro + '</td>' +
                                        '<td>' + registro.descripcion + '</td>' +
                                        '<td>' + registro.valor + '</td>' +
                                     '</tr>';
                        });
                        $('tbody').html(filas);
                    }
                });
            }

            // Actualizar los datos cada 0.5 segundos
            setInterval(actualizarDatos, 500);
            actualizarDatos(); // Cargar inicialmente los datos
        });
    </script>
</body>
</html>
