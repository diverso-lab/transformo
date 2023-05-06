USE wordpress;

ALTER TABLE `wp_comments` CHANGE `comment_date` `comment_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP, CHANGE `comment_date_gmt` `comment_date_gmt` DATETIME NULL DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE `wp_links` CHANGE `link_updated` `link_updated` DATETIME NULL DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE `wp_posts` CHANGE `post_date` `post_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP, CHANGE `post_date_gmt` `post_date_gmt` DATETIME NULL DEFAULT CURRENT_TIMESTAMP, CHANGE `post_modified` `post_modified` DATETIME NULL DEFAULT CURRENT_TIMESTAMP, CHANGE `post_modified_gmt` `post_modified_gmt` DATETIME NULL DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE `wp_users` CHANGE `user_registered` `user_registered` DATETIME NULL DEFAULT CURRENT_TIMESTAMP;


-- Elimina el procedimiento almacenado si ya existe
DROP PROCEDURE IF EXISTS truncate_all_tables;

-- Procedimiento almacenado para truncar todas las tablas en la base de datos excepto 'wp_options'
DELIMITER //
CREATE PROCEDURE truncate_all_tables()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE tableName CHAR(64);
    
    -- Cursor para obtener todas las tablas de la base de datos
    DECLARE cur CURSOR FOR
        SELECT t.TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES t
        WHERE t.TABLE_SCHEMA = DATABASE() AND t.TABLE_NAME != 'wp_options';
    
    -- Manejo del fin del cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    -- Abre el cursor
    OPEN cur;
    
    -- Bucle para recorrer todas las tablas
    read_loop: LOOP
        FETCH cur INTO tableName;
        
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Truncar la tabla actual
        SET @truncateSql = CONCAT('TRUNCATE TABLE `', tableName, '`;');
        PREPARE stmt FROM @truncateSql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END LOOP;
    
    -- Cierra el cursor
    CLOSE cur;
END//
DELIMITER ;

-- Ejecuta el procedimiento almacenado para truncar todas las tablas excepto 'wp_options'
CALL truncate_all_tables();

-- Elimina el procedimiento almacenado
DROP PROCEDURE truncate_all_tables;


DROP PROCEDURE IF EXISTS make_columns_nullable;

DELIMITER //
CREATE PROCEDURE make_columns_nullable()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE tableName CHAR(64);
    DECLARE columnName CHAR(64);
    DECLARE columnType CHAR(64);
    DECLARE isPrimaryKey BOOLEAN;
    DECLARE defaultValue TEXT;
    
    DECLARE cur CURSOR FOR
        SELECT t.TABLE_NAME, c.COLUMN_NAME, c.COLUMN_TYPE, c.COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.TABLES t
        JOIN INFORMATION_SCHEMA.COLUMNS c ON t.TABLE_NAME = c.TABLE_NAME
        WHERE t.TABLE_SCHEMA = DATABASE() AND c.DATA_TYPE != 'datetime';
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO tableName, columnName, columnType, defaultValue;
        
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET @checkPrimaryKeySql = CONCAT('SELECT IF(COUNT(*) > 0, TRUE, FALSE) INTO @isPrimaryKey FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = "', tableName, '" AND COLUMN_NAME = "', columnName, '" AND CONSTRAINT_NAME = "PRIMARY";');
        PREPARE stmt FROM @checkPrimaryKeySql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SELECT @isPrimaryKey INTO isPrimaryKey;
        
        -- Si la columna no es PRIMARY KEY, modificar la columna para permitir NULL
        IF NOT isPrimaryKey THEN
            IF defaultValue IS NOT NULL THEN
                SET @alterSql = CONCAT('ALTER TABLE `', tableName, '` MODIFY `', columnName, '` ', columnType, ' NULL DEFAULT ', QUOTE(defaultValue), ';');
            ELSE
                SET @alterSql = CONCAT('ALTER TABLE `', tableName, '` MODIFY `', columnName, '` ', columnType, ' NULL;');
            END IF;
            PREPARE stmt FROM @alterSql;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
        END IF;
    END LOOP;
    
    CLOSE cur;
END//
DELIMITER ;

CALL make_columns_nullable();

DROP PROCEDURE make_columns_nullable;



-- Elimina el procedimiento almacenado si ya existe
DROP PROCEDURE IF EXISTS remove_auto_increment;

-- Procedimiento almacenado para eliminar la propiedad AUTO_INCREMENT de todas las columnas PRIMARY KEY en todas las tablas, excepto 'umeta_id'
DELIMITER //
CREATE PROCEDURE remove_auto_increment()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE tableName CHAR(64);
    DECLARE columnName CHAR(64);
    DECLARE columnType CHAR(64);
    DECLARE dataType CHAR(64);
    DECLARE extra CHAR(64);
    
    -- Cursor para obtener todas las tablas y columnas de la base de datos
    DECLARE cur CURSOR FOR
        SELECT t.TABLE_NAME, c.COLUMN_NAME, c.COLUMN_TYPE, c.DATA_TYPE, c.EXTRA
        FROM INFORMATION_SCHEMA.TABLES t
        JOIN INFORMATION_SCHEMA.COLUMNS c ON t.TABLE_NAME = c.TABLE_NAME
        WHERE t.TABLE_SCHEMA = DATABASE() AND c.COLUMN_KEY = 'PRI' AND c.EXTRA = 'auto_increment';
    
    -- Manejo del fin del cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    -- Abre el cursor
    OPEN cur;
    
    -- Bucle para recorrer todas las tablas y columnas
    read_loop: LOOP
        FETCH cur INTO tableName, columnName, columnType, dataType, extra;
        
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Si la columna es PRIMARY KEY, tiene la propiedad AUTO_INCREMENT y su nombre no es 'umeta_id', eliminar la propiedad AUTO_INCREMENT
        IF extra = 'auto_increment' AND columnName != 'umeta_id' THEN
            SET @alterSql = CONCAT('ALTER TABLE `', tableName, '` MODIFY `', columnName, '` ', columnType, ' NOT NULL;');
            PREPARE stmt FROM @alterSql;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
        END IF;
    END LOOP;
    
    -- Cierra el cursor
    CLOSE cur;
END//
DELIMITER ;

-- Ejecuta el procedimiento almacenado para eliminar la propiedad AUTO_INCREMENT de todas las columnas PRIMARY KEY en todas las tablas, excepto 'umeta_id'
CALL remove_auto_increment();

-- Elimina el procedimiento almacenado
DROP PROCEDURE remove_auto_increment;

