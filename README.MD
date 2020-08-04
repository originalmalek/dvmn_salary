# Get average salary for programming engineer
The project print to terminal average salary for programming engineer vacancies. 


## Description
The code: 
The project print to terminal average salary for programing engineer vacancies from sites [Headhunter](https://hh.ru) and [Superjob](https://www.superjob.ru/).

* The project use:  
  * [Headhunter API](https://github.com/hhru/api);  
  * [SuperJob API](https://api.superjob.ru/doc/api2-public/).
  

## Requirements
Python >=3.7  
Register application on [SuperJob](https://api.superjob.ru/info/) ang get API key.  

Create file '.env' and add the code:
```
SUPERJOB_TOKEN = your_superjob_token
```

Install requirements modules:
```
pip install -r requirements.txt	
```


### How to use

Install requirements.  
Open and run 'main.py'.
```
python main.py	
```


## Additional information
You can change area(city, region) for searching vacancies.
Change variables in main() function:
```
area_hh = 1
area_sj = 4
```
Get more information:
 * [Headhunter API](https://github.com/hhru/api/blob/master/docs/areas.md);  
 * [SuperJob API](https://api.superjob.ru/#townlist).


## Project goal

The code was written for educational purpose on online course for Api developers [Devman](http://dvmn.org). 

