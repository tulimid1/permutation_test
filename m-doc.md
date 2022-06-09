---
layout: page
title: MATLAB
permalink: /MATLAB/
---

# [permutation_test](https://github.com/tulimid1/permutation_test/blob/main/permutation_test.m) 
---

Non-parametric permutation test to compare groups. See [Using_permutation_test.mlx](https://github.com/tulimid1/permutation_test/blob/main/Using_permutation_test.mlx) for a notebook of given examples. 

## Syntax
---
[pval = permutation_test(data1, data2)](#a)

[pval = permutation_test(data1, data2, Name, Value)](#b)

## Description
---
### A
[pval](#pval) = permutation_test([data1](#data1), [data2](#data2)) returns the p-value for a two-sided permutation test comparing mean between two independent samples. [example](#example-1)

### B
[pval](#pval) = permutation_test([data1](#data1), [data2](#data2), [Name, Value)](#name-value-arguments) returns the p-value for a permutation test with additional options specified by one or more name-value pair arguments. For example, you can do a one-sided test or compare medians instead of means. [example](#example-2)

## Examples 
---
### Example 1
Compare mean of two independent samples. This is equivalent to default `ttest2`. 

    mu1 = 0; sigma1 = 1; n1 = 20; 
    mu2 = 0.2; sigma2 = 1.3; n2 = 20; 
    groupA = normrnd(mu1, sigma1, [n1,1]);
    groupB = normrnd(mu2, sigma2, [n2,1]); 

    p = permutation_test(groupA, groupB)

p = 0.7318
    
### Example 2
Compute a one-sided independent difference of medians with parallel computing. 

    mu1 = 0; sigma1 = 1; n1 = 20; 
    mu2 = 0.2; sigma2 = 1.3; n2 = 20; 
    groupA = normrnd(mu1, sigma1, [n1,1]);
    groupB = normrnd(mu2, sigma2, [n2,1]); 

    p = permutation_test(groupA, groupB, 'alternative', 'less', 'test_fun', @median, 'parQuick', true)

p = 0.7897

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

Specified optional comma-separated pairs of ```Name,Value``` arguments. ```Name``` is the is the argument name and ```Value``` is the corresponding value. ```Name``` musta ppear inside single or double quotes. You can specify several name and value pair arguments in any order as ```Name1,Value1,...,NameN,ValueN```. 

**Example**: ```'name1', value1, 'name2', value2``` specifies blah blah blah.

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
Function for statistic to compare between groups (default=`@mean`)

Statistic to compute and compare permuted group values.  

Data Types: (function handle)

### ```parQuick```
Use parallel computation (default=`true`)

Whether or not to use parallel computation.  

Options: `false`, `true`

This will decrease overall computation time if one needs to do multiple permutation tests within a script. This function will create MATLAB workers and leave them running assuming you will reuse the workers. 

To manually shut-down workers, use the code `delete(gcp())`. 

Data Types: (boolean, scalar)

### ```bound```
Boundary for determining significance (default=`nan`)

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

This is a great function to use for analyses. This function supports one- and two-tailed tests. It can used in combination with [CLES]() to determine a non-parametric effect size of the difference. 

## Tips 
---

I would suggest adding both `permutation_test.m` and `functionSignatures.json` to a folder that is in your MATLAB path. The `permutation_test.m` contains the function and the `functionSignatures.json` will you give custom suggestions and code completion for when you call `permutation_test` in a script or notebook. 

If you already have a `functionSignatures.json` file in your folder, just add the pertinent code to the original `functionSignatures.json`. 

## Issues and Discussion
---

[Issues](https://github.com/tulimid1/permutation_test/issues) and [Discussion](https://github.com/tulimid1/permutation_test/discussions).

If you don't know how to use github (or don't want to), just send me an [email](mailto:tulimid@udel.edu). 
