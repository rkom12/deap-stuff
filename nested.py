import ystockquote
import ast

class AutoVivification(dict):
#    Implementation of perl's autovivification feature
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


a = AutoVivification()
a = ystockquote.get_historical_prices('MSFT','2016-08-08','2016-08-12')
print a
#b = ast.literal_eval(a['2016-08-07']['High'])
#b = b+100
#print b