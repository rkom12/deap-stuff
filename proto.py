import ystockquote	# data fetch no jutsu
import ast	# autovivification - perl stlye no jutsu
import pandas	# dates and stuff
import operator
import math
import random
import numpy


from deap import algorithms
from deap import base	# hardcore evolutionary operators and a virtual Fitness class (different from the creator.create(fitness object)
from deap import creator	# creates classes of our own liking (here's how we modify our GAs)
from deap import tools	# operators dealing with individuals - crossover,mutation etc - also,some of the functions here are actually from the 'gp' module
from deap import gp	# tree building and function evaluating

# ********************************************************************************************************************************************
class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


#a = AutoVivification()
#a = ystockquote.get_historical_prices('MSFT','2016-08-08','2016-08-12')
#print a
#b = ast.literal_eval(a['2016-08-07']['High'])
#b = b+100
#print b

ticker = 'GOOG'

past_data = AutoVivification()
past_data = ystockquote.get_historical_prices(ticker,'2016-07-05','2016-09-01')	# take dates from july to september



weekdays = pandas.Series(pandas.bdate_range('20160705 09:10:12', periods=41))	# only weekdays from july to september
dates = weekdays.dt.strftime('%Y-%m-%d')

p = 41	# run the loop for 40 days as periods = 41
i = 0

open_val = []
close_val = []
low_val = []
high_val = []
volume_val = []



while i<(p-1):
    open_val.append(ast.literal_eval(past_data[dates[i]]['Open']))
    close_val.append(ast.literal_eval(past_data[dates[i]]['Close']))
    low_val.append(ast.literal_eval(past_data[dates[i]]['Low']))
    high_val.append(ast.literal_eval(past_data[dates[i]]['High']))
    volume_val.append(ast.literal_eval(past_data[dates[i]]['Volume']))
    i = i + 1

close_val.append(ast.literal_eval(past_data[dates[i]]['Close']))	# last day check


rsi_n = 40
rsi_i = 0
avg_gain = 0
avg_loss = 0

while (rsi_i < rsi_n):
    change = close_val[rsi_i + 1] - close_val[rsi_i]
    if (change < 0):
        avg_loss = avg_loss + change
    else:
        avg_gain = avg_gain + change
    rsi_i = rsi_i + 1

avg_gain = avg_gain / 40
avg_loss = abs(avg_loss)
avg_loss = avg_loss / 40

rs = avg_gain / avg_loss
rsi = (100 - (100 / (1 + rs)))

print '\n'
print 'The 40-point RSI value is ->'
print rsi
print '\n'
print '\n'

if (rsi >= 70):
    print 'Overbought -> sell it !'
elif (rsi <= 30):
    print 'Oversold -> buy it !'
else:
    print 'Hold on folks - just stick to the stock !'

print '\n'
print '\n'


#--------------------------------------------------------------------------------------------- MP - Modification Points for various approaches
# Define new functions - we can have our own function / terminal sets here --------------------------------------------------------------- MP1

def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

# the arity below gives the number of inputs - ARG0,ARG1,ARG2,.... ------------------------------------------------------------------------MP2
pset = gp.PrimitiveSet("MAIN", 5)	#class deap.gp.PrimitiveSet(name, arity, prefix='ARG') - also pset here is global set
pset.addPrimitive(operator.add, 2)	# addPrimitive only adds to the function set
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)	# addTerminal - requires only terminals to be added
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))	# here its gonna be -1,0,+1 - we can have our own constants ------ MP3

pset.renameArguments(ARG0='open')
pset.renameArguments(ARG1='close')
pset.renameArguments(ARG2='low')
pset.renameArguments(ARG3='high')
pset.renameArguments(ARG4='volume')



# ********************************************************************************************************************************************

# Essentially, creator.create transforms this ->
#class Foo(list):
#    spam = 1
#
#   def __init__(self):
#        self.bar = dict() # bar is initialized as an empty dictionary


# into this ->


#create("Foo", list, bar=dict, spam=1)


#  deap.creator.create(name, base[, attribute[, ...]]) - where base is the parent class whose attributes are inherited
# here a fitness object and an individual object are created ----------------------------------------------------------------------------- MP4
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))	# weighted maximization/minimization of objectives ----------------------- MP5
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)	# any individual object now created will have these attributes
# here the individual is a PrimitiveTree - but it could be anything - a list,dict etc..





# ********************************************************************************************************************************************


toolbox = base.Toolbox()	# 'registering' many other functions of our choice in the toolbox


#Essentially, the register function converts this ->
#>>> def func(a, b, c=3):
#...     print a, b, c

# to this ->

#>>> tools = Toolbox()
#>>> tools.register("myFunc", func, 2, c=4)
#>>> tools.myFunc(3)
#2 3 4

#register(alias, method[, argument[, ...]]) - the syntax of register

# 'expr','individual','population','compile' etc. are registered in toolbox - KEEP IN MIND THAT THEY ARE NEWLY ADDED FUNCTIONS

# gneHalfandHalf - combination of genGrow() & genFull() -----------------------------------------------------------------------------------MP6
# deap.gp.genHalfAndHalf(pset, min_, max_, type_=None) ,where
# pset is the primitive set
# min_ is the minimum height of tree
# max_ is the maximum height of tree
# type (optional) is return type of tree
# the above stuff returns a full grown tree - dayum !
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)	# now think of expr as a newly added function




