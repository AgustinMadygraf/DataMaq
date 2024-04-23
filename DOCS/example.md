# Ejemplos de Uso de DigiRail para Monitoreo y Mejora de OEE

Exploramos cómo utilizar DigiRail, una herramienta poderosa para la adquisición automática de datos relevantes en entornos industriales. Este documento no oficial muestra el potencial de DigiRail para monitorear vueltas de revolución, así como parámetros críticos como presión y temperatura, contribuyendo así a mejorar las métricas de OEE en tus operaciones.

## Monitoreo de Vueltas de Revolución (Modo Contador)

DigiRail se puede configurar para capturar datos de vueltas de revolución a través de sus entradas digitales en modo contador, ofreciendo un seguimiento preciso de la actividad de la maquinaria.

### Configuración

1. Conecta tu sensor de revoluciones a la entrada digital en DigiRail destinada para el modo contador.
2. Utiliza el software de configuración para ajustar la entrada digital al modo "Contador".
3. Define los parámetros de acuerdo a las especificaciones de tu sensor y las necesidades específicas de tu proceso.

### Ejemplo de Aplicación

Considera el monitoreo de un motor esencial en tu línea de producción. Al emplear DigiRail para contar las vueltas, podrás:

- Identificar variaciones en la velocidad que señalen necesidad de mantenimiento preventivo.
- Estimar el tiempo total de operación al comparar los datos de revolución a lo largo del tiempo.

![Ejemplo de Monitoreo](https://github.com/AgustinMadygraf/DigiRail/blob/main/src/config/img1.jpg)

## Medición de Presión y Temperatura

DigiRail también permite el monitoreo de parámetros ambientales como la presión y temperatura, esenciales para el mantenimiento preventivo y la eficiencia operativa.

### Configuración

1. Enlaza los sensores de presión y temperatura a las entradas analógicas adecuadas en DigiRail.
2. En el software de configuración, asigna cada canal al tipo de señal correspondiente (ej., 4-20 mA para presión, PT100 para temperatura).

### Ejemplo de Aplicación

El seguimiento de la presión y temperatura en un sistema hidráulico te permite:

- Evitar fallas por sobrecalentamiento o presión de operación inadecuada.
- Ajustar las operaciones en tiempo real para optimizar la eficiencia energética.

## Cálculo de OEE

El OEE, o Eficiencia Global del Equipo, es un indicador compuesto por la disponibilidad, rendimiento y calidad. Con DigiRail, es posible:

- **Calcular la Disponibilidad**: Comparando el tiempo de operación (obtenido de las vueltas de revolución) con el tiempo planificado de producción.
- **Evaluar el Rendimiento**: Midiendo la cantidad real de producción frente a la cantidad teórica, considerando las paradas y ralentizaciones.
- **Medir la Calidad**: Comparando la producción sin defectos con la producción total.

DigiRail simplifica la recopilación de los datos necesarios para estas métricas, permitiendo tomar decisiones informadas para la mejora continua de la producción.

Para más información sobre configuraciones específicas y ejemplos avanzados, te animamos a revisar el [manual completo de DigiRail](https://cdn.novusautomation.com/downloads/manual_digirail_connect_v10x_m_es.pdf).