
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros_modbus`
--

CREATE TABLE `registros_modbus` (
  `ID` int(11) NOT NULL,
  `direccion_modbus` int(11) NOT NULL,
  `registro` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `rw` varchar(5) DEFAULT NULL,
  `acceso` varchar(20) DEFAULT NULL,
  `valor` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
