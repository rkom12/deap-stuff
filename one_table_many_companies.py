import ystockquote
import peewee
from peewee import *

db = MySQLDatabase('stock1', user='root',passwd='penguin')

class Stocks(peewee.Model):
    week_high_52 = peewee.FloatField()
    week_low_52 = peewee.FloatField()
    price = peewee.FloatField()
    volume = peewee.IntegerField()

    company = peewee.CharField()

    class Meta:
	database = db

Stocks.create_table()

google_arg1 = ystockquote.get_52_week_high('GOOG')
google_arg2 = ystockquote.get_52_week_low('GOOG')
google_arg3 = ystockquote.get_price('GOOG')
google_arg4 = ystockquote.get_volume('GOOG')

google_stocks = Stocks(week_high_52 = google_arg1 , week_low_52 = google_arg2 , price = google_arg3 , volume = google_arg4 , company = 'Google')
google_stocks.save()




adobe_arg1 = ystockquote.get_52_week_high('ADBE')
adobe_arg2 = ystockquote.get_52_week_low('ADBE')
adobe_arg3 = ystockquote.get_price('ADBE')
adobe_arg4 = ystockquote.get_volume('ADBE')

adobe_stocks = Stocks(week_high_52 = adobe_arg1 , week_low_52 = adobe_arg2 , price = adobe_arg3 , volume = adobe_arg4 , company = 'Adobe')
adobe_stocks.save()




nvidia_arg1 = ystockquote.get_52_week_high('NVDA')
nvidia_arg2 = ystockquote.get_52_week_low('NVDA')
nvidia_arg3 = ystockquote.get_price('NVDA')
nvidia_arg4 = ystockquote.get_volume('NVDA')

nvidia_stocks = Stocks(week_high_52 = nvidia_arg1 , week_low_52 = nvidia_arg2 , price = nvidia_arg3 , volume = nvidia_arg4 , company = 'Nvidia')
nvidia_stocks.save()







microsoft_arg1 = ystockquote.get_52_week_high('MSFT')
microsoft_arg2 = ystockquote.get_52_week_low('MSFT')
microsoft_arg3 = ystockquote.get_price('MSFT')
microsoft_arg4 = ystockquote.get_volume('MSFT')

microsoft_stocks = Stocks(week_high_52 = microsoft_arg1 , week_low_52 = microsoft_arg2 , price = microsoft_arg3 , volume = microsoft_arg4 , company = 'Microsoft')
microsoft_stocks.save()





facebook_arg1 = ystockquote.get_52_week_high('FB')
facebook_arg2 = ystockquote.get_52_week_low('FB')
facebook_arg3 = ystockquote.get_price('FB')
facebook_arg4 = ystockquote.get_volume('FB')

facebook_stocks = Stocks(week_high_52 = facebook_arg1 , week_low_52 = facebook_arg2 , price = facebook_arg3 , volume = facebook_arg4 , company = 'Facebook')
facebook_stocks.save()





cognizant_arg1 = ystockquote.get_52_week_high('CTSH')
cognizant_arg2 = ystockquote.get_52_week_low('CTSH')
cognizant_arg3 = ystockquote.get_price('CTSH')
cognizant_arg4 = ystockquote.get_volume('CTSH')

cognizant_stocks = Stocks(week_high_52 = cognizant_arg1 , week_low_52 = cognizant_arg2 , price = cognizant_arg3 , volume = cognizant_arg4 , company = 'Cognizant')
cognizant_stocks.save()






accenture_arg1 = ystockquote.get_52_week_high('ACN')
accenture_arg2 = ystockquote.get_52_week_low('ACN')
accenture_arg3 = ystockquote.get_price('ACN')
accenture_arg4 = ystockquote.get_volume('ACN')

accenture_stocks = Stocks(week_high_52 = accenture_arg1 , week_low_52 = accenture_arg2 , price = accenture_arg3 , volume = accenture_arg4 , company = 'Accenture')
accenture_stocks.save()




#for google in Google.filter(author="Khalid"):
 #   print google.title

# replace 3 things - Google,google,GOOG
# adobe - ADBE
# nvidia - NVDA
# microsoft - MSFT
# facebook - FB
# cogni - CTSH
# accenture - ACN
# persistent - PERSISTENT - apparently can't be fetched