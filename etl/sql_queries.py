import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
IAM_ARN = config.get('IAM_ROLE', 'ARN')
CSSE_DATA = config.get('S3', 'CSSE_DATA')
OWID_DATA = config.get('S3', 'OWID_DATA')
GOOGLE_DATA = config.get('S3', 'GOOGLE_DATA')
ISO3166_1_DATA = config.get('S3', 'ISO3166_1_DATA')
ISO3166_2_DATA = config.get('S3', 'ISO3166_2_DATA')
FIPS_DATA = config.get('S3', 'FIPS_DATA')

# DROP TABLES
staging_covid_owid_table_drop = "DROP TABLE IF EXISTS staging_covid_owid;"
staging_covid_csse_table_drop = "DROP TABLE IF EXISTS staging_covid_csse;"
staging_mobility_table_drop = "DROP TABLE IF EXISTS staging_mobility;"
ref_iso3166_1_table_drop = "DROP TABLE IF EXISTS ref_iso3166_1;"
ref_iso3166_2_table_drop = "DROP TABLE IF EXISTS ref_iso3166_2;"
ref_fips_table_drop = "DROP TABLE IF EXISTS ref_fips;"
dim_date_table_drop = "DROP TABLE IF EXISTS dim_date;"
dim_country_table_drop = "DROP TABLE IF EXISTS dim_country;"
dim_region_table_drop = "DROP TABLE IF EXISTS dim_region;"
dim_subregion_table_drop = "DROP TABLE IF EXISTS dim_subregion;"
fact_covid_cases_table_drop = "DROP TABLE IF EXISTS fact_covid_cases;"
fact_covid_tests_table_drop = "DROP TABLE IF EXISTS fact_covid_tests;"
fact_covid_response_table_drop = "DROP TABLE IF EXISTS fact_covid_response;"
fact_mobility_measurements_table_drop = ("""DROP TABLE IF EXISTS
                                            fact_mobility_measurements;""")

# CREATE TABLES
staging_covid_owid_create = (
    """CREATE TABLE IF NOT EXISTS staging_covid_owid (
          iso_code varchar(10),
          continent varchar(100),
          location varchar(100),
          population integer,
          population_density float,
          date date,
          median_age float,
          total_tests integer,
          new_tests integer,
          new_tests_smoothed integer,
          tests_units varchar(100),
          stringency_index float);"""
          )

staging_covid_csse_create = (
    """CREATE TABLE IF NOT EXISTS staging_covid_csse (
          Active integer,
          Admin2 varchar(100),
          Confirmed integer,
          Country_Region varchar(100),
          Date date,
          Deaths integer,
          FIPS varchar(10),
          Lat float,
          Long_ float,
          Province_State varchar(100),
          Recovered integer);"""
          )

staging_mobility_create = (
    """CREATE TABLE IF NOT EXISTS staging_mobility (
          country_region_code varchar(2),
          country_region varchar(100),
          sub_region_1 varchar(100),
          sub_region_2 varchar(100),
          metro_area varchar(100),
          iso_3166_2_code varchar(10),
          census_fips_code varchar(10),
          date date,
          retail_and_recreation_percent_change_from_baseline integer,
          grocery_and_pharmacy_percent_change_from_baseline integer,
          parks_percent_change_from_baseline integer,
          transit_stations_percent_change_from_baseline integer,
          workplaces_percent_change_from_baseline integer,
          residential_percent_change_from_baseline integer);"""
          )

ref_iso3166_1_create = (
    """CREATE TABLE IF NOT EXISTS ref_iso3166_1 (
          English_short_name varchar(100),
          Alpha_2_code varchar(2),
          Alpha_3_code varchar(3),
          location_normalized varchar(100),
          latitude float,
          longitude float);"""
          )

ref_iso3166_2_create = (
    """CREATE TABLE IF NOT EXISTS ref_iso3166_2 (
          country_code varchar(2),
          subdivision_name varchar(100),
          code varchar(10),
          country_name varchar(100),
          combined_name varchar(256),
          location_normalized varchar(100),
          latitude float,
          longitude float,
          place_id varchar(30));"""
          )

ref_fips_create = (
    """CREATE TABLE IF NOT EXISTS ref_fips (
          Summary_Level varchar(3),
          State_Code varchar(2),
          County_Code varchar(5),
          County_Subdivision_Code varchar(5),
          Place_Code varchar(5),
          Consolidtated_City_Code varchar(5),
          Area_Name varchar(100));"""
          )

