-- NACIONALIDADES ------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS table_cube_nacionalidad (
                                                       nacionalidad_nombre VARCHAR(255),
                                                       fecha_visualizacion DATE,
                                                       tiempo_total DOUBLE PRECISION
);
-- -------------------------------- PROCEDURE NACIONALIDAD --------------------------------
/*
PARAMETROS
    N: Evalua los dias a evaluar
CONSTRAINTS
    En la capa de aplicacion debera de evaluar si es null o si tiene un valor
    en el caso de que sea null debera de colocar como defecto 7
*/
DROP PROCEDURE IF EXISTS actualizar_table_cube_nacionalidad;
CREATE PROCEDURE actualizar_table_cube_nacionalidad(n INTEGER)
    LANGUAGE plpgsql
AS $$
BEGIN
    -- Vaciar la tabla existente para actualizar los datos
    TRUNCATE table_cube_nacionalidad;

    -- Insertar los datos actualizados desde el cubo de nacionalidades
    INSERT INTO table_cube_nacionalidad (nacionalidad_nombre, fecha_visualizacion, tiempo_total)
    SELECT * FROM sp_nacionalidad_cube_n_dias(n);
END;
$$;
ALTER PROCEDURE actualizar_table_cube_nacionalidad(n INTEGER) OWNER TO postgres;
-- -------------------------------- PROCEDURE NACIONALIDAD --------------------------------
DROP PROCEDURE IF EXISTS vista_pastel_nacionalidad;
CREATE OR REPLACE PROCEDURE vista_pastel_nacionalidad()
    LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar si la vista existe y eliminarla antes de recrearla
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'view_pastel_nacionalidad') THEN
        DROP VIEW view_pastel_nacionalidad;
    END IF;

    -- Crear la vista para la visualización tipo pastel de nacionalidades
    CREATE VIEW view_pastel_nacionalidad AS
    WITH total_tiempo AS (
        SELECT SUM(n.tiempo_total) AS total
        FROM
            table_cube_nacionalidad n
                INNER JOIN
            "Nacionalidades_nacionalidad" nn ON n.nacionalidad_nombre = nn."nacTitulo_1"
                INNER JOIN
            "Nacionalidades_categoriasnacionalidades" c ON nn."catXnacNombre_id" = c.id
    )
    SELECT
        c."catXnacNombre" AS categoria, -- Categoría como eje X
        SUM(n.tiempo_total) AS eje_y, -- Tiempo total acumulado
        ROUND((SUM(n.tiempo_total)::numeric / tt.total::numeric) * 100, 2) AS porcentaje -- Porcentaje del total
    FROM
        table_cube_nacionalidad n
            INNER JOIN
        "Nacionalidades_nacionalidad" nn ON n.nacionalidad_nombre = nn."nacTitulo_1"
            INNER JOIN
        "Nacionalidades_categoriasnacionalidades" c ON nn."catXnacNombre_id" = c.id
            CROSS JOIN
        total_tiempo tt
    GROUP BY
        c."catXnacNombre", tt.total
    ORDER BY
        eje_y DESC;
END;
$$;
ALTER PROCEDURE vista_pastel_nacionalidad() OWNER TO postgres;
-- -------------------------------- PROCEDURE NACIONALIDAD --------------------------------

-- -------------------------------- FUNCTION NACIONALIDAD --------------------------------
/*
PARAMETROS
    modo_visualizacion: Evalua el tipo de inversion de dimensiones a trabajar
    k: Es el valor en Z a evaluar sobre las otras dos dimensiones
CONSTRAINTS
    En la capa de aplicacion debera de delimitar el tipo de modo_visualizacion y interpretarlo con 1 o 2
    En la capa de aplicacion debera de determinar el valor de k, sea valido segun el modo de visualizacion
*/
DROP FUNCTION visualizacion_bidimensional_dinamica_nacionalidad;
CREATE OR REPLACE FUNCTION visualizacion_bidimensional_dinamica_nacionalidad(
    modo_visualizacion INT,
    k TEXT
)
    RETURNS TABLE(
                     eje_x VARCHAR,
                     eje_y DOUBLE PRECISION
                 )
    LANGUAGE plpgsql
