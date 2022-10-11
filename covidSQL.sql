
-- Inspecting the data 
select*
from covid_deaths$

-- Inspecting the data 
select*
from covid_vaccination$

--data that is going to be used for further analysis
select location, date, population, total_cases,total_deaths, new_cases
from covid_deaths$

--PERCENT OF POPULATION INFECTED IN GHANA
select location, date, population, total_cases, round((total_cases/population)*100, 2) as populationInfected
from covid_deaths$
where location = 'Ghana'
order by 3,4 desc

--CASE FATALITY OF COVID IN GHANA
--the likelihood of dying if you contract covid in Ghana
select location, date, total_deaths, total_cases, round((total_deaths/total_cases)*100, 2) as casefatality_rate
from covid_deaths$
where location = 'Ghana'
order by 3,4 desc

--INCIDENT RATE IN GHANA
select location, date, new_cases, total_cases, round((new_cases/total_cases)*100, 2) as incidence_rate
from covid_deaths$
where location = 'Ghana'
order by date

--COUNTRIES WITH THE HIGHEST INFECTION RATE
select location, population, max(total_cases) as highestInfectionRate, round(max((total_cases/population))*100,2) as populationInfected
from covid_deaths$
where continent is not null
group by location, population
order by populationInfected desc

--COUNTRIES WITH THE HIGHEST DEATH RATE
select location,  max(cast(total_deaths as int)) as highestDeath
from covid_deaths$
where continent is not null
group by location
order by highestDeath desc

-- BREAKDOWN OF TOTAL DEATH BY CONTINENT
select location,  max(cast(total_deaths as int)) as highestDeath
from covid_deaths$
where continent is null and location not like '%income%'and location not like '%world%'
group by location
order by highestDeath desc 


--GLOBAL DATA infection rate
select  date,new_cases, population, round((convert(numeric,new_cases)/convert(numeric, population))* 100, 2) as incidentRate
from covid_deaths$
where location ='World' 
order by incidentRate

--GLOBAL DATA death Rate
-- The likelihood of dying if you contract covid globally
select  date,total_deaths, total_cases, round((total_deaths/total_cases)* 100, 2)  as deathRate
from covid_deaths$
where location = 'World'
order by deathRate desc

--CASE FATALITY BY CONTINENT
select location, max(cast(total_deaths as int))/max(cast(total_cases as numeric))*100 as casefatality_rate
from covid_deaths$
where continent is null and location not like '%income%'and location not like '%world%' and location not like '%tional%'
group by location
order by casefatality_rate desc 

------------------------------------------------- COVID VACCINATION TABLE----------------------------------------------------------------

--COVID VACCINATION TABLE 
select * 
from covid_vaccination$
order by 3,4 


--JOINNING THE TWO TABLES (ie covid_deaths and covid_vaccinations)

---CREATING A TEMPORARY TABLE TO ALLOW FOR THE USAGE OF THE NEWLY CREATED VARIABLE----

Drop table if exists #popvac

CREATE Table #popvac( 
continent varchar(50),
location  varchar(50),
population numeric,
date datetime,
new_vaccinations numeric, 
RollingTotalvac numeric)

INSERT INTO #popVac
select dea.continent ,dea.location,  convert(int,dea.population),  dea.date, vac.new_vaccinations,
SUM( convert(bigint, vac.new_vaccinations)) OVER (partition by dea.location Order by dea.date, dea.location) as RollingTotalvac
from covid_deaths$ dea --dea is an aliase
join covid_vaccination$ vac --vac is an aliase
	on dea.location= vac.location
	and dea.date=vac.date
where dea.continent is not null
order by 2,3
--- the temporary table has been created

select*, (RollingTotalvac/population)*100 as percentVac
from #popVac

CREATE Table popvac( 
continent varchar(50),
location  varchar(50),
population numeric,
date datetime,
new_vaccinations numeric, 
RollingTotalvac numeric,
RollingPercentVac numeric)

insert into popvac
select*, (RollingTotalvac/population)*100 as percentVac
from #popVac


----CRERATE A VIEW TO STORE DATA FOR FUTURE VISUALIZATION-----

Create View RollingTotalVac as 
select dea.continent ,dea.location,  convert(int,dea.population) as population,  dea.date, vac.new_vaccinations,
SUM( convert(bigint, vac.new_vaccinations)) OVER (partition by dea.location Order by dea.date, dea.location) as RollingTotalvac
from covid_deaths$ dea --dea is an aliase
join covid_vaccination$ vac --vac is an aliase
	on dea.location= vac.location
	and dea.date=vac.date
where dea.continent is not null

drop  VIEW IF exists RollingPercentVac
create view RollingPercentVac as 
select*,round((RollingTotalVac/convert(numeric,population))*100,4) as  percentRollingVac
from RollingTotalVac


select*
from RollingPercentVac


 

