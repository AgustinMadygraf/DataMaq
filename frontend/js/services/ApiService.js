/*
Path: frontend/js/services/ApiService.js
Este servicio se encarga de hacer peticiones a la API del backend.
*/

import appState from '../state/AppState.js';

class ApiService {
    /**
     * URL base para las peticiones API
     */
    static BASE_URL = '/DataMaq/backend/api';
    
    /**
     * Obtiene los datos del dashboard desde la API
     * @param {string} periodo - Periodo de tiempo (semana, turno, hora) - opcional, si no se especifica se obtiene del estado
     * @param {number|null} conta - Timestamp para filtrar datos (opcional) - opcional, si no se especifica se obtiene del estado
     * @returns {Promise<Object>} - Respuesta de la API
     */
    static async getDashboardData(periodo = null, conta = null) {
        try {
            // Marcar como cargando en el estado
            appState.setLoading('dashboard', true);
            
            // Si no se proporcionan parámetros, intentar obtenerlos del estado
            if (periodo === null) {
                const initialData = appState.getInitialData();
                periodo = initialData.periodo || 'semana';
            }
            
            if (conta === null) {
                const initialData = appState.getInitialData();
                conta = initialData.conta;
            }
            
            let url = `${this.BASE_URL}/dashboard.php?periodo=${periodo}`;
            
            if (conta !== null) {
                url += `&conta=${conta}`;
            }
            
            console.log(`ApiService - Obteniendo datos del dashboard: ${url}`);
            
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.status === 'success') {
                // Guardar datos en el estado centralizado
                appState.setChartData({
                    conta: result.data.conta,
                    rawdata: result.data.rawdata,
                    ls_periodos: result.data.ls_periodos,
                    menos_periodo: result.data.menos_periodo,
                    periodo: result.data.periodo
                });
                
                // Mantener compatibilidad con código legacy
                if (typeof window !== 'undefined') {
                    window.chartData = appState.getChartData();
                }
                
                console.log("ApiService - Datos del dashboard obtenidos y guardados en estado:", result.data);
            } else {
                // Registrar error en el estado
                appState.addError('apiService', `Error en la respuesta: ${result.message || 'Respuesta inesperada'}`);
            }
            
            return result;
        } catch (error) {
            console.error('Error en ApiService.getDashboardData:', error);
            
            // Registrar error en el estado
            appState.addError('apiService', error);
            
            return {
                status: 'error',
                message: error.message
            };
        } finally {
            // Marcar como no cargando en el estado
            appState.setLoading('dashboard', false);
        }
    }
    
    /**
     * Envía datos al servidor
     * @param {string} endpoint - Endpoint de la API
     * @param {Object} data - Datos a enviar
     * @param {string} method - Método HTTP (POST, PUT, DELETE)
     * @returns {Promise<Object>} - Respuesta de la API
     */
    static async sendData(endpoint, data, method = 'POST') {
        try {
            // Obtener token CSRF desde el estado centralizado
            const initialData = appState.getInitialData();
            const csrfToken = initialData.csrfToken || '';
            
            if (!csrfToken) {
                console.warn('ApiService - Token CSRF no disponible en el estado');
            }
            
            const response = await fetch(`${this.BASE_URL}/${endpoint}`, {
                method,
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.status !== 'success') {
                // Registrar error en el estado
                appState.addError('apiService', `Error en ${endpoint}: ${result.message || 'Error desconocido'}`);
            }
            
            return result;
        } catch (error) {
            console.error(`Error en ApiService.sendData (${endpoint}):`, error);
            
            // Registrar error en el estado
            appState.addError('apiService', `Error en ${endpoint}: ${error.message}`);
            
            return {
                status: 'error',
                message: error.message
            };
        }
    }
    
    /**
     * Inicializa el estado desde los datos iniciales de la página
     * Método para facilitar la transición de window.initialData a AppState
     */
    static initializeFromWindowData() {
        try {
            if (typeof window !== 'undefined' && window.initialData) {
                console.log("ApiService - Inicializando estado desde window.initialData");
                appState.setInitialData(window.initialData);
                return true;
            }
            return false;
        } catch (error) {
            console.error("ApiService - Error al inicializar desde window.initialData:", error);
            appState.addError('apiService', error);
            return false;
        }
    }
}

// Inicializar el estado desde datos existentes en window si existen
if (typeof document !== 'undefined') {
    // Ejecutar cuando el DOM esté listo
    document.addEventListener('DOMContentLoaded', () => {
        ApiService.initializeFromWindowData();
    });
}

export default ApiService;