# Yet Another Log Analyzer
This tool analizes the content of log files, it has diferent operations to get usefull info. It takes a file/directory as input an processes    
it generating a json output file.

How to use it
======
### Standard Way
```bash
git clone https://github.com/nicomda/yet_another_log_analyzer.git 
cd yet_another_log_analyzer
chmod +x yet_another_log_analyzer.py
python3 yet_another_log_analyzer.py <PARAMETERS> 
```
### Docker Way
```bash
git clone https://github.com/nicomda/yet_another_log_analyzer.git 
cd yet_another_log_analyzer
docker build --tag yala . #Build docker image
docker run -it --name yala -v <HOST_INPUT_PATH>:/data yala <OPTIONAL_PARAMETERS> 
```
Parameters
======
| Parameter               | Description                                                                
|-------------------------|----------------------------------------------------------------------------
| -i INPUT, --input INPUT | Path to one plain-text file, or a directory. All .log files will be read    
| -h, --help              | show help message and exit                                                 
| --mfip                  | Add most frequent IP to output (default: False)                             
| --lfip                  | Add less frequent IP to output (default: False)                             
| --eps                   | Add events per second to output (default: False)                            
| --bytes                 | Add total amount of bytes exchanged (default: False)                        
| -o --output OUTPUT      | Path of the file where you want to store the output (default: output.json)

*All parameters are optional or they have a default value

How to test
======
Pytest is being used for testing purposes. To test the app, follow the steps below
```bash
cd test
pip3 install pytest==7.1.3 #Be sure that you have libraries added to PATH
pytest --verbose
```