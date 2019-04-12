# Data Mining CHARM
This project provides the implementation of CHARM algorithm for mining closed frequent sets. Implementation based on the scientific paper: [**CHARM: An Efficient Algorithm for Closed Itemset Mining Mohammed** J. Zaki Ching-Jui Hsiao](https://pdfs.semanticscholar.org/fc59/bb528815efc84c2a08a3ad09f9ced8cc7508.pdf)

## Table of contents
* [General information](#General-information)
* [Setup](#Setup)  
* [Usage](#Usage)  
* [Implementation details](Implementation-details)
* [Quality evaluation](Quality-evaluation)
* [Performance evaluation](Performance-evaluation)

## General information
The algorithm itself is implemented in Python 3.6 using Numpy library for DataFrame operations. Main script **charm.py** provides the algorithm functionality which is getting closed frequent sets given the input set of transactions. The script expects two required command line arguments:
* **Filename**, which is name of the file with set of transactions for itemset mining.
* **Support**, which is the minimal relative support of the itemset to be taken into account in the result. For example, if the specified support is 0.5, only itemsets that occur in 50% or more transactions can be included in the result

See [Usage](#Usage) section for detailed script usage.  

### Input file
Input file should be a space separated set of transactions, each line corresponds to one transaction and each set of characters between spaces is considered as an item.  
Example input files: 
```
ab#$ ad cd asd
ad#$ we asd
ab#$ ad cd asd
ab#$ ad we asd
ab#$ ad we cd asd
ad#$ we cd
```
```
1 4 6
3 4 5
2 4
1 2 3 4
2 3
1 2 4
2 3 5 7
3 4 6
```
Example input files for the script are included in the [test_data](https://github.com/klepaczmikolaj/data-mining-Charm/tree/master/test_data) catalog. 

### Output
The output file, containing closed frequent itemsets can have two formats:
* **standard format**, which is a result of *to_csv()* method of result DataFrame in format: **Set_of_items**[\t]**Support**:
```
item    support
{'25', '34', '9', '1', '13', '21', '29', '7', '5', '36', '40', '27'}    114
{'25', '34', '21', '29', '7', '1', '5', '36', '27', '13'}       115
{'25', '34', '17', '9', '1', '11', '21', '29', '7', '15', '5', '36', '40', '27'}        101
{'25', '34', '17', '9', '1', '11', '21', '29', '15', '5', '36', '40', '27'}     102
```
* **spmf format**, which is similar to standard, but without column headers and with **sorted** list of items, it is especially useful during algorithm [quality evaluation](#Quality-evaluation) when comparing with java [spmf library for data mining](http://www.philippe-fournier-viger.com/spmf/index.php)
```
[1, 5, 7, 9, 13, 21, 25, 27, 29, 34, 36, 40]    114
[1, 5, 7, 13, 21, 25, 27, 29, 34, 36]   115
[1, 5, 7, 9, 11, 15, 17, 21, 25, 27, 29, 34, 36, 40]    101
[1, 5, 9, 11, 15, 17, 21, 25, 27, 29, 34, 36, 40]       102
```

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

## Implementation details  
Text here
## Quality evaluation  
Text here
## Performance evaluation  
Text here
