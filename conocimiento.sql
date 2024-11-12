-- create database Conocimiento;

use Conocimiento;


-- Crear un nuevo usuario llamado 'nuevo_usuario' con la contraseña 'contraseña_segura'
CREATE USER 'admin'@'localhost' IDENTIFIED BY '1234';

-- Otorgar todos los privilegios CRUD sobre la base de datos 'mi_base_de_datos'
GRANT ALL PRIVILEGES ON Conocimiento.* TO 'admin'@'localhost';

-- Para ver los privilegios otorgados
SHOW GRANTS FOR 'admin'@'localhost';
-- drop database Conocimiento;

-- drop table objeto;
create table Enfermedad (
	Id_Enfermedad int primary key auto_increment ,
	Nombre varchar(90),
    Descripcion varchar(360),
    Imagen varchar(200) 
);

create table Sintomas (
	Id_Sintoma int primary key auto_increment ,
	Nombre varchar(90),
    Imagen varchar(200) 
);


CREATE TABLE Relacion (
	Id_Sintoma INT,
    Id_Enfermedad INT,
    Probabilidad INT,
	FOREIGN KEY (Id_Enfermedad) REFERENCES Enfermedad(Id_Enfermedad),
    FOREIGN KEY (Id_Sintoma) REFERENCES Sintomas(Id_Sintoma),
    UNIQUE (Id_Sintoma, Id_Enfermedad)
);

Drop table Relacion;

select * from Enfermedad;
select * from Sintomas;
select * from Relacion;

Alter table Enfermedad add column Bandera boolean;
Alter table Enfermedad add column Peso int;

show Tables;
update Enfermedad set Bandera=0 where Id_Enfermedad>=0;
update Enfermedad set Peso=0 where Id_Enfermedad>=0;

DELIMITER //

CREATE TRIGGER set_default_values_before_insert
BEFORE INSERT ON Enfermedad
FOR EACH ROW
BEGIN
    -- Establecer Bandera a 0
    SET NEW.Bandera = 0;

    -- Establecer Peso a 0
    SET NEW.Peso = 0;
END;
//

DELIMITER ;


DELIMITER //

CREATE TRIGGER suma_peso_enfermedad
AFTER INSERT ON Relacion
FOR EACH ROW
BEGIN
    -- Actualizar el Peso de la enfermedad sumando la probabilidad insertada
    UPDATE Enfermedad 
    SET Peso = Peso + NEW.Probabilidad
    WHERE Id_Enfermedad = NEW.Id_Enfermedad;
END;
//

DELIMITER ;




DELIMITER //

CREATE TRIGGER resta_peso_enfermedad
AFTER DELETE ON Relacion
FOR EACH ROW
BEGIN
    -- Actualizar el Peso de la enfermedad restando la probabilidad eliminada
    UPDATE Enfermedad 
    SET Peso = Peso - OLD.Probabilidad
    WHERE Id_Enfermedad = OLD.Id_Enfermedad;
END;
//

DELIMITER ;

select * from sintomas where Id_Sintoma>=50;

select Nombre from sintomas where Id_Sintoma>=0;

INSERT INTO sintomas(Nombre, Imagen) VALUES ('Sensibilidad a la luz', 'Imagenes\\Sintomas\\sin_imagen.jpg');

insert into sintomas(Nombre,Imagen)values('Dificultad para masticar','Imagenes\Sintomas\sin_imagen.jpg'); 


INSERT INTO sintomas(Nombre, Imagen) VALUES ('Entumecimiento', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Hipersensibilidad al frío', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Ruidos en las articulaciones', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Piel morada', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Infección en las uñas', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Pérdida del sentido del olfato', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Sabor metálico en la boca', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dolor de encías', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Sibilancias nocturnas', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dificultad para oír', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Cólicos menstruales', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Párpados hinchados', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Caída de las uñas', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Coloración amarillenta en los ojos', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dolor en la cadera', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dolor en la mandíbula', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Micción frecuente', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Incontinencia urinaria', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Pérdida del control del intestino', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Hinchazón de la lengua', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dolor en el talón', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dolor en los dedos de los pies', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Ronquidos', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Piel agrietada', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Presión en los oídos', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Cambios de humor', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Somnolencia', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Desorientación', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Aumento de la frecuencia cardíaca', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dolor en las muñecas', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dolor en los tobillos', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dolor de senos nasales', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Úlceras bucales', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Babeo excesivo', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Cicatrización anormal', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Moretones sin causa', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Debilidad en las manos', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Palidez extrema', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Escamas en el cuero cabelludo', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Falta de coordinación motora', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Respiración ruidosa', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Sensación de deshidratación', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Temblores en los párpados', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dificultad para mantener la postura', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Calor en las articulaciones', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Dolor lumbar nocturno', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Picores en el cuero cabelludo', 'Imagenes\\Sintomas\\sin_imagen.jpg');
INSERT INTO sintomas(Nombre, Imagen) VALUES ('Sensación de desmayo', 'Imagenes\\Sintomas\\sin_imagen.jpg');



select nombre from enfermedad where Id_Enfermedad>10;























-- Consultas
use Conocimiento;
Select * from Enfermedad where Id_Enfermedad>23;
select * from Relacion where Id_Enfermedad>23;
select * from sintomas;
alter table Relacion add column bandera boolean;
update relacion set bandera=0 where Id_Enfermedad >= 0;

