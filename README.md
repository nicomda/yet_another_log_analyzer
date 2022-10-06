# Yet Another Log Analyzer
This tool analizes the content of log files, it has diferent operations to get usefull info. It takes a file/directory as input an processes    
it generating a json output file.

### PARAMETERS
| Parameter               | Description                                                                | Required |
|-------------------------|----------------------------------------------------------------------------|----------|
| -i INPUT, --input INPUT | Path to one plain-text file, or a directory. All .log files will be read                | Yes      |
| -h, --help              | show help message and exit                                                 | No       |
| --mfip                  | Get most frequent IP (default: False)                                      | No       |
| --lfip                  | Less frequent IP (default: False)                                          | No       |
| --eps                   | Events per second (default: False)                                         | No       |
| --bytes                 | Total amount of bytes exchanged (default: False)                           | No       |
| -o --output OUTPUT      | Path of the file where you want to store the output (default: output.json) | No       |