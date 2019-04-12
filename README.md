# data mining Charm
Inplementation of CLOSET algorithm for mining closed frequent sets

## Table of contents
[Setup](#Setup)  
[Usage](#Usage)  
[Intro](#intro)

## Setup
The only requirement for the library is python3 with modules specified in requirements.txt file.  
Installation for linux:
```
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
sudo python3 -m pip install -r requirements.txt
```

## Usage
**Script usage**, also available in the help message: `python3 charm.py --help`
charm.py [-h] -f FILENAME -s SUPPORT [--output OUTPUT] [--spmf-format]

required arguments:  
  -f FILENAME, --filename FILENAME  Name of the file with data for itemset generation  
  -s SUPPORT, --support SUPPORT  Minimum support for frequent itemsets 

optional arguments:  
  -h, --help            show this help message and exit  
  --output OUTPUT       Output file name, default: output.txt  
  --spmf-format         Specify output file format as SPMF  

Example:
```
python3 charm.py -f test_data/contextPFPM.txt -s 0.5 --spmf-format --output out_file_PFPM.txt
```
<a name="intro"/>
## Intro