dim_date_create = (
    """CREATE TABLE IF NOT EXISTS dim_date (
          date date PRIMARY KEY,
          day integer NOT NULL,
          weekday integer NOT NULL,
          week integer NOT NULL,
          month integer NOT NULL,
          year integer NOT NULL);"""
          )

dim_country_create = (
    """CREATE TABLE IF NOT EXISTS dim_country (
          id varchar(3) PRIMARY KEY,
          name varchar(100) NOT NULL,
          continent varchar(30),
          latitude float,
          longitude float,
          population integer,
          population_density float,
          median_age float);"""
          )

dim_region_create = (
    """CREATE TABLE IF NOT EXISTS dim_region (
          id varchar(30) PRIMARY KEY,
          country_iso varchar(3) NOT NULL REFERENCES dim_country(id),
          name varchar(200) NOT NULL,
          latitude float,
          longitude float);"""
          )

dim_subregion_create = (
    """CREATE TABLE IF NOT EXISTS dim_subregion (
          id varchar(30) PRIMARY KEY,
          country_iso varchar(3) NOT NULL REFERENCES dim_country(id),
          region_id varchar(30) NOT NULL REFERENCES dim_region(id),
          name varchar(200) NOT NULL,
          latitude float,
          longitude float);"""
          )

fact_covid_cases_create = (
    """CREATE TABLE IF NOT EXISTS fact_covid_cases (
          id integer identity(0,1) PRIMARY KEY,
          date date NOT NULL REFERENCES dim_date(date),
          country_iso varchar(3) NOT NULL REFERENCES dim_country(id),
          region_id varchar(30) NOT NULL REFERENCES dim_region(id),
          subregion_id varchar(30) NOT NULL REFERENCES dim_subregion(id),
          cases_confirmed integer NOT NULL,
          cases_active integer NOT NULL,
          deaths integer NOT NULL,
          recovered integer NOT NULL);"""
          )

fact_covid_tests_create = (
    """CREATE TABLE IF NOT EXISTS fact_covid_tests (
          id integer identity(0,1) PRIMARY KEY,
          date date NOT NULL REFERENCES dim_date(date),
          country_iso varchar(3) NOT NULL REFERENCES dim_country(id),
          tests_total integer,
          tests_new integer,
          tests_new_smoothed integer,
          tests_unit varchar(30));"""
          )

fact_covid_response_create = (
    """CREATE TABLE IF NOT EXISTS fact_covid_response (
          id integer identity(0,1) PRIMARY KEY,
          date date NOT NULL REFERENCES dim_date(date),
          country_iso varchar(3) NOT NULL REFERENCES dim_country(id),
          stringency_index float NOT NULL);"""
          )

fact_mobility_measurements_create = (
    """CREATE TABLE IF NOT EXISTS fact_mobility_measurements (
          id integer identity(0,1) PRIMARY KEY,
          date date NOT NULL REFERENCES dim_date(date),
          country_iso varchar(3) NOT NULL REFERENCES dim_country(id),
          region_id varchar(30) NOT NULL REFERENCES dim_region(id),
          subregion_id varchar(30) NOT NULL REFERENCES dim_subregion(id),
          retail_recreation_change_baseline integer,
          grocery_pharmacy_change_baseline integer,
          parks_change_baseline integer,
          transit_stations_change_baseline integer,
          workplaces_change_baseline integer,
          residential_change_baseline integer);"""
          )

# STAGING TABLES COPY
staging_covid_owid_copy = (
    """COPY staging_covid_owid
       FROM {}
       IAM_ROLE {}
       JSON 'auto';"""
       ).format(OWID_DATA, IAM_ARN)

staging_covid_csse_copy = (
    """COPY staging_covid_csse
       FROM {}
       IAM_ROLE {}
       CSV
       IGNOREHEADER 1;"""
       ).format(CSSE_DATA, IAM_ARN)

staging_mobility_copy = (
    """COPY staging_mobility
       FROM {}
       IAM_ROLE {}
       CSV
       IGNOREHEADER 1;"""
       ).format(GOOGLE_DATA, IAM_ARN)

