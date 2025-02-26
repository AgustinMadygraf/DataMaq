/*
Path: frontend/js/services/UiService.js
Este servicio se encarga de actualizar la interfaz de usuario con los datos recibidos de la API.
*/

class UiService {
    /**
     * Actualiza el dashboard completo con los datos recibidos
     * @param {Object} data - Datos recibidos de la API
     */
    static async updateDashboard(data) {
        try {
            // Generar el contenido del info-display
            const infoDisplayHtml = this.generateInfoDisplayHtml(data);
            
            // Actualizar el contenedor con el HTML generado
            const container = document.getElementById('info-display-container');
            if (container) {
                container.innerHTML = infoDisplayHtml;
            }
            
            // Agregar event listeners a los botones de la botonera
            this.setupBotoneraEventListeners();
            
            return true;
        } catch (error) {
            console.error('Error en UiService.updateDashboard:', error);
            throw error;
        }
    }
    
    /**
     * Genera el HTML para el info-display
     * @param {Object} data - Datos recibidos de la API
     * @returns {string} HTML generado
     */
    static generateInfoDisplayHtml(data) {
        try {
            console.log("UiService - Generando HTML para info-display");
            const { vel_ult_calculada, formatoData, uiData } = data;
            const { formato, ancho_bobina } = formatoData;
            const { estiloFondo } = uiData;
            
            // Generar la botonera
            const botoneraHtml = this.generateBotoneraHtml(data);
            
            // Retornar el HTML completo del info-display
            // Asegurarnos de que el div#container se crea correctamente
            const html = `
                <div class="hoja" style="${estiloFondo}">
                    <div class="info">
                        <div class="cabecera">
                            <div class="c1">
                                <p2>Velocidad ${vel_ult_calculada} unidades por minuto</p2>
                                <p1>Formato ${formato}</p1>
                                <p2>Ancho Bobina ${ancho_bobina}</p2>
                            </div>
                        </div>
                        <div id="container" class="graf"></div>
                        <div class="botonera-container">
                            ${botoneraHtml}
                        </div>
                    </div>
                </div>
            `;
            
            console.log("UiService - HTML para info-display generado correctamente");
            return html;
        } catch (error) {
            console.error("UiService - Error en generateInfoDisplayHtml:", error);
            return `<div class="alert alert-danger">Error al generar la visualización: ${error.message}</div>`;
        }
    }
    
    /**
     * Genera el HTML para la botonera
     * @param {Object} data - Datos recibidos de la API
     * @returns {string} HTML generado
     */
    static generateBotoneraHtml(data) {
        try {
            const { periodo, conta } = data;
            const { refClass, preConta, postConta } = data.uiData;
            const csrfToken = window.initialData?.csrfToken || '';
            
            return `
                <div class="botonera">
                    <form action="?periodo=${periodo}&conta=${preConta}" method="post" class="botonI">
                        <input type="hidden" name="csrf_token" value="${csrfToken}">
                        <input type="submit" value="${periodo} anterior" class="presione">
                    </form>
                    <div class='spacer'></div>
                    <form action="?periodo=semana&conta=${conta}" method="post" class="periodo">
                        <input type="hidden" name="csrf_token" value="${csrfToken}">
                        <input type="submit" value="semana" class="${refClass[0]}">
                    </form>
                    <form action="?periodo=turno&conta=${conta}" method="post" class="periodo">
                        <input type="hidden" name="csrf_token" value="${csrfToken}">
                        <input type="submit" value="turno" class="${refClass[1]}">
                    </form>
                    <form action="?periodo=hora&conta=${conta}" method="post" class="periodo">
                        <input type="hidden" name="csrf_token" value="${csrfToken}">
                        <input type="submit" value="2 horas" class="${refClass[2]}">
                    </form>
                    <div class='spacer'></div>
                    <form action="?periodo=${periodo}&conta=${postConta}" method="post" class="botonD">
                        <input type="hidden" name="csrf_token" value="${csrfToken}">
                        <input type="submit" value="${periodo} siguiente" class="presione">
                    </form>
                    <form action="?periodo=${periodo}" method="post" class="fin">
                        <input type="hidden" name="csrf_token" value="${csrfToken}">
                        <input type="submit" value='>|' class="presione">
                    </form>
                </div>
            `;
        } catch (error) {
            console.error('Error en UiService.generateBotoneraHtml:', error);
            return `<div class="alert alert-danger">Error en la botonera: ${error.message}</div>`;
        }
    }
    
    /**
     * Configura event listeners para los botones de la botonera
     */
    static setupBotoneraEventListeners() {
        // Implementar la funcionalidad de los botones utilizando AJAX en lugar de envío de formulario
        const forms = document.querySelectorAll('.botonera form');
        
        forms.forEach(form => {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                // Extraer periodo y conta de la URL del formulario
                const action = form.getAttribute('action');
                const params = new URLSearchParams(action.split('?')[1]);
                const periodo = params.get('periodo');
                const conta = params.get('conta');
                
                // Mostrar indicador de carga
                document.getElementById('loading-indicator').style.display = 'flex';
                
                try {
                    // Actualizar la URL sin recargar la página
                    window.history.pushState({}, '', action);
                    
                    // Cargar los nuevos datos
                    const response = await import('./ApiService.js').then(module => {
                        return module.default.getDashboardData(periodo, conta);
                    });
                    
                    if (response.status === 'success') {
                        // Actualizar la UI con los nuevos datos
                        await UiService.updateDashboard(response.data);
                        
                        // Actualizar los datos del gráfico
                        window.chartData = {
                            conta: response.data.conta,
                            rawdata: response.data.rawdata,
                            ls_periodos: response.data.ls_periodos,
                            menos_periodo: response.data.menos_periodo,
                            periodo: response.data.periodo
                        };
                        
                        // Notificar que los datos del gráfico están listos
                        document.dispatchEvent(new CustomEvent('chartDataReady'));
                    } else {
                        throw new Error(response.message || 'Error al cargar los datos');
                    }
                } catch (error) {
                    console.error('Error al procesar la acción del botón:', error);
                    alert('Error: ' + error.message);
                } finally {
                    // Ocultar indicador de carga
                    document.getElementById('loading-indicator').style.display = 'none';
                }
            });
        });
    }
}

export default UiService;