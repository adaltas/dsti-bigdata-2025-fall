# Lab 1: Unstructured data analysis with RDDs

Analyze unstructured data (text) with RDDs and Spark Core Functions.

## Goals

- Get familiar with the Hadoop and Spark environment
- Get familiar with the most frequently used functions for RDD processing: `map`, `flatMap`, `flatMapValues`, and `reduceByKey`
- Learn how to define lambda functions
- Learn when you can use pure Python functionalities and constructs in Spark environment

## Prerequisites

Prepare the input raw file to be used for the lab in the cluster. We have selected "Moby-Dick" as our target file, and will be performing a word count on it.

### Access the cluster through edge node

If you access the cluster with VPN, make sure the connection is active.

Connect to the edge node with SSH, get an active Kerberos ticket, and create a dedicated folder for the lab.

```bash
ssh <username>@<fqdn>
echo <password> | kinit
hdfs dfs -mkdir lab-spark-intro
```

### Put the file in HDFS

Once you are ready in the cluster. Download the "Moby Dick" content file and its output into your HDFS home directory. 

> Note, redirecting stdin into the put command is not documented.

```bash
hdfs dfs -help put
curl https://www.gutenberg.org/files/2701/2701-h/2701-h.htm | 
  hdfs dfs -put - lab-spark-intro/moby-dick.txt
hdfs dfs -cat lab-spark-intro/moby-dick.txt
```

### Spark development environment

The `pyspark` command provide a Python REPL environment useful for development. The  `spark-shell` command start the Spark Shell REPL for Scala developers. In this lab the `pyspark` REPL will be required to perform the following task.

```bash
pyspark
```

After the prerequisites, we are expecting to have access to the edge node, to have the "moby-dick.txt" in HDFS directory, and the `pyspark` shell is launched. And then we could move on to the following section.

## Loading HDFS content

First thing first, the raw file should be retrieved in the `pyspark` shell.

Use the `wholeTextFiles` to load the content of the "Moby Dick" file.

> Note: an available Spark Context is made available by the REPL with the `sc` variable. There is no need to initialize a new one.

```python
moby_dick = sc.wholeTextFiles('hdfs:///user/demo/lab-spark-intro/moby-dick.txt')
```

Check the status of partition: use `getNumPartitions` to get the number of partitions created in RDD.

```python
moby_dick.getNumPartitions()
```

Count the number of elements in the RDD. Why this outcome?

```python
moby_dick.count()
```

Get the first x elements of the RDD.

```python
moby_dick.take(x)
```
## Data cleansing

### Use lambda function to perform the data cleansing task

Before we dive into the cleansing job, let's first understand how Python lambda function works. Here is a simple example:

```python
times_2 = lambda x: x*2
test = lambda t: (t[0], t[1]*2)

print(times_2(2))
print(test( ("toto", 4) ))
```

Design lambda function to keep only the book's name and split the text by lines.

```python
content = moby_dick.map(lambda file_text: (
    file_text[0].split('/')[-1],
    file_text[1].split('\r\n')
))
```

There are a lot of '*' in the text, remove them.

```python
content_no_stars = content.map(lambda file_text: (
    file_text[0],
    [ l.replace('*', '') for l in file_text[1] ]
))
```

Overview of the content.

```python
content_no_stars.count()
len(content_no_stars.collect())
len(content_no_stars.collect()[0])
```

Create an element by line. 

Compare two functions: `flatMap` and `flatMapValues`. Do they return the same or different results?

```python
lines = content_no_stars.flatMap(lambda file_text: [(file_text[0], l) for l in file_text[1]])
lines.take(5)

lines_test = content_no_stars.flatMapValues(lambda lines: lines)
lines_test.take(5)
```

Now each line of the paragraph is obtained, split each line into strings (separated by ' '). 

Next, compare two functions: `flatMap` and `flatMapValues`. Do they return the same or different results for the string splitting task?

```python
strings = lines.flatMap(
    lambda file_text: [(file_text[0], s) for s in file_text[1].split(' ')]
)
strings.take(100)

strings_test = lines.flatMapValues(lambda line: line.split())
strings_test.take(100)
```

Remove the punctuation. A python library named `string` is required. A value of 1 will be assigned to each key-value pair for the mapping process.

```python
import string as stri

def remove_punctuation(content_string):
    book, text = content_string
    for p in stri.punctuation:
        text = text.replace(p, '')
    return (book, text, 1)

words = strings.map(remove_punctuation)
words.take(100)
```

Remove empty words.

```python
words_no_empty = words.filter(lambda words: words[1] != '')
words_no_empty.take(100)
```

## Counting words by using MapReduce process

```python
words_no_empty.countByKey()
```

Retrieve dictionary value using `item()` method.

```python
words_no_empty.countByKey().items()
```


## To-Do

Tasks:

1. Find the top 10 of the most used words in the whole book.

Advanced tasks:
1. Count number of words in each chapter.
2. Find the top 10 of the most used words by chapter.

## Resources

Spark docs:

- [Pyspark API reference doc](https://spark.apache.org/docs/latest/api/python/pyspark.html)
- [RDD Transformations](https://spark.apache.org/docs/latest/rdd-programming-guide.html#transformations)
