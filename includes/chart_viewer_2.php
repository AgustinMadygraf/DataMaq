<!-- chart_viewer.php -->
<script type='text/javascript'>
    var doubleClicker = {
        clickedOnce: false,
        timer: null,
        timeBetweenClicks: 400
    };

    var resetDoubleClick = function () {
        clearTimeout(doubleClicker.timer);
        doubleClicker.timer = null;
        doubleClicker.clickedOnce = false;
    };

    var zoomIn = function (event) {
        var tiempo = Highcharts.numberFormat(event.xAxis[0].value + <?= $ls_periodos[$menos_periodo[$periodo]] / 2 ?>);
        window.open("<?=$_SERVER["PHP_SELF"].'?medidor='.$medidor.'&periodo='.$menos_periodo[$periodo].'&conta='?>" + tiempo, "_self");
    };

    var ondbclick = function (event) {
        if (doubleClicker.clickedOnce === true && doubleClicker.timer) {
            resetDoubleClick();
            zoomIn(event);
        } else {
            doubleClicker.clickedOnce = true;
            doubleClicker.timer = setTimeout(function () {
                resetDoubleClick();
            }, doubleClicker.timeBetweenClicks);
        }
    };

    $(function () {
        Highcharts.setOptions({
            global: {
                useUTC: false
            },
            lang: {
                thousandsSep: "",
                months: [
                    'Enero', 'Febrero', 'Marzo', 'Abril',
                    'Mayo', 'Junio', 'Julio', 'Agosto',
                    'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
                ],
                weekdays: [
                    'Domingo', 'Lunes', 'Martes', 'Miércoles',
                    'Jueves', 'Viernes', 'Sábado'
                ]
            }
        });

        var chart;
        $('#container').highcharts({
            chart: {
                type: 'column',
                animation: false,
                marginRight: 10,
                events: {
                    load: function () {

                    },
                    click: function (event) {
                        ondbclick(event);
                    }
                }
            },
            title: {
                text: (function () {
                    return Highcharts.dateFormat("%A, %d %B %Y - %H:%M:%S", <?= $conta; ?>);
                })(),
                events: {
                    load: function () {

                    },
                    click: function (event) {
                        ondbclick(event);
                    }
                }
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 1
            },
            yAxis: {    
                //type: 'logarithmic', // Establece el eje vertical como logarítmico
                title: {
                    text: '[Producción]'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat("%A, %d %B %Y - %H:%M:%S", this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 1) + '  Unidades por minuto';
                }
            },
            legend: {
                enabled: true
            },
            exporting: {
                enabled: true
            },
            series: [
                {
                    name: 'Produccion',
                    animation: false,
                    data: (function () {
                        var data = [];
                        <?php for ($i = 1; $i < count($rawdata); $i++) { ?>
                            data.push([<?= 1000*$rawdata[$i]["unixtime"] ?>, <?= $rawdata[$i]["HR_COUNTER1"]/5 ?>]);
                        <?php } ?>
                        return data;
                    })()
                }
            ]
        });
    });
</script>
