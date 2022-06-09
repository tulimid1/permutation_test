function p_val = permutation_test(data1, data2, varargin)
%{

Permutation test one and two-sample

INPUTS:
data1/2: data vectors
varargin: 
paired: paired test, true/false?, default=false 
alternative: alternative hypothesis, two-sided, less, greater, default =
'two-sided'
mu: hypothesized population mean, default=0
iterations: # of iterations to run, default=1000000
vis: plot results, true/false? default=false
test_fun: test function/statistic, mean, median, mode, etc,default = @mean 
parQuick: turn on parallel pools do quickly, default = false
    good idea if going to do a lot of permutatoin tests simultaneously
bound: manually set value of interest

OUTPUTs:
p_val: p-value from permutation test 

%}

% arguments block 
arguments 
    data1 (1,:)
    data2 (1,:)
end
arguments (Repeating) 
    varargin
end

% parse inputs 
p = inputParser();
vectorNumbers = @(x) isnumeric(x) & isvector(x); 
scaleNum = @(x) isscalar(x) & isnumeric(x); 
addRequired(p, 'data1', vectorNumbers);
addRequired(p, 'data2', vectorNumbers);
addParameter(p, 'paired', false, @islogical); % not sure if this is right
addParameter(p, 'alternative', 'two-sided', @mustBeText);
addParameter(p, 'mu', 0, scaleNum); % not sure if this is right
addParameter(p, 'iterations', 1000000, scaleNum); 
addParameter(p, 'vis', false, @islogical); 
addParameter(p, 'test_fun', @mean, @(x) strcmpi(class(x), 'function_handle')); 
addParameter(p, 'parQuick', false, @islogical); 
addParameter(p, 'bound', nan, scaleNum); 
parse(p, data1, data2, varargin{:}); 

% assignment vector 
assign1 = zeros([length(data1), 1]);
if ~isempty(data2)
    assign2 = ones([length(data2), 1]); 
else
    assign2 = [];
end
assignment = [assign1; assign2];
data = [data1, data2]; 

% paired ?
if p.Results.paired 
    if length(data1) ~= length(data2)
        error('Length of data vectors must be the same for paired permutation test')
    else 
        data = data2 - data1; % paired difference 
        data = data - mean(data); % center 
    end
end

% one-sample ? 
if isempty(data2)
    data = p.Results.mu - data1;
end

% parallel computing or not 
workers = gcp('nocreate'); 
if p.Results.parQuick && isempty(workers)
    parpool(); 
    workers = gcp('nocreate'); 
end
if isempty(workers)
    numWorkers = 0; % will do for-loops
else
    numWorkers = workers.NumWorkers;  % will parallel compute 
end

% pre-allocations
t_diff = nan(1,p.Results.iterations);
parfor (i = 1:p.Results.iterations, numWorkers)
    if p.Results.paired || isempty(data2)
        % randomly sample indices
        rnd = randsample(length(data), length(data), true);
        % find test function of randomly sampled data 
        t_diff(i) = p.Results.test_fun(data(rnd)); 
    else
        % randomly assign new groups 
        rnd = assignment(randperm(length(assignment))); 
        % find the difference  
        t_diff(i) = p.Results.test_fun(data(rnd == 0)) - p.Results.test_fun(data(rnd == 1));
    end
end

if p.Results.paired
    data_diff = mean(data1-data2); 
elseif isempty(data2)
    data_diff = mean(data1); %????
else
    data_diff = p.Results.test_fun(data(assignment == 0)) - p.Results.test_fun(data(assignment == 1));
end
if isnan(p.Results.bound)
    abs_data_diff = abs(data_diff);
else % manually set bound 
    abs_data_diff = p.Results.bound;
end

if strcmpi(p.Results.alternative, 'two-sided')
    total = sum(t_diff <= -abs_data_diff) + sum(t_diff >= abs_data_diff);
elseif strcmpi(p.Results.alternative, 'greater')
    total = sum(t_diff >= data_diff);
elseif strcmpi(p.Results.alternative, 'less')
    total = sum(t_diff <= data_diff);
end

% find p 
p_val = total / p.Results.iterations; 

if p.Results.vis % visualize 
    figure();
    histogram(t_diff)
    hold on 
    if strcmpi(p.Results.alternative, 'two-sided')
        plot([abs_data_diff abs_data_diff], get(gca, 'ylim'), 'k--', 'linewidth', 2); 
        plot([-abs_data_diff -abs_data_diff], get(gca, 'ylim'), 'k--', 'linewidth', 2); 
    elseif strcmpi(p.Results.alternative, 'greater')
        plot([abs_data_diff abs_data_diff], get(gca, 'ylim'), 'k--', 'linewidth', 2); 
    elseif strcmpi(p.Results.alternative, 'less')
        plot([-abs_data_diff -abs_data_diff], get(gca, 'ylim'), 'k--', 'linewidth', 2); 
    end
    ylabel('Frequency'); xlabel('Test-statistic result')
    title(sprintf('p-val = %d / %d = %.5f', total, length(t_diff), p_val))
    set(gca, 'fontsize', 16); 
end

end