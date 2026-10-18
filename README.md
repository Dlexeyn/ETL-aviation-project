Поле	Тип PostgreSQL	Назначение
incident_id	TEXT PRIMARY KEY	Уникальный идентификатор инцидента
date	DATE	Дата события
year	INTEGER	Год события
month	INTEGER	Месяц события
airline	TEXT	Название авиакомпании
airline_region	TEXT	Регион авиакомпании
airline_country	TEXT	Страна авиакомпании
aircraft_type	TEXT	Тип воздушного судна
aircraft_category	TEXT	Категория воздушного судна
manufacturer	TEXT	Производитель воздушного судна
aircraft_age_years	INTEGER	Возраст воздушного судна в годах
manufacture_year	INTEGER	Год выпуска воздушного судна
departure_airport	TEXT	Аэропорт отправления
arrival_airport	TEXT	Аэропорт прибытия
country	TEXT	Страна происшествия
region	TEXT	Регион происшествия
incident_type	TEXT	Тип авиационного инцидента
phase_of_flight	TEXT	Этап полёта
weather_conditions	TEXT	Погодные условия
primary_cause	TEXT	Основная причина инцидента
is_fatal	BOOLEAN	Признак наличия погибших
fatalities	INTEGER	Количество погибших
occupants_onboard	INTEGER	Количество находившихся на борту
injuries	INTEGER	Количество пострадавших
hull_loss	BOOLEAN	Признак полной потери воздушного судна
damage_category	TEXT	Категория повреждений
investigation_status	TEXT	Статус расследования
engines	INTEGER	Количество двигателей
seats_config	INTEGER	Количество мест согласно конфигурации

| Поле | Тип PostgreSQL | Назначение |
| :--- | :--- | :--- |
| incident_id | TEXT PRIMARY KEY | Уникальный идентификатор инцидента |
| date | DATE | Дата события |
| year | INTEGER | Год события |
| month | INTEGER | Месяц события |
| airline | TEXT | Название авиакомпании |
| airline_region | TEXT | Регион авиакомпании |
| airline_country | TEXT | Страна авиакомпании |
| aircraft_type | TEXT | Тип воздушного судна |
| aircraft_category | TEXT | Категория воздушного судна |
| manufacturer | TEXT | Производитель воздушного судна |
| aircraft_age_years | INTEGER | Возраст воздушного судна в годах |
| manufacture_year | INTEGER | Год выпуска воздушного судна |
| departure_airport | TEXT | Аэропорт отправления |
| arrival_airport | TEXT | Аэропорт прибытия |
| country | TEXT | Страна происшествия |
| region | TEXT | Регион происшествия |
| incident_type | TEXT | Тип авиационного инцидента |
| phase_of_flight | TEXT | Этап полёта |
| weather_conditions | TEXT | Погодные условия |
| primary_cause | TEXT | Основная причина инцидента |
| is_fatal | BOOLEAN | Признак наличия погибших |
| fatalities | INTEGER | Количество погибших |
| occupants_onboard | INTEGER | Количество находившихся на борту |
| injuries | INTEGER | Количество пострадавших |
| hull_loss | BOOLEAN | Признак полной потери воздушного судна |
| damage_category | TEXT | Категория повреждений |
| investigation_status | TEXT | Статус расследования |
| engines | INTEGER | Количество двигателей |
| seats_config | INTEGER | Количество мест согласно конфигурации |