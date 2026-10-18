import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

INPUT_FILE = "/app/data/incidents.csv"
REJECTED_FILE = "/app/output/rejected_incidents.csv"

DB_CONFIG = {
    "dbname": os.getenv("PGDATABASE", "aviation_etl"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.environ["PGPASSWORD"],
    "host": os.getenv("PGHOST", "postgres"),
    "port": int(os.getenv("PGPORT", "5432")),
}


TEXT_COLUMNS = [
    "incident_id", "airline", "airline_region",
    "airline_country", "aircraft_type", "aircraft_category",
    "manufacturer", "departure_airport", "arrival_airport",
    "country", "region", "incident_type", "phase_of_flight",
    "weather_conditions", "primary_cause", "damage_category",
    "investigation_status",
]

INTEGER_COLUMNS = [
    "year", "month", "aircraft_age_years", "manufacture_year",
    "fatalities", "occupants_onboard", "injuries",
    "engines", "seats_config",
]

BOOLEAN_COLUMNS = ["is_fatal", "hull_loss"]

ALL_COLUMNS = [
    "incident_id", "date", "year", "month", "airline",
    "airline_region", "airline_country", "aircraft_type",
    "aircraft_category", "manufacturer", "aircraft_age_years",
    "manufacture_year", "departure_airport", "arrival_airport",
    "country", "region", "incident_type", "phase_of_flight",
    "weather_conditions", "primary_cause", "is_fatal",
    "fatalities", "occupants_onboard", "injuries", "hull_loss",
    "damage_category", "investigation_status", "engines",
    "seats_config",
]

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS incidents (
    incident_id TEXT PRIMARY KEY,
    date DATE NOT NULL,
    year INTEGER,
    month INTEGER,
    airline TEXT,
    airline_region TEXT,
    airline_country TEXT,
    aircraft_type TEXT,
    aircraft_category TEXT,
    manufacturer TEXT,
    aircraft_age_years INTEGER,
    manufacture_year INTEGER,
    departure_airport TEXT,
    arrival_airport TEXT,
    country TEXT,
    region TEXT,
    incident_type TEXT,
    phase_of_flight TEXT,
    weather_conditions TEXT,
    primary_cause TEXT,
    is_fatal BOOLEAN,
    fatalities INTEGER,
    occupants_onboard INTEGER,
    injuries INTEGER,
    hull_loss BOOLEAN,
    damage_category TEXT,
    investigation_status TEXT,
    engines INTEGER,
    seats_config INTEGER
);
"""


def extract():
    """Извлечение данных из CSV."""
    df = pd.read_csv(
        INPUT_FILE,
        sep=None,
        engine="python",
        dtype={"incident_id": "string"},
    )

    # Удаляем пробелы по краям текстовых значений.
    for column in TEXT_COLUMNS:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()
            df[column] = df[column].replace("", pd.NA)

    print(f"Extract: загружено строк: {len(df)}")
    return df


def transform(df):
    """Очистка, преобразование типов и валидация."""
    missing_columns = set(ALL_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"В CSV отсутствуют столбцы: {sorted(missing_columns)}"
        )

    df = df[ALL_COLUMNS].copy()

    # ГГГГ-ММ-ДД
    df["date"] = pd.to_datetime(
        df["date"],
        format="%Y-%m-%d",
        errors="coerce",
    )

    # Преобразование числовых значений.
    invalid_numeric = pd.Series(False, index=df.index)

    for column in INTEGER_COLUMNS:
        original = df[column]
        converted = pd.to_numeric(original, errors="coerce")

        invalid_numeric |= (
            original.notna() & converted.isna()
        )

        invalid_numeric |= (
            converted.notna()
            & (converted % 1 != 0)
        )

        df[column] = converted

    # 0/1 преобразуются в BOOLEAN; остальные значения отклоняются.
    invalid_boolean = pd.Series(False, index=df.index)

    for column in BOOLEAN_COLUMNS:
        original = df[column].astype("string").str.lower()
        mapping = {
            "1": True, "0": False,
            "true": True, "false": False,
        }

        converted = original.map(mapping)
        invalid_boolean |= original.notna() & converted.isna()
        df[column] = converted

    invalid = (
        df["incident_id"].isna()
        | df["incident_id"].eq("").fillna(True)
        | df["date"].isna()
        | invalid_numeric
        | invalid_boolean
    )

    # Идентификатор должен быть уникальным.
    invalid |= df["incident_id"].duplicated(keep="first")

    nonnegative_columns = [
        "aircraft_age_years", "fatalities", "occupants_onboard",
        "injuries", "engines", "seats_config",
    ]

    for column in nonnegative_columns:
        invalid |= df[column].notna() & (df[column] < 0)

    invalid |= df["month"].notna() & ~df["month"].between(1, 12)
    invalid |= df["is_fatal"].notna() & ~df["is_fatal"].isin([True, False])
    invalid |= (
        df["fatalities"].notna()
        & df["occupants_onboard"].notna()
        & (df["fatalities"] > df["occupants_onboard"])
    )

    # Год и месяц должны совпадать с датой события.
    invalid |= (
        df["year"].notna()
        & (df["year"] != df["date"].dt.year)
    )
    invalid |= (
        df["month"].notna()
        & (df["month"] != df["date"].dt.month)
    )

    rejected = df.loc[invalid].copy()
    clean = df.loc[~invalid].copy()

    if not rejected.empty:
        rejected.to_csv(REJECTED_FILE, index=False)

    clean["date"] = clean["date"].dt.date
    clean = clean.astype(object).where(pd.notna(clean), None)

    print(f"Transform: корректных строк: {len(clean)}")
    print(f"Transform: отклонено строк: {len(rejected)}")

    return clean


def load(df):
    """Загрузка данных в PostgreSQL одной транзакцией."""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)

            if not df.empty:
                rows = list(df[ALL_COLUMNS].itertuples(
                    index=False, name=None
                ))

                execute_values(
                    cur,
                    """
                    INSERT INTO incidents (
                        incident_id, date, year, month, airline,
                        airline_region, airline_country, aircraft_type,
                        aircraft_category, manufacturer, aircraft_age_years,
                        manufacture_year, departure_airport, arrival_airport,
                        country, region, incident_type, phase_of_flight,
                        weather_conditions, primary_cause, is_fatal,
                        fatalities, occupants_onboard, injuries, hull_loss,
                        damage_category, investigation_status, engines,
                        seats_config
                    ) VALUES %s
                    ON CONFLICT (incident_id) DO NOTHING
                    """,
                    rows,
                )

            cur.execute("SELECT COUNT(*) FROM incidents")
            total = cur.fetchone()[0]

    print(f"Load: всего записей в PostgreSQL: {total}")


def main():
    extracted = extract()
    transformed = transform(extracted)
    load(transformed)


if __name__ == "__main__":
    main()
