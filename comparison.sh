#!/usr/bin/env bash
#=================================================
# environment preparation
#=================================================
logfile='execution.log'
result_dir='results'
test_data_dir='test_data'

rm -f ${logfile}

if hash java 2>/dev/null; then
    echo "OK Java installed"
else
    echo "Error, java not installed"
    exit 1
fi

if hash python3 2>/dev/null; then
    echo "OK Python3 installed"
else
    echo "Error, python3 not installed"
    exit 1
fi

echo "checking if spmf.jar exists"
if [[ ! -e spmf.jar ]]; then
    echo "Downloading spmf.jar"
    wget http://www.philippe-fournier-viger.com/spmf/spmf.jar >> ${logfile}
fi

echo "checking python requirements"
if python3 -c "requirements.txt" &> /dev/null; then
    echo "Installing python requirements"
    python3 -m pip install -r requirements.txt >> ${logfile}
fi

rm -f ${result_dir}/*
mkdir -p ${result_dir}

#=================================================
# check input parameters
#=================================================
input_data="$@"
if [[ $# == 0 ]]; then
    echo "No input files specified, exiting"
    exit 1
fi
for i in ${input_data}; do
    if [[ ! -e ${test_data_dir}/${i} ]]; then
        echo "File ${i} does not exist in ${test_data_dir} directory"
        echo "Exiting"
        exit 1
    fi
done

#=================================================
# itemset generation
#=================================================
for i in ${input_data}; do
    echo "generating closed frequent itemsets in python for ${i} file"
    python3 charm.py -f ${test_data_dir}/${i} -s 0.5 --output ${result_dir}/python_out_${i} --spmf-format >> ${logfile}
    echo "generating closed frequent itemsets in java for ${i} file"
    java -jar spmf.jar run Charm_bitset ${test_data_dir}/${i} ${result_dir}/java_out_${i} 50% >> ${logfile}
done

#=================================================
# data comparison
#=================================================
echo "updating python results format"
sed -i 's/\[//g' ${result_dir}/python_out_*
sed -i 's/,//g' ${result_dir}/python_out_*
sed -i 's/]/  #SUP:/g' ${result_dir}/python_out_*
sed -i 's/\t/ /g' ${result_dir}/python_out_*

echo "Comparing algorithms output"
for i in ${input_data}; do
    sort -o ${result_dir}/python_out_${i} ${result_dir}/python_out_${i}
    sort -o ${result_dir}/java_out_${i} ${result_dir}/java_out_${i}
    if diff ${result_dir}/python_out_${i} ${result_dir}/java_out_${i} &> /dev/null ; then
        echo "OK Python and SPMF outputs match for ${i} input file"
    else
        echo "FAIL Python and SPMF outputs do not match for ${i} input file"
    fi
done
