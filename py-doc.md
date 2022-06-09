---
layout: page
title: Python
permalink: /Python/
---

# [permutation_test](https://github.com/tulimid1/permutation_test/blob/main/permutation_test/permutation_test.py)
---

Non-parametric permutation test to compare groups.. See [Using_permutation_test.ipynb](https://github.com/tulimid1/permutation_test/blob/main/Using_permutation_test.ipynb) for a notebook of given examples. 

## Syntax
---
    from permutation_test import permutation_test

[pval = permutation_test(data1, data2)](#a)

[pval = permutation_test(data1, data2, Name=Value)](#b)

## Description
---
### A
[pval](#pval) = permutation_test([data1](#data1), [data2](#data2)) returns the p-value for a two-sided permutation test comparing mean between two independent samples. [example](#example-1)

### B 
[pval](#pval) = permutation_test([data1](#data1), [data2](#data2), [Name=Value)](#name-value-arguments) returns the p-value for a permutation test with additional options specified by one or more name-value pair arguments. For example, you can do a one-sided test or compare medians instead of means. [example](#example-2)

## Examples 
---
### Example 1
Compare mean of two independent samples. This is equivalent to default `scipy.stats.ttest_ind`.  

    # create data 
    A = np.random.normal(0,1,[50,])
    B = np.random.normal(0,1,[50,])

    p = permutation_test(data1=A, data2=B, vis=True)

p = 0.5220

### Example 2 
Compute a one-sided independent difference of medians with parallel computing. 

    # create data 
    A = np.random.normal(0,1,[50,])
    B = np.random.normal(0,1,[50,])

    p = permutation_test(data1=A, data2=B, vis=True, parQuick=True)

p = 0.5217

## Input Arguments
---
### ```data1```
Group 1 data. 

Data vector for first group. 

Data Types: (numeric, vector)

### ```data2```
Group 2 data. 

Data vector for second group. 

Data Types: (numeric, vector)

### Name-Value Arguments

Specified optional pairs of ```Name=Value``` arguments. ```Name``` is the is the argument name and ```Value``` is the corresponding value. You can specify several name and value pair arguments in any order as ```Name1=Value1,...,NameN=ValueN```. 

**Example**: ```alternative='less'``` specifies a test that the group average of [data1](#data1) is less than the group average of [data2](#data2).

### ```paired```
Compute the paired difference (default=`false`)

Determine if algorithm should compute the paired difference. 

Options: `false`, `true`

Data Types: (boolean, scalar)

### ```alternative```
Alternative hypothesis (default='two-sided')

Alternative hypothesis for algorithm to use. 

Options: `two-sided`, `greater`, `less`

Data Types: (string/character, scalar)

### ```mu```
Population average (default=0)

Average to use for population if doing one-sample test. 

Data Types: (numeric, scalar)

### ```iterations```
Number of iterations to permute. (default=1000000)

Number of permutations to compute. The larger the number, the long the computation, but more stable the estimate. 

Data Types: (numeric, positive, integer, scalar)

### ```vis```
Visualize result (default=`false`)

Whether or not to visualize the histogram of group differences.

Options: `false`, `true`

Data Types: (boolean, scalar)

### ```test_fun```
Function for statistic to compare between groups (default=`numpy.mean`)

Statistic to compute and compare permuted group values.  

Data Types: (function handle)

### ```parQuick```
Use parallel computation (default=`false`)

Whether or not to use parallel computation via [numba](https://numba.pydata.org/).  

Options: `false`, `true`

This will decrease overall computation time drastically. Highly recommended. 

Data Types: (boolean, scalar)

### ```bound```
Boundary for determining significance (default=`None`)

Manually set boundary for comparison. 

Data Types: (numeric, scalar)

## Output
---

## ```pval```
p-value of permutation test. 

The probability of observing a test statistic as extreme, or more, than the observed value given the null hypothesis. 

Data Types: (numeric, scalar)

## More About 
---

This is a great function to use for analyses. This function supports one- and two-tailed tests. It can used in combination with [CLES](https://tulimid1.github.io/CLES/Python/) to determine a non-parametric effect size of the difference. 

## Tips 
---

Set [`parQuick`](#parquick) to true. It will speed up the code a lot. 

## Issues and Discussion 
---

[Issues](https://github.com/tulimid1/permutation_test/issues) and [Discussion](https://github.com/tulimid1/permutation_test/discussions).

If you don't know how to use github (or don't want to), just send me an [email](mailto:tulimid@udel.edu). 