ref_iso3166_1_copy = (
    """COPY ref_iso3166_1
       FROM {}
       IAM_ROLE {}
       CSV
       IGNOREHEADER 1;"""
       ).format(ISO3166_1_DATA, IAM_ARN)

ref_iso3166_2_copy = (
    """COPY ref_iso3166_2
       FROM {}
       IAM_ROLE {}
       CSV
       IGNOREHEADER 1;"""
       ).format(ISO3166_2_DATA, IAM_ARN)

ref_fips_copy = (
    """COPY ref_fips
       FROM {}
       IAM_ROLE {}
       CSV
       IGNOREHEADER 1;""").format(FIPS_DATA, IAM_ARN)

# FINAL TABLES TRANSFORMATION
dim_date_table_insert = (
    """INSERT INTO dim_date (date, day, weekday, week, month, year)
          (SELECT DISTINCT
             date AS date,
             EXTRACT(day FROM date) AS day,
             EXTRACT(weekday FROM date) AS weekday,
             EXTRACT(week FROM date) AS week,
             EXTRACT(month FROM date) AS month,
             EXTRACT(year FROM date) AS year
           FROM staging_covid_owid);"""
           )

dim_country_table_insert = (
    """INSERT INTO dim_country (id, name, continent, latitude, longitude,
                                population, population_density, median_age)
          (SELECT DISTINCT
              r.Alpha_3_code AS id,
              r.location_normalized as name,
              o.continent as continent,
              r.latitude as latitude,
              r.longitude as longitude,
              o.population as population,
              o.population_density as population_density,
              o.median_age as median_age
           FROM staging_mobility s
           JOIN ref_ISO3166_1 r
           ON (s.country_region_code = r.Alpha_2_code)
           JOIN staging_covid_owid o
           ON (r.Alpha_3_code = o.iso_code));"""
           )

dim_region_table_iso_insert = (
    """INSERT INTO dim_region (id, country_iso, name, latitude, longitude)
          (SELECT DISTINCT
             rtwo.code AS id,
             rone.Alpha_3_code AS country_iso,
          	 rtwo.location_normalized AS name,
             rtwo.latitude as latitude,
             rtwo.longitude as longitude
          FROM staging_mobility s
          JOIN ref_ISO3166_1 rone
          ON (s.country_region_code = rone.Alpha_2_code)
          JOIN ref_ISO3166_2 rtwo
          ON (s.iso_3166_2_code = rtwo.code)
          WHERE SUBSTRING(rtwo.code, 1, 3) != 'US-');"""
          )

dim_region_table_fips_insert = (
    """INSERT INTO dim_region (id, country_iso, name, latitude, longitude)
          (SELECT DISTINCT
              rfips.State_Code AS id,
              riso.Alpha_3_code AS country_iso,
              rfips.Area_Name AS name,
              0.0 as latitude,
              0.0 as longitude
           FROM staging_mobility s
           JOIN ref_ISO3166_1 riso
           ON (s.country_region_code = riso.Alpha_2_code)
           JOIN ref_fips rfips
           ON (SUBSTRING(s.census_fips_code, 1, 2) = rfips.State_Code)
           WHERE rfips.County_Code = '000'
           AND rfips.County_Subdivision_Code = '00000'
           AND rfips.Place_Code = '00000'
           AND rfips.Consolidtated_City_Code = '00000');"""
          )

dim_subregion_table_insert = (
    """INSERT INTO dim_subregion (id, country_iso, region_id, name,
                                  latitude, longitude)
          (SELECT DISTINCT
              rfips.County_Code AS id,
              riso.Alpha_3_code AS country_iso,
              rfips.State_Code AS region_id,
              rfips.Area_Name AS name,
              0.0 as latitude,
              0.0 as longitude
           FROM staging_mobility s
           JOIN ref_ISO3166_1 riso
           ON (s.country_region_code = riso.Alpha_2_code)
           JOIN ref_fips rfips
           ON (s.census_fips_code = CONCAT(rfips.State_Code, rfips.County_Code))
           WHERE rfips.County_Code != '000'
           AND rfips.County_Subdivision_Code = '00000'
           AND rfips.Place_Code = '00000'
           AND rfips.Consolidtated_City_Code = '00000');"""
          )

