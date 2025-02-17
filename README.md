# WEATHER API
Weather API use to get weather data of a particular area or place. It can be any place where you live or any other city.
Here use [visualcrossing](https://www.visualcrossing.com/weather-api/) to fetch weather data. Also use [Redis](https://redis.io) as 
store data.

## UI
It have only a simple ui at '/main/' endpoint

## API
It have few endpoint to get weather data. 
For example: \

`/api/wr/[location]/` \
Above endpoint will give today's information.

`/hour/[location]/[date]?hour=00` \
Endpoint will get return a certain hour weather info of a particular place.

`/multiple/[location]/[date1]/[date2]` \
Above endpoint will return thoes days info.

This project creadted inspired by [roadmap.sh](https://roadmap.sh/projects/personal-blog)
