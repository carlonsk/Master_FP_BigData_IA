
-- registramos la librería PiggyBank para poder usar la función de carga CSVExcelStorage.
REGISTER piggybank.jar

-- Leemos el fichero fligths.csv

FLIGHTS = LOAD '$flights_file' USING
       org.apache.pig.piggybank.storage.CSVExcelStorage(',', 'NO_MULTILINE', 'UNIX', 'SKIP_INPUT_HEADER')
       AS (dayofmonth:int, dayofweek:int, carrier:chararray, 
               depairportid:chararray, arrairportid:chararray, depdelay:int, arrdelay:int);

-- Filtramos las llegadas con retraso, seleccionando aquellos vuelos con un retraso en la llegada mayor a 15 minutos.
OPERATIONS = filter FLIGHTS by arrdelay > 15;

-- Agrupamos los vuelos filtrados por la compañía aérea.

TOTAL_OPERATIONS = GROUP OPERATIONS BY carrier;

-- Mostramos el esquema resultante.
DESCRIBE TOTAL_OPERATIONS;

-- Renombramos los campos y se cuenta el número de vuelos retrasados para cada compañía aérea.
TOTAL_OPERATIONS = FOREACH TOTAL_OPERATIONS GENERATE group AS carrier, COUNT(OPERATIONS) AS delayed_flights;

-- Ordenamos de forma descendente por vuelos
TOTAL_OPERATIONS = ORDER TOTAL_OPERATIONS BY delayed_flights DESC;

-- Limitamos a 5 aeropuertos
TOP5_TOTAL_OPERATIONS = LIMIT TOTAL_OPERATIONS 5;

-- Mostramos los resultados.
DUMP TOP5_TOTAL_OPERATIONS;
