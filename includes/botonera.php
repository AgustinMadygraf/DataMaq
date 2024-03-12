<!-- botonera.php -->
<div class="botonera">
    
    <form action="<?= $_SERVER["PHP_SELF"] . '?periodo=' . $periodo . '&conta=' . ($conta - 1000*$ls_periodos[$periodo]) ?>" method="post" class="botonI">
        <input type="submit" value="<?= $periodo . ' anterior' ?>" class="presione">
    </form>

    <div class='spacer'></div>

    <form action="<?= $_SERVER["PHP_SELF"] . '?periodo=semana&conta=' . $conta ?>" method="post" class="periodo">
        <input type="submit" value="semana" class="<?= $ref_class[$class[0]] ?>">
    </form>

    

    <form action="<?= $_SERVER["PHP_SELF"] . '?periodo=turno&conta=' . $conta ?>" method="post" class="periodo">
        <input type="submit" value="turno" class="<?= $ref_class[$class[1]] ?>">
    </form>

    <form action="<?= $_SERVER["PHP_SELF"] . '?periodo=hora&conta=' . $conta ?>" method="post" class="periodo">
        <input type="submit" value="2 horas" class="<?= $ref_class[$class[2]] ?>">
    </form>

    <div class='spacer'></div>

    <form action="<?= $_SERVER["PHP_SELF"] . '?periodo=' . $periodo . '&conta=' . ($conta + 1000*$ls_periodos[$periodo]) ?>" method="post" class="botonD">
        <input type="submit" value="<?= $periodo . ' siguiente' ?>" class="presione">
    </form>

    <form action="<?= $_SERVER["PHP_SELF"] . '?periodo=' . $periodo ?>" method="post" class="fin">
        <input type="submit" value='>|' class="presione">
    </form>
</div>