fact_covid_tests_table_insert = (
    """INSERT INTO fact_covid_tests (date, country_iso, tests_total, tests_new,
                                     tests_new_smoothed, tests_unit)
          (SELECT
              o.date AS date,
              c.id AS country_iso,
              o.total_tests AS tests_total,
              o.new_tests AS tests_new,
              o.new_tests_smoothed AS tests_new_smoothed,
              o.tests_units AS tests_unit
           FROM staging_covid_owid o
           JOIN dim_country c
           ON (o.iso_code = c.id)
           JOIN dim_date d
           ON (o.date = d.date));"""
           )

fact_covid_response_table_insert = (
    """INSERT INTO fact_covid_response (date, country_iso, stringency_index)
          (SELECT
              o.date AS date,
              c.id AS country_iso,
              o.stringency_index AS stringency_index
           FROM staging_covid_owid o
           JOIN dim_country c
           ON (o.iso_code = c.id)
           JOIN dim_date d
           ON (o.date = d.date));"""
           )

fact_mobility_country_level_table_insert = (
    """INSERT INTO fact_mobility_measurements
       (date, country_iso, region_id, subregion_id,
        retail_recreation_change_baseline, grocery_pharmacy_change_baseline,
        parks_change_baseline, transit_stations_change_baseline,
        workplaces_change_baseline, residential_change_baseline)
          (SELECT
              m.date as date,
              iso.Alpha_3_code as country_iso,
              'No Region' AS region_id,
              'No Subregion' AS subregion_id,
              m.retail_and_recreation_percent_change_from_baseline
              AS retail_recreation_change_baseline,
              m.grocery_and_pharmacy_percent_change_from_baseline
              AS grocery_pharmacy_change_baseline,
              m.parks_percent_change_from_baseline
              AS parks_change_baseline,
              m.transit_stations_percent_change_from_baseline
              AS transit_stations_change_baseline,
              m.workplaces_percent_change_from_baseline
              AS workplaces_change_baseline,
              m.residential_percent_change_from_baseline
              AS residential_change_baseline
           FROM staging_mobility m
           JOIN ref_ISO3166_1 iso
           ON (m.country_region_code = iso.Alpha_2_code)
           JOIN dim_country c
           ON (iso.Alpha_3_code = c.id)
           JOIN dim_date d
           ON (m.date = d.date)
           WHERE m.iso_3166_2_code = '');"""
           )

fact_mobility_region_level_table_insert = (
    """INSERT INTO fact_mobility_measurements
       (date, country_iso, region_id, subregion_id,
        retail_recreation_change_baseline, grocery_pharmacy_change_baseline,
        parks_change_baseline, transit_stations_change_baseline,
        workplaces_change_baseline, residential_change_baseline)
          (SELECT
              m.date as date,
              iso.Alpha_3_code as country_iso,
              m.iso_3166_2_code AS region_id,
              'No Subregion' AS subregion_id,
              m.retail_and_recreation_percent_change_from_baseline
              AS retail_recreation_change_baseline,
              m.grocery_and_pharmacy_percent_change_from_baseline
              AS grocery_pharmacy_change_baseline,
              m.parks_percent_change_from_baseline
              AS parks_change_baseline,
              m.transit_stations_percent_change_from_baseline
              AS transit_stations_change_baseline,
              m.workplaces_percent_change_from_baseline
              AS workplaces_change_baseline,
              m.residential_percent_change_from_baseline
              AS residential_change_baseline
           FROM staging_mobility m
           JOIN ref_ISO3166_1 iso
           ON (m.country_region_code = iso.Alpha_2_code)
           JOIN dim_country c
           ON (iso.Alpha_3_code = c.id)
           JOIN dim_region r
           ON (r.id = m.iso_3166_2_code)
           JOIN dim_date d
           ON (m.date = d.date)
           WHERE SUBSTRING(m.iso_3166_2_code, 1, 3) != 'US-');"""
           )

