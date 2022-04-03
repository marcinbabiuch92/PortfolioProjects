SELECT *
FROM Coronavirus_Portfolio..CovidDeaths$
ORDER BY 3,4

SELECT *
FROM Coronavirus_Portfolio..CovidVaccinations$
ORDER BY 3,4

--Select Data that we are going to be using

SELECT location, date, total_cases, new_cases, total_deaths, population
FROM Coronavirus_Portfolio..CovidDeaths$
ORDER BY 1, 2

-- Loking at Total Cases vs Total Deaths
-- Shows likelihood of dying if you contract covid in specific country

SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS DeathPercentage
FROM Coronavirus_Portfolio..CovidDeaths$
WHERE location = 'Poland'
ORDER BY 1, 2

--Looking at Total Cases vs Population

SELECT location, date, total_cases, population, (total_cases/population)*100 AS CasesPercentage
FROM Coronavirus_Portfolio..CovidDeaths$
WHERE location = 'Ukraine'
ORDER BY 1, 2

--Loking at countries with Highest Infection Rate compared to Population

SELECT location, population, MAX(total_cases) AS HightestInfectionCount, MAX((total_cases/population))*100 AS CasesPercentage
FROM Coronavirus_Portfolio..CovidDeaths$
GROUP BY location, population
ORDER BY 1, 2

-- Showing Countries with Highest Deadth Count per Population

SELECT Location, MAX(CAST(Total_deaths AS INT)) AS TotalDeathCount
FROM Coronavirus_Portfolio..CovidDeaths$
WHERE continent IS NOT NULL
GROUP BY Location
ORDER BY TotalDeathCount DESC

-- LET'S BREAK THINGS DOWN BY CONTINENT

SELECT continent, MAX(cast(Total_deaths as int)) as TotalDeathCount
FROM Coronavirus_Portfolio..CovidDeaths$
WHERE continent is not null
GROUP BY continent
ORDER BY TotalDeathCount DESC

-- GLOBAL NUMBERS

SELECT SUM(new_cases) AS total_cases, SUM(CAST(new_deaths AS INT)) AS total_deaths, SUM(CAST(new_deaths AS INT))/SUM(new_cases)*100 AS Death_Percentage
FROM Coronavirus_Portfolio..CovidDeaths$
WHERE continent is not null
--GROUP BY date
ORDER BY 1,2

-- Looking at Total Population vs Vaccination
SET ANSI_WARNINGS OFF

-- USE CTE
WITH PopVsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
AS
(
SELECT dea.continent, dea.location, dea.date, dea.population, 
vac.new_vaccinations, 
SUM(CONVERT(bigint, vac.new_vaccinations)) 
OVER (PARTITION BY dea.Location ORDER BY dea.Location, dea.date) 
AS RollingPeopleVaccinated
--(RollingPeopleVaccinated/population)*100
FROM Coronavirus_Portfolio..CovidDeaths$ dea
JOIN Coronavirus_Portfolio..CovidVaccinations$ vac
	ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent is not null
--ORDER by 2,3
)
SELECT *, (RollingPeopleVaccinated/Population)*100
FROM PopVsVac

-- TEMP TABLE

DROP TABLE if exists #PercentPopulationVaccinated -- thanks to that I can alter temp table
CREATE TABLE #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)

Insert into #PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, 
vac.new_vaccinations, 
SUM(CONVERT(bigint, vac.new_vaccinations)) 
OVER (PARTITION BY dea.Location ORDER BY dea.Location, dea.date) 
AS RollingPeopleVaccinated
--(RollingPeopleVaccinated/population)*100
FROM Coronavirus_Portfolio..CovidDeaths$ dea
JOIN Coronavirus_Portfolio..CovidVaccinations$ vac
	ON dea.location = vac.location AND dea.date = vac.date
--WHERE dea.continent is not null
--ORDER by 2,3


SELECT *, (RollingPeopleVaccinated/Population)*100
FROM #PercentPopulationVaccinated

-- Creating View to store data for later visualizations

Create View PercentPopulationVaccinated AS 
SELECT dea.continent, dea.location, dea.date, dea.population, 
vac.new_vaccinations, 
SUM(CONVERT(bigint, vac.new_vaccinations)) 
OVER (PARTITION BY dea.Location ORDER BY dea.Location, dea.date) 
AS RollingPeopleVaccinated
--(RollingPeopleVaccinated/population)*100
FROM Coronavirus_Portfolio..CovidDeaths$ dea
JOIN Coronavirus_Portfolio..CovidVaccinations$ vac
	ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent is not null
--ORDER by 2,3

SELECT *
FROM PercentPopulationVaccinated