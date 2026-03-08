-- Agregar columna usuario_id a las tablas de lotes si no existe
-- Para permitir gestión por usuario registrado

-- Engorde: Lote
ALTER TABLE api_lote ADD COLUMN usuario_id INT NULL;

-- Ponedoras: LotePonedora  
ALTER TABLE api_loteponedora ADD COLUMN usuario_id INT NULL;

-- Asignar un usuario por defecto (id=1) a los registros existentes
UPDATE api_lote SET usuario_id = 1 WHERE usuario_id IS NULL;
UPDATE api_loteponedora SET usuario_id = 1 WHERE usuario_id IS NULL;

-- Ahora hacer la columna NOT NULL (opcional, para producción)
-- ALTER TABLE api_lote MODIFY usuario_id INT NOT NULL;
-- ALTER TABLE api_loteponedora MODIFY usuario_id INT NOT NULL;
