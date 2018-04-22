from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data

# Dow Jones
param = {
    'q': "AAPL", # Stock symbol (ex: "AAPL")
    'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
    'x': "NASDAQ", # Stock exchange symbol on which stock is traded (ex: "NASDAQ")
    'p': "1M" # Period (Ex: "1Y" = 1 year)
}
# get price data (return pandas dataframe)
df = get_price_data(param)

time = []
open = []
i = 0
for item  in df.iterrows():
    print("first:{0}  second:{1}".format(item[0], item[1]))
    print(item[1][0])
    i += 1
    time.append(i)
    open.append(item[1][0])

print(time)
print(open)

from bokeh.plotting import figure, output_file, show
output_file("test.html")
p = figure()
p.line(x=time, y=open)
show(p)