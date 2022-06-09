# Permutation testing

# import libraries
import numpy

def permutation_test(data1, data2=None, paired=False, alternative='two-sided', mu=0, iterations=1000000, vis=False, test_fun=numpy.mean, parQuick=False, bound=None):
    '''
    Permutation test (one and two-sample)

    INPUTS:
    data1/2: data vectors 
    optionals: 
    paired: paired test, true/false?, default=false 
    alternative: alternative hypothesis, two-sided, less, greater, default =
    'two-sided'
    mu: hypothesized population mean, deault=0
    iterations: # of iterations to run, default=100000
    vis: plot results, true/false? default=false
    test_fun: test function/statistic, mean, median, mode, etc, default = numpy.mean
    parQuick: turn on parallel pools do quickly, default = false
        good idea if going to do a lot of permutatoin tests simultaneously
    bound: meanually set value of interest, defeault = None

    OUTPUTs:
    p_val: p-value from permutation test 
    '''
    import numpy 
    import matplotlib
    matplotlib.pyplot.rcParams.update({'font.size': 16}) 
    import numba 

    # test function (default = mean)
    test_func = lambda x: test_fun(x)

    # assignment vector 
    assign1 = [0] * len(data1)
    if len(data2) == 0:
        assign2 = []
    elif len(data2) > 0: 
        assign2 = [1] * len(data2)
    assignment = numpy.concatenate((assign1, assign2))
    data = numpy.concatenate((data1, data2))

    # paired ?
    if paired:
        if len(data1) != len(data2):
            raise ValueError('Length of data vectors must be the same for paired permutation test')
        else :
            data = data2 - data1
            data -= numpy.mean(data)
    # one-sample 
    if len(data2) == 0:
        data = mu - data1
    
    # create local functions decorated for quick parallel computing 
    @numba.njit(parallel=True) 
    def one_or_paired_samp(D=data, its=iterations, t_f=numba.njit(test_func)):
        '''
        Main loop for one sample or paired sample permutations 
        
        INPUTS:
        D: data vector 
        its: # of iterations
        t_f: test function

        OUTPUT:
        t_diff: difference in groups 
        '''
        # pre-allcoate
        t_diff = numpy.empty(its)
        for i in numba.prange(its):
            # randomly sample with replacement
            rnd = numpy.random.choice(D, len(D), replace=True)

            # find the test function of data with new signs
            t_diff[i] = t_f(rnd)

        return t_diff

    @numba.njit(parallel=True) 
    def two_samp(D=data, A=assignment, its=iterations, t_f=numba.njit(test_func)):
        '''
        Main loop for one sample or paired sample permutations 
        
        INPUTS:
        D: data vector 
        A: assignment vector 
        its: # of iterations
        t_f: test function

        OUTPUT:
        t_diff: difference in groups 
        '''
        # pre-allcoate
        t_diff = numpy.empty(its)
        for i in numba.prange(its):
            # randomly assign new groups 
            assigned = numpy.random.permutation(A)

            # find the mean difference 
            t_diff[i] = t_f(D[assigned == 0]) - t_f(D[assigned == 1])

        return t_diff

    # iterate
    if parQuick and not paired and len(data2) > 0: 
        t_diff = two_samp()
    elif parQuick and (paired or len(data2) == 0):
        t_diff = one_or_paired_samp()
    elif not parQuick and not paired: 
        # pre-allcoate
        t_diff = numpy.empty(iterations)
        for i in range(iterations):
            # randomly assign new groups 
            assigned = numpy.random.permutation(assignment)
            # find the difference 
            t_diff[i] = test_fun(data[assigned == 0]) - test_fun(data[assigned == 1])
    elif (not parQuick and paired) or (not parQuick and len(data2) ==0): 
        # pre-allcoate
        t_diff = numpy.empty(iterations)
        for i in range(iterations):
            # randomly sample with replacement
            rnd = numpy.random.choice(data, len(data), replace=True)
            # find the test function of data with new signs
            t_diff[i] = test_fun(rnd)

    if paired:
        data_diff = numpy.mean(data1-data2)
    elif data2 is None:
        data_diff = numpy.mean(data1) #unsure
    else : 
        data_diff = test_fun(data[assignment==0]) - test_fun(data[assignment==1])
    
    # absolute data difference 
    if bound is None:
        abs_data_diff = numpy.abs(data_diff)
    else  :
        abs_data_diff = bound


    #     data_diff = numpy.mean(data1-data2)
    # elif len(data2) == 0:
    #     data_diff = mu
    # else : 
    #     data_diff = test_fun(data[assignment == 0]) - test_fun(data[assignment == 1])
    # abs_data_diff = numpy.abs(data_diff)
    
    # alternative hypothesis 
    if alternative=='two-sided':
        total = numpy.sum(t_diff <= -abs_data_diff) + numpy.sum(t_diff >= abs_data_diff)
    elif alternative=='greater':
        total = numpy.sum(t_diff >= data_diff)
    elif alternative=='less':
        total = numpy.sum(t_diff <= data_diff)
    
    # calculate p-value 
    p_val = total / iterations

    # visualize 
    if vis:
        matplotlib.pyplot.figure()
        matplotlib.pyplot.hist(t_diff)
        if alternative=='two-sided':
            matplotlib.pyplot.axvline(abs_data_diff, c='k', ls='--', lw=2)
            matplotlib.pyplot.axvline(-abs_data_diff, c='k', ls='--', lw=2)
        elif alternative=='greater': 
            matplotlib.pyplot.axvline(abs_data_diff, c='k', ls='--', lw=2)
        elif alternative=='less':
            matplotlib.pyplot.axvline(-abs_data_diff, c='k', ls='--', lw=2)
        matplotlib.pyplot.ylabel('Frequency')
        matplotlib.pyplot.xlabel('Test-statistic result')
        matplotlib.pyplot.title(f'p-val = {total:d} / {iterations:d} = {p_val:.4f}')

    return p_val 

