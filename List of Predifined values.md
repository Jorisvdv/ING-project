# Defined variables/distributions:

* Envoirment.py: None
* Logger.py:
    * [ ] defaults: directory="logs", level = 20 (20 is level INFO)
* LogProcessing.py:
    * [x] LOG_PATH = 'logs'
    * [ ] logs/Manual_Log_Filtered.csv
* Middleware.py: None
* MultiServers.py: None
* OutlierDetection.py:
    * [x] 15: OUT_DIR = 'logs/outliers/'
    * [ ] 17: moving_average: default: 3 (maybe a bit small for this large amount of records)
    * [ ] 35: detect_outliers: n=3, s=2, filename='outliers.csv'
    * [ ] 68: outlier_writer: delimiter=',' (rest of csv have ";" delimiter)
* Process.py: 


## sample code:
### first most recent file matchting a certain condition:
import glob, os
list_of_files = glob.glob('/path/to/folder/\*') # * means all if need specific format then \*.csv
latest_file = max(list_of_files, key=os.path.getctime)

### Set relative paths to script location
file_dir = os.path.dirname(__file__)
location_logs = os.path.join(file_dir, "Logs")
