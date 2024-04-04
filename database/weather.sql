USE weatherdata;

SELECT * FROM weather;
SELECT State,City,count(City)
FROM weather
GROUP BY State,City