# deap.tools.initIterate(container, generator)
# where , container is the type of the data from func(see func below)
# generator is a function returning an iterable (list, tuple, ...) - the content of this iterable will fill the container.
# the above stuff returns an instance of the container filled with data from the generator
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)	# halfandhalf trees are put into Individuals




# deap.tools.initRepeat(container, func, n)
# where, container - the type to put in the data from func
# func is the function that will be called 'n' times to fill up the container
# n is number of times to call func - it could be understood as the size of an individual
# the above stuff returns an instance of the container filled with data from func
toolbox.register("population", tools.initRepeat, list, toolbox.individual)	# a population of individuals is created - notice how 'individual' function is used to generate the population - the population is put inside a list(i.e. the container)

# from 'expr' we made an 'individual' which we replicated to make a 'population',which is stored in a list


toolbox.register("compile", gp.compile, pset=pset) # deap.gp.compile(expr, pset) - compiles expr and RETURNS a function which we've named 'compile'

# the above lines specify how to create an individual and how to create the population --------------------------------------------------- MP7







def evalSymbReg(individual):	# receives an individual as an input and returns CORRESPONDING fitness --------------------------- MP8
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)	# our above registered functions are being used


#	For our stock project,

#	run this func on an input-output pair and then measure the sqerror
#	Math.abs(func(x_i,y_i,z_i,p_i,q_i,r_i) - output for that input) -> sqerror
#	above line will be run for all input-output pairs (in a loop) - the summation of sqerrors will be calculated and returned as the final fitness

    # Evaluate the mean squared error between the expression
    # and the real function : x**4 + x**3 + x**2 + x

    #abs_errors = ((func(Open,Close,Low,High,Volume) - close_9)+(func(Open,Close,Low,High,Volume) - close_10)+(func(Open,Close,Low,High,Volume) - close_11))

    abs_error = 0

    j = 40
    k = 0

    while k<j:
        error = abs(func(open_val[k],close_val[k],low_val[k],high_val[k],volume_val[k]) - close_val[k+1])
        k = k + 1
        abs_error = abs_error + error

    #abs_errors = ((func(o,c,l,h,v)-close_9)+(func(o,c,l,h,v)-close_10)+(func(o,c,l,h,v)-close_11))
    #sqerrors = ((func(x) - x**4 - x**3 - x**2 - x)**2 for x in points)
    #return math.fsum(sqerrors) / len(points),	# the evaluation function ALWAYS returns a tuple,hence the comma
    return abs_error,


toolbox.register("evaluate",evalSymbReg)	# x from -1 to +1 will be sent as points to make up the (expected-obtained) function evaluations


# deap.tools.selTournament(individuals, k, tournsize)
# where.
# individuals is list of individuals to select from
# k is the number of individuals to select
# tournsize is the number of individuals participating in each tournament
# the above stuff returns the list of selected individuals ------------------------------------------------------------------------------ MP9
toolbox.register("select", tools.selTournament, tournsize=3)


# heavy modification is possible in the lines below ------------------------------------------------------------------------------------ MP10

toolbox.register("mate", gp.cxOnePoint)	# returns a tuple of 2 trees

toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)	# generates an expression where each leaf has same depth between min and max
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset) # mutates subtree with 'expr_mut'


# decorate is a wrapper which makes sure stuff is within constraints - here we've made sure that the length of individuals is <= 17
# remember - the tree's level should not go higher than 90 - that is Python's 'call stack depth' limit
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))	# Koza thinks that 17 is optimal tree depth value
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))	# this is to control bloat



# ********************************************************************************************************************************************


def main():
    random.seed(318)	# giving the PRG it's previous value (XOR-style)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)	# the HallOfFame stores only 1 individual - if it stored many,the one at 0th index would be the very best

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)


# the below algo takes a population as an input and returns an optimized population and a logbook
    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 144, stats=mstats,
                                   halloffame=hof, verbose=True)	# heavy modification possible again ---------------------------- MP11

# deap.algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen[, stats, halloffame, verbose])
# where,

# population is a list of individuals
# toolbox is the Toolbox that contains the evolution operators
# cxpb is the probability of mating two individuals
# mutpb is the probability of mutating an individual
# ngen is the the number of generation
# stats is a Statistics object that is updated inplace (optional)
# halloffame is a HallOfFame object that will contain the best individuals (optional)
# verbose indicates whether or not to log the statistics

# the above algo will run for 40 generations - i.e. 40 iterations of training

    # print log
    print '\n'
    print '\n'
    print 'The function generated by GP that best forecasts the stock price is ->'
    print '\n'
    print hof[0]
    print '\n'
    function = toolbox.compile(expr=hof[0])
    obtained = function(open_val[p-2],close_val[p-2],low_val[p-2],high_val[p-2],volume_val[p-2])
    expected = close_val[p-1]
    difference = abs(obtained-expected)
    print 'The expected closing price is ->'
    print '\n'
    print expected
    print '\n'
    print 'The obtained closing price is ->'
    print '\n'
    print obtained
    print '\n'
    print 'The difference between expected and obtained is ->'
    print '\n'
    print difference
    print '\n'
    previous_day_price = open_val[p-2]
    print 'The open price on the day is = '
    print previous_day_price
    print '\n'
    print '\n'
    print 'GP said -> '
    gp_says = obtained - previous_day_price
    print gp_says
    print '\n'
    todays_price = (float)(ystockquote.get_price(ticker))
    reality_says = todays_price - expected
    print '\n'
    print 'Reality says ->'
    print reality_says
    return pop, log, hof

if __name__ == "__main__":
    main()