AS $$
BEGIN
    -- Modo 1: Filtro por fecha_visualizacion
    IF modo_visualizacion = 1 THEN
        RETURN QUERY
            SELECT
                nacionalidad_nombre::VARCHAR AS eje_x,
                tiempo_total AS eje_y
            FROM
                table_cube_nacionalidad
            WHERE
                fecha_visualizacion = k::DATE
            ORDER BY
                tiempo_total DESC;

        -- Modo 2: Filtro por nacionalidad_nombre
    ELSIF modo_visualizacion = 2 THEN
        RETURN QUERY
            SELECT
                fecha_visualizacion::VARCHAR AS eje_x,
                tiempo_total AS eje_y
            FROM
                table_cube_nacionalidad
            WHERE
                nacionalidad_nombre = k
            ORDER BY
                fecha_visualizacion;

        -- Si el modo es inválido
    ELSE
        RAISE EXCEPTION 'Modo de visualización inválido. Use 1 o 2.';
    END IF;
END;
$$;
ALTER FUNCTION visualizacion_bidimensional_dinamica_nacionalidad(modo_visualizacion INT, k TEXT) OWNER TO postgres;
-- -------------------------------- FUNCTION NACIONALIDAD --------------------------------
/*
PARAMETROS
    N: Evalua el total de dias a evaluar
*/
DROP FUNCTION sp_nacionalidad_cube_n_dias;
CREATE OR REPLACE FUNCTION sp_nacionalidad_cube_n_dias(n INTEGER)
    RETURNS TABLE(
                     nacionalidad_nombre VARCHAR(255),
                     fecha_visualizacion DATE,
                     tiempo_total DOUBLE PRECISION
                 )
    LANGUAGE plpgsql
AS $$
BEGIN
    -- Generamos el cubo de datos para nacionalidades, basado en los últimos n días
    RETURN QUERY
        WITH date_range AS (
            -- Generamos un rango de fechas desde la fecha máxima de visualización hasta los últimos n días
            SELECT GENERATE_SERIES(
                           (SELECT MAX(DATE(tv."fecha_visualizacion")) FROM public."Nacionalidades_tiempovisualizacion" tv) - INTERVAL '1 day' * (n - 1),
                           (SELECT MAX(DATE(tv."fecha_visualizacion")) FROM public."Nacionalidades_tiempovisualizacion" tv),
                           '1 day'::INTERVAL
                   )::DATE AS fecha
        )
        SELECT
            n."nacTitulo_1" AS nacionalidad_nombre,
            dr.fecha AS fecha_visualizacion,
            COALESCE(SUM(tv."tiempo_visualizado"), 0) AS tiempo_total
        FROM
            public."Nacionalidades_nacionalidad" n
                CROSS JOIN
            date_range dr -- Cross join para generar todas las combinaciones de fechas y nacionalidades
                LEFT JOIN
            public."Nacionalidades_tiempovisualizacion" tv
            ON
                n."nacCodigo" = tv."nacionalidad_id" AND DATE(tv."fecha_visualizacion") = dr.fecha
        GROUP BY
            n."nacTitulo_1", dr.fecha
        ORDER BY
            dr.fecha, n."nacTitulo_1";
END;
$$;
ALTER FUNCTION sp_nacionalidad_cube_n_dias(n INTEGER) OWNER TO postgres;
-- -------------------------------- FUNCTION NACIONALIDAD --------------------------------


-- TURISTICAS ------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS table_cube_turistica (
                                                    turistica_nombre VARCHAR(255),
                                                    fecha_visualizacion DATE,
                                                    tiempo_total DOUBLE PRECISION
);
-- -------------------------------- PROCEDURE TURISTICAS --------------------------------
DROP PROCEDURE actualizar_table_cube_turistica;
CREATE PROCEDURE actualizar_table_cube_turistica(n INTEGER)
    LANGUAGE plpgsql
AS $$
BEGIN
    -- Vaciar la tabla existente
    TRUNCATE table_cube_turistica;

    -- Insertar nuevos datos desde el cubo de datos
    INSERT INTO table_cube_turistica
    SELECT * FROM sp_turistica_cube_n_dias(n);
END;
$$;
ALTER PROCEDURE actualizar_table_cube_turistica(n INTEGER) OWNER TO postgres;
-- -------------------------------- PROCEDURE TURISTICAS --------------------------------
DROP PROCEDURE IF EXISTS vista_pastel_turistica;
CREATE PROCEDURE vista_pastel_turistica()
    LANGUAGE plpgsql
