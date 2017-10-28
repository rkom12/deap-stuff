# 'deap'-stuff

In-sem break ->

So now,we've got a idea of how RSI works. Tentatively, we'll use the RSI model (take average of 14 days,smooth it with current values,scale to 0-100) and use resistance bands to find the **overbought** and **oversold** conditions to determine the buying or selling or holding of stocks.

In the 2nd approach- We'll do the exact same things, except that the 'taking average & smoothing with current values & (maybe)scaling it to 0-100' will all be done by GP(Genetic Programming). Thus, we hope that a comparitive paper might be possible.

And to top it off,we'll try to find some fundamental analysis stuff that might help us identify strong trends so that the RSI accuracy is maintained.

Well then,we'll continue after the exams !

---------------------------------------------------------------------------------------------------------------------------------
example.py (modified code will be uploaded soon) --------------------------------->

A sample symbolic regression GP code has been carefully optimized and explained. Our main stock forecasting code will (probably) be similar to this 'style' of code.

To run the code,use pip to install the DEAP (Distributed Evolutionary Algorithms in Python) package -
```
pip install deap
```

If pip wasn't bundled with your current python version,then isntall pip -
```
sudo apt-get install python-setuptools

sudo easy_install pip
```

## File Description:-


---------------------------------------------------------------------------------------------------------------------------------
example_output --------------------------------->

Shows the output of 'example.py' - an alternative but highly identical function for a quartic polynomial (x4+x3+x2+x) is generated.


---------------------------------------------------------------------------------------------------------------------------------
one_table_many_companies.py (modified code will be uploaded soon) --------------------------------->

Some sample stock data is taken for trial uses. The data is fetched from Yahoo using the 'ystockquote' API and put into a MySQL table - it's things like these that restore faith in humanity ;)


---------------------------------------------------------------------------------------------------------------------------------
nested.py --------------------------------->

Illustrates the use of AutoVivification to traverse nested dictionaries like a pro.

---------------------------------------------------------------------------------------------------------------------------------
microsoft_proto.py --------------------------------->

Finally,a proper working mini-prototype of our project. Admittedly, it's rather too mini - but hey,I'd say this lays down solid foundations for our GP-stock project.



---------------------------------------------------------------------------------------------------------------------------------
microsoft_proto_output

Output of the basic code. The expressions that are formed kinda resemble time-series analysis stuff - looks promising !


---------------------------------------------------------------------------------------------------------------------------------

