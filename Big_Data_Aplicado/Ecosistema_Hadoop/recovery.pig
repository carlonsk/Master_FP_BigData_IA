
-- Leemos el archivo flights.csv.
flights_data = LOAD '$flights_file' USING org.apache.pig.piggybank.storage.CSVExcelStorage(',', 'NO_MULTILINE', 'UNIX', 'SKIP_INPUT_HEADER')
       AS (dayofmonth:int, dayofweek:int, carrier:chararray, 
              depairportid:chararray, arrairportid:chararray, depdelay:int, arrdelay:int);

-- Filtramos de vuelos con salida retrasada y vuelos recuperados.
delayed_flights = FILTER flights_data BY depdelay > 15;
recovered_flights = FILTER flights_data BY depdelay > 15 AND arrdelay <= 15;

-- Agrupamos los vuelos con salida retrasada por compañía aérea.
grouped_delayed_flights = GROUP delayed_flights BY carrier;
delayed_count = FOREACH grouped_delayed_flights GENERATE
    group AS carrier,
    COUNT(delayed_flights) AS delayed_count;

-- Agrupamos los vuelos recuperados por compañía aérea.
grouped_recovered_flights = GROUP recovered_flights BY carrier;
recovered_count = FOREACH grouped_recovered_flights GENERATE
    group AS carrier,
    COUNT(recovered_flights) AS recovered_count;

-- Mostramos el esquema de las relaciones resultantes.
DESCRIBE grouped_delayed_flights;
DESCRIBE grouped_recovered_flights;

-- Unimos los conteos de vuelos con salida retrasada y vuelos recuperados.
joined_counts = JOIN delayed_count BY carrier, recovered_count BY carrier;

-- Cálculamos el porcentaje de vuelos recuperados.
percent_recovered = FOREACH joined_counts GENERATE
    delayed_count::carrier AS carrier,
    recovered_count / (float)delayed_count::delayed_count AS percent_recovered;

-- Ordenamos descendente por el porcentaje de vuelos recuperados.
ordered_flights = ORDER percent_recovered BY percent_recovered DESC;

-- Limitamos de resultados a los 5 primeros.
limited_flights = LIMIT ordered_flights 5;

-- Mostramos de los resultados finales.
DUMP limited_flights;