AS $$
BEGIN
    -- Eliminar la vista existente antes de recrearla
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'view_pastel_turistica') THEN
        DROP VIEW view_pastel_turistica;
    END IF;

    -- Crear la vista para la visualización tipo pastel agrupada por categoría con porcentajes
    CREATE VIEW view_pastel_turistica AS
    WITH total_tiempo AS (
        SELECT COALESCE(SUM(tc.tiempo_total), 0) AS total
        FROM table_cube_turistica tc
                 INNER JOIN "Turisticas_turistica" tur ON tc.turistica_nombre = tur."turTitulo_1"
                 INNER JOIN "Turisticas_categoriasturisticas" cat ON tur."catXturNombre_id" = cat.id
    )
    SELECT
        cat."catXturNombre" AS eje_x, -- Nombre de la categoría como eje X
        SUM(tc.tiempo_total) AS eje_y, -- Tiempo total acumulado
        CASE
            WHEN tot.total > 0 THEN ROUND((SUM(tc.tiempo_total)::numeric / tot.total::numeric) * 100, 2)
            ELSE 0 -- Asignar 0 si el total es cero
            END AS porcentaje -- Porcentaje del total
    FROM
        table_cube_turistica tc
            INNER JOIN
        "Turisticas_turistica" tur ON tc.turistica_nombre = tur."turTitulo_1"
            INNER JOIN
        "Turisticas_categoriasturisticas" cat ON tur."catXturNombre_id" = cat.id
            CROSS JOIN
        total_tiempo tot
    GROUP BY
        cat."catXturNombre", tot.total
    ORDER BY
        porcentaje DESC;
END;
$$;
ALTER PROCEDURE vista_pastel_turistica() OWNER TO postgres;
-- -------------------------------- PROCEDURE TURISTICAS --------------------------------

-- -------------------------------- FUNCTION TURISTICAS --------------------------------
DROP PROCEDURE visualizacion_bidimensional_dinamica_turistica;
CREATE OR REPLACE FUNCTION visualizacion_bidimensional_dinamica_turistica(
    modo_visualizacion INT,
    k TEXT
)
    RETURNS TABLE(
                     eje_x VARCHAR,
                     eje_y DOUBLE PRECISION
                 )
    LANGUAGE plpgsql
AS $$
BEGIN
    -- Modo 1: Filtro por fecha_visualizacion
    IF modo_visualizacion = 1 THEN
        RETURN QUERY
            SELECT
                turistica_nombre::VARCHAR AS eje_x,
                tiempo_total AS eje_y
            FROM
                table_cube_turistica
            WHERE
                fecha_visualizacion = k::DATE
            ORDER BY
                tiempo_total DESC;

        -- Modo 2: Filtro por turistica_nombre
    ELSIF modo_visualizacion = 2 THEN
        RETURN QUERY
            SELECT
                fecha_visualizacion::VARCHAR AS eje_x,
                tiempo_total AS eje_y
            FROM
                table_cube_turistica
            WHERE
                turistica_nombre = k
            ORDER BY
                fecha_visualizacion;

        -- Si el modo es inválido
    ELSE
        RAISE EXCEPTION 'Modo de visualización inválido. Use 1 o 2.';
    END IF;
END;
$$;
ALTER FUNCTION visualizacion_bidimensional_dinamica_turistica(modo_visualizacion INT, k TEXT) OWNER TO postgres;
-- -------------------------------- FUNCTION TURISTICAS --------------------------------
DROP FUNCTION sp_turistica_cube_n_dias;
CREATE OR REPLACE FUNCTION sp_turistica_cube_n_dias(n INTEGER)
    RETURNS TABLE(
                     turistica_nombre VARCHAR(255),
                     fecha_visualizacion DATE,
                     tiempo_total DOUBLE PRECISION
                 )
    LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
        WITH date_range AS (
            -- Generamos un rango de fechas desde hoy hasta los últimos n días
            SELECT GENERATE_SERIES(
                                   CURRENT_DATE - INTERVAL '1 day' * (n - 1),
                                   CURRENT_DATE,
                                   '1 day'::INTERVAL
                   )::DATE AS fecha
        )
        SELECT
            t."turTitulo_1" AS turistica_nombre,
            dr.fecha AS fecha_visualizacion,
            COALESCE(SUM(tv."tiempo_visualizado"), 0) AS tiempo_total
        FROM
            public."Turisticas_turistica" t
                CROSS JOIN
            date_range dr -- Generamos combinaciones de fechas y turísticas
                LEFT JOIN
            public."Turisticas_tiempovisualizacion" tv
            ON
                t."turCodigo" = tv."turistica_id" AND DATE(tv."fecha_visualizacion") = dr.fecha
        GROUP BY
            t."turTitulo_1", dr.fecha
        ORDER BY
            dr.fecha, t."turTitulo_1";
END;
$$;
ALTER FUNCTION sp_turistica_cube_n_dias(n INTEGER) OWNER TO postgres;
-- -------------------------------- FUNCTION TURISTICAS --------------------------------