fact_mobility_subregion_level_table_insert = (
    """INSERT INTO fact_mobility_measurements
       (date, country_iso, region_id, subregion_id,
        retail_recreation_change_baseline, grocery_pharmacy_change_baseline,
        parks_change_baseline, transit_stations_change_baseline,
        workplaces_change_baseline, residential_change_baseline)
          (SELECT
              m.date as date,
              sr.country_iso as country_iso,
              sr.region_id AS region_id,
              sr.id AS subregion_id,
              m.retail_and_recreation_percent_change_from_baseline
              AS retail_recreation_change_baseline,
              m.grocery_and_pharmacy_percent_change_from_baseline
              AS grocery_pharmacy_change_baseline,
              m.parks_percent_change_from_baseline
              AS parks_change_baseline,
              m.transit_stations_percent_change_from_baseline
              AS transit_stations_change_baseline,
              m.workplaces_percent_change_from_baseline
              AS workplaces_change_baseline,
              m.residential_percent_change_from_baseline
              AS residential_change_baseline
           FROM staging_mobility m
           JOIN dim_subregion sr
           ON (m.census_fips_code = CONCAT(sr.region_id, sr.id))
           JOIN dim_date d
           ON (m.date = d.date));"""
           )

fact_covid_cases_country_level_table_insert = (
    """INSERT INTO fact_covid_cases
       (date, country_iso, region_id, subregion_id, cases_confirmed,
        cases_active, deaths, recovered)
          (SELECT
              cov.Date as date,
              c.id as country_iso,
              'No Region' AS region_id,
              'No Subregion' AS subregion_id,
			  cov.Confirmed AS cases_confirmed,
              cov.Active AS cases_active,
              cov.Deaths AS deaths,
              cov.Recovered AS recovered
           FROM staging_covid_csse cov
           JOIN dim_country c
           ON (c.name = cov.Country_Region)
           JOIN dim_date d
           ON (cov.Date = d.date)
           WHERE cov.Province_State = '');"""
           )

fact_covid_cases_region_level_table_insert = (
    """INSERT INTO fact_covid_cases
       (date, country_iso, region_id, subregion_id, cases_confirmed,
        cases_active, deaths, recovered)
          (SELECT
              cov.Date as date,
              r.country_iso as country_iso,
              r.id AS region_id,
              'No Subregion' AS subregion_id,
			  cov.Confirmed AS cases_confirmed,
              cov.Active AS cases_active,
              cov.Deaths AS deaths,
              cov.Recovered AS recovered
           FROM staging_covid_csse cov
           JOIN dim_region r
           ON (r.name = cov.Province_State)
           JOIN dim_date d
           ON (cov.Date = d.date)
           WHERE cov.Country_Region != 'US');"""
           )

fact_covid_cases_subregion_level_table_insert = (
    """INSERT INTO fact_covid_cases
       (date, country_iso, region_id, subregion_id, cases_confirmed,
        cases_active, deaths, recovered)
          (SELECT
              cov.Date as date,
              r.country_iso as country_iso,
              r.region_id AS region_id,
              r.id AS subregion_id,
			  cov.Confirmed AS cases_confirmed,
              cov.Active AS cases_active,
              cov.Deaths AS deaths,
              cov.Recovered AS recovered
           FROM staging_covid_csse cov
           JOIN dim_subregion r
           ON (cov.FIPS = CONCAT(r.region_id, r.id))
           JOIN dim_date d
           ON (cov.Date = d.date));"""
           )

# QC QUERIES
count_staging_covid_owid = "SELECT COUNT(*) FROM staging_covid_owid;"
count_staging_covid_csse = "SELECT COUNT(*) FROM staging_covid_csse;"
count_staging_mobility = "SELECT COUNT(*) FROM staging_mobility;"
count_fact_covid_cases = "SELECT COUNT(*) FROM fact_covid_cases;"
count_fact_covid_tests = "SELECT COUNT(*) FROM fact_covid_tests;"
count_fact_covid_response = "SELECT COUNT(*) FROM fact_covid_response;"
count_fact_mobility_measurements = ("""SELECT COUNT(*) FROM
                                       fact_mobility_measurements;""")

# QUERY LISTS
create_table_queries = [
    {'q': staging_mobility_create,
     'desc': 'Create Table staging_mobility'},
    {'q': staging_covid_owid_create,
     'desc': 'Create Table staging_covid_owid'},
    {'q': staging_covid_csse_create,
     'desc': 'Create Table staging_covid_csse'},
    {'q': ref_iso3166_1_create,
     'desc': 'Create Table ref_ISO3166_1'},
    {'q': ref_iso3166_2_create,
     'desc': 'Create Table ref_ISO3166_2'},
    {'q': ref_fips_create,
     'desc': 'Create Table ref_fips'},
    {'q': dim_date_create,
     'desc': 'Create Table dim_date'},
    {'q': dim_country_create,
     'desc': 'Create Table dim_country'},
    {'q': dim_region_create,
     'desc': 'Create Table dim_region'},
    {'q': dim_subregion_create,
     'desc': 'Create Table dim_subregion'},
    {'q': fact_covid_cases_create,
     'desc': 'Create Table fact_covid_cases'},
    {'q': fact_covid_tests_create,
     'desc': 'Create Table fact_covid_tests'},
    {'q': fact_covid_response_create,
     'desc': 'Create Table fact_covid_response'},
    {'q': fact_mobility_measurements_create,
     'desc': 'Create Table fact_mobility_measurements'}
    ]

