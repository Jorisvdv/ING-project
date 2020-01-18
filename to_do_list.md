# Possible Adjustments:
* [ ] Now we download all files, can we narrow that down to the selected simulation based on the name?  
* [ ] Introduce different types of errors
    1. [ ] Error where connection between servers is severed  
    2. [ ] Infinite loop  
    3. [ ] Connection break  
    4. [ ] A faulty patch, anomaly processed within 10 seconds at the place of 1 seconds after update.  
* [ ] Finalise plotly drop down selection  
* [ ] Add latency to logs and visualisation  
* [ ] Add crash and restart when memory overload  
* [ ] Add timeout error (with appropriate logger level)  
* [ ] Add error introduction (with seperate logger (see Manual_Error_Log.csv))  
* [ ] Different routes for request type  
* [ ] Visual interface (see java modelling tool for inspiration)  

# Bugs:
* [ ] Simulation only prints out 21 lines of log (both from frontend and command line)  
* [ ] Frontend fails if most recent file is not in correct format (reason moving Manual_Log_Filtered.csv and alteration file search method)
## relative paths
* OutlierDetection.py:  
    * [ ] 15: OUT_DIR  
* Logger.py:  
    * [ ] defaults: directory="logs"
* LogProcessing.py:  
    * [ ] LOG_PATH = 'logs'  
    * [ ] logs/Manual_Log_Filtered.csv  


# Defined variables/distributions/proposed changes:  
## lib folder  
* Envoirment.py: None  
* Logger.py:  
    * [ ] defaults: directory="logs", level = 20 (20 is level INFO)    
* Middleware.py: None  
* MultiServers.py: None
    * [ ] 17: moving_average:  
     35: detect_outliers: n=3, default: 3 (maybe a bit small for this large amount of records)  
    * [ ] 68: outlier_writer: delimiter=',' (rest of csv have ";" delimiter)  
* Process.py:  
## main app2 folder  
* routes.py  
    * [ ] Abstract simulation to separate module  
    * [ ] 181: wrong format log_filenames  
    * [ ] 187: fixed filename seasonality, change to default  
    * [ ] 187: make max_volume flexible  
    * [ ] 224: Replace complicated most recent file search to more default functions  
    * [ ] 272: Replace complicated most recent file search to more default functions  
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
