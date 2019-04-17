# Data Mining CHARM
This project provides the implementation of CHARM algorithm for mining closed frequent sets. Implementation based on the scientific paper: [**CHARM: An Efficient Algorithm for Closed Itemset Mining Mohammed** J. Zaki Ching-Jui Hsiao](https://pdfs.semanticscholar.org/fc59/bb528815efc84c2a08a3ad09f9ced8cc7508.pdf)

## Table of contents
* [General information](#General-information)
* [Setup](#Setup)  
* [Usage](#Usage)  
* [Implementation details](#Implementation-details)
* [Quality evaluation](#Quality-evaluation)
* [Performance evaluation](#Performance-evaluation)

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
The charm.py script contains two classes: **DataPreparation** and **CharmAlgorithm**.  
**DataPreparation** class has three methods:
* `import_data(self, filename)` - imports input data and writes it in a transactional form, as a list of tuples: {'tid': tid, 'item':    element}
* `transform_data(self)` - generates list of transactions for each element in the input data and writes to dataframe
* `get_frequent_items(self, min_sup)` - returns dataframe with all one-element itemsets with relative_support => min_sup  
**CharmAlgorithm** class contains implementation of the Charm algorithm. It has two main methods containing algorithm logic:
* `charm_extend(self, items_grouped)` - main algorithm responsible for finding closed itemsets, output is stored in `self.result` dataframe, the method considers each combination of itemset-transaction_id pairs appearing in **items_grouped** input dataframe and executes `charm_property()` method
* `charm_property(self, row1, row2, items, new_item, new_tid)` - applies one of the four properties on two given itemset-transaction_id-pairs, properties explained in the [paper](https://pdfs.semanticscholar.org/fc59/bb528815efc84c2a08a3ad09f9ced8cc7508.pdf) 
## Quality evaluation  
Corectness of the implementation is validated by comparing the output of charm.py script for [test_data](https://github.com/klepaczmikolaj/data-mining-Charm/tree/master/test_data) with output of **spmf data mining library** for the same test data. [spmf library for data mining](http://www.philippe-fournier-viger.com/spmf/index.php) is a java library specialized in pattern mining. It provides implementation of many data mining algorithms incuding the **Charm** algorithm which will be used in the output data comparison.  
`comparison.sh` is a dedicated shell script for charm.py script validation by comparing its output to spmf library output.  
The script requires Java 1.7 (necessary for spmf) and python 3.6 with requirements.txt installed.  
### Script usage
./comparison.sh [list of files from **test_data** directory for the comparison]  
If any specified file is not in test_data/ directory, the script terminates.  
```
chmod +x comparison.sh
./comparison.sh mushroom.txt retail.txt data1.txt
```
### Results for test data
charm.py script validation was conducted on all test files in [test_data](https://github.com/klepaczmikolaj/data-mining-Charm/tree/master/test_data) directory. Results from python script exactly match the results obtained from spmf library, which confirms the corectness of python implementation.  
*Part of script output for test data*
```
Comparing algorithms output
OK Python and SPMF outputs match for chess_trimmed.txt input file
OK Python and SPMF outputs match for contextPFPM.txt input file
OK Python and SPMF outputs match for data1.txt input file
OK Python and SPMF outputs match for retail.txt input file
OK Python and SPMF outputs match for chess_trimmed_more.txt input file
OK Python and SPMF outputs match for contextRelim.txt input file
OK Python and SPMF outputs match for mushroom.txt input file
OK Python and SPMF outputs match for tennis.txt input file
```

## Performance evaluation  
The execution time and closed itemsets statistics are redirected to **execution.log** file.  
The most significant difference in performance occurs when the number of found itemsets is considerably large, e.g for 3196 transactions and 2738 frequent itemsets, python implementation is 372 times slower, whereas for 88162 transactions and only one itemset found, python implementation is only 2 times slower than spmf.  

Performance results for different size of input files are presented below:  
```
File: test_data/chess_trimmed.txt
Python elapsed time: 90087 ms, Java elapsed time ~ 242 ms
Transactions count: 3196, Frequent closed itemsets count : 2738  
===================================================
File: test_data/contextPFPM.txt
Python elapsed time: 116 ms, Java elapsed time ~ 10 ms
Transactions count: 7, Frequent closed itemsets count : 4
===================================================
File: test_data/data1.txt
Python elapsed time: 201 ms, Java elapsed time ~ 15 ms
Transactions count: 6, Frequent closed itemsets count : 7
===================================================
File: test_data/retail.txt
Python elapsed time: 6947 ms, Java elapsed time ~ 3459 ms
Transactions count: 88162, Frequent closed itemsets count : 1
===================================================
File: test_data/chess_trimmed_more.txt
Python elapsed time: 3298 ms, Java elapsed time ~ 32 ms
Transactions count: 200, Frequent closed itemsets count : 107
===================================================
File: test_data/contextRelim.txt
Python elapsed time: 79 ms, Java elapsed time ~ 12 ms
Transactions count: 10, Frequent closed itemsets count : 3
===================================================
File: test_data/mushroom.txt
Python elapsed time: 2095 ms, Java elapsed time ~ 131 ms
Transactions count: 8124, Frequent closed itemsets count : 45
===================================================
File: test_data/tennis.txt
Python elapsed time: 103 ms, Java elapsed time ~ 7 ms
Transactions count: 14, Frequent closed itemsets count : 4
```

### todo
czas długość ilość wykresy, wielowątkowość algorytmu, możliwe podejścia, co wprowadzić żeby nie zepsuło jakości wynikówne 