drop_table_queries = [staging_covid_owid_table_drop,
                      staging_covid_csse_table_drop,
                      staging_mobility_table_drop,
                      ref_iso3166_1_table_drop,
                      ref_iso3166_2_table_drop,
                      ref_fips_table_drop,
                      fact_covid_cases_table_drop,
                      fact_covid_tests_table_drop,
                      fact_covid_response_table_drop,
                      fact_mobility_measurements_table_drop,
                      dim_date_table_drop,
                      dim_subregion_table_drop,
                      dim_region_table_drop,
                      dim_country_table_drop]

drop_staging_only_table_queries = [staging_covid_owid_table_drop,
                                   staging_covid_csse_table_drop,
                                   staging_mobility_table_drop,
                                   ref_iso3166_1_table_drop,
                                   ref_iso3166_2_table_drop,
                                   ref_fips_table_drop]

copy_table_queries = [
    {'q': ref_iso3166_1_copy,
     'desc': 'Import ref_iso3166_1 data source'},
    {'q': ref_iso3166_2_copy,
     'desc': 'Import ref_iso3166_2 data source'},
    {'q': ref_fips_copy,
     'desc': 'Import ref_fips data source'},
    {'q': staging_mobility_copy,
     'desc': 'Import staging_mobility data source'},
    {'q': staging_covid_owid_copy,
     'desc': 'Import staging_covid_owid data source'},
    {'q': staging_covid_csse_copy,
     'desc': 'Import staging_covid_csse data source'}
    ]

insert_table_queries = [
    {'q': dim_date_table_insert,
     'desc': 'Insert dim_date data'},
    {'q': dim_country_table_insert,
     'desc': 'Insert dim_country data'},
    {'q': dim_region_table_iso_insert,
     'desc': 'Insert dim_region ISO reference data'},
    {'q': dim_region_table_fips_insert,
     'desc': 'Insert dim_region FIPS reference data'},
    {'q': dim_subregion_table_insert,
     'desc': 'Insert dim_subregion data'},
    {'q': fact_covid_cases_country_level_table_insert,
     'desc': 'Insert fact_covid_cases country data'},
    {'q': fact_covid_cases_region_level_table_insert,
     'desc': 'Insert fact_covid_cases region data'},
    {'q': fact_covid_cases_subregion_level_table_insert,
     'desc': 'Insert fact_covid_cases subregion data'},
    {'q': fact_covid_tests_table_insert,
     'desc': 'Insert fact_covid_tests data'},
    {'q': fact_covid_response_table_insert,
     'desc': 'Insert fact_covid_response data'},
    {'q': fact_mobility_country_level_table_insert,
     'desc': 'Insert fact_mobility_measurements country data'},
    {'q': fact_mobility_region_level_table_insert,
     'desc': 'Insert fact_mobility_measurements region data'},
    {'q': fact_mobility_subregion_level_table_insert,
     'desc': 'Insert fact_mobility_measurements data'}
    ]

qc_queries = [
    {'count_source': count_staging_covid_owid,
     'count_dest': count_fact_covid_tests,
     'desc': "Compare row count of staging_covid_owid and fact_covid_tests"},
    {'count_source': count_staging_covid_owid,
     'count_dest': count_fact_covid_response,
     'desc': "Compare row count of staging_covid_owid and fact_covid_response"},
    {'count_source': count_staging_covid_csse,
     'count_dest': count_fact_covid_cases,
     'desc': "Compare row count of staging_covid_csse and fact_covid_cases"},
    {'count_source': count_staging_mobility,
     'count_dest': count_fact_mobility_measurements,
     'desc': "Compare count of staging_mobility and fact_mobility_measurements"}
    ]
