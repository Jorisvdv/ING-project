# Possible Adjustments:
* [ ] Now we download all files, can we narrow that down to the selected simulation based on the name?  
* [ ] Introduce different types of errors
    1. [ ] Error where connection between servers is severed  
    2. [ ] Infinite loop  
    3. [ ] Connection break  
    4. [ ] A faulty patch, anomaly processed within 10 seconds at the place of 1 seconds after update.  
* [ ] Finalise plotly drop down selection  
* [ ] Add latency and kind servers to logs
    * [ ] Add latency to visualisation
    * [ ] Color network graph based on server kind
    * [ ] Add filtering on server kind to plotly
    * [ ] Take mean for all servers of a specific kind
* [ ] Add crash and restart when memory overload  
* [ ] Add timeout error (with appropriate logger level)  
* [ ] Add error introduction (with seperate logger (see Manual_Error_Log.csv))  
* [ ] Different routes for request type  
* [ ] Visual interface (see java modelling tool and Areana? for inspiration)

# Bugs:
* [ ] Simulation only prints out 21 lines of log (both from frontend and command line)  
* [x] Frontend fails if most recent file is not in correct format (fixed by filtering logs by filenames)
## relative paths
* OutlierDetection.py:  
    * [x] 15: OUT_DIR  
* Logger.py:  
    * [x] defaults: directory="logs"
* LogProcessing.py:  
    * [x] LOG_PATH = 'logs'  
    * [x] logs/Manual_Log_Filtered.csv  


# Defined variables/distributions/proposed changes:  
## lib folder  
* Envoirment.py: None  
* Logger.py:  
    * [x] defaults: directory="logs", level = 20 (20 is level INFO)  
* LogProcessing.py:
    * [x] LOG_PATH (change to relative to file)
    * [x] 172: add "latency" to metrics
* Middleware.py: None  
* MultiServers.py: None
    * [ ] 17: moving_average:  
     35: detect_outliers: n=3, default: 3 (maybe a bit small for this large amount of records)  
    * [ ] 68: outlier_writer: delimiter=',' (rest of csv have ";" delimiter)  
* Process.py:  
## main app2 folder  
* routes.py  
    * [ ] Abstract simulation to separate module  
    * [X] 181: wrong format log_filenames  
    * [X] 187: fixed filename seasonality, change to default  
    * [x] 187: make max_volume flexible  
    * [x] 224: Replace complicated most recent file search to more default functions  
    * [x] 272: Replace complicated most recent file search to more default functions  
    * [ ] 306: Only save files of selected simulation  
    * [ ] 315: name logs based on simulation run number  

## sample code:  
### first most recent file matchting a certain condition:  
```
import glob, os
list_of_files = glob.glob('log_*.csv')
latest_file = max(list_of_files, key=os.path.getctime))
```

### Set relative paths to script location  
```
file_dir = os.path.dirname(__file__)  
location_logs = os.path.join(file_dir, "Logs")  
```
