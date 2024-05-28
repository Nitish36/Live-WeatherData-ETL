USE weatherdata;

SELECT * FROM weather;
SELECT State,count(City)
FROM weather
GROUP BY State;

CREATE user 'weatherdata'@'localhost' identified by '$Freeman_007$';
Grant All on weatherdata.* to 'weatherdata'@'localhost';
flush privileges;
Show grants for 'weatherdata'@'localhost';
