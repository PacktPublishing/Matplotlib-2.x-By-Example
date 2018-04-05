import matplotlib
import matplotlib.pyplot as plt
import textwrap
import requests
import pandas as pd
from bs4 import BeautifulSoup
# Import Matplotlib radio button widget
from matplotlib.widgets import RadioButtons


url = "https://www.bls.gov/emp/ep_table_001.htm"
response = requests.get(url)
bs = BeautifulSoup(response.text)
thead = bs.select("#bodytext > table > thead")[0]
tbody = bs.select("#bodytext > table > tbody")[0]

headers = []
for col in thead.find_all('th'):
    headers.append(col.text.strip())

data = {header:[] for header in headers}
for row in tbody.find_all('tr'):
    cols = row.find_all(['th','td'])
    
    for i, col in enumerate(cols):
        value = col.text.strip()
        if i > 0:
            value = float(value.replace(',','')) 
        data[headers[i]].append(value)

df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(6,7))
ind = range(df.shape[0])
rects = ax.barh(ind, df["Median usual weekly earnings ($)"], height=0.5)
ax.set_xlabel('Median weekly earnings (USD)')
ylabels=[textwrap.fill(label,15) for label in df["Educational attainment"]]
ax.set_yticks(ind)
ax.set_yticklabels(ylabels)
fig.subplots_adjust(left=0.3)

# Create axes for holding the radio selectors.
# supply [left, bottom, width, height] in normalized (0, 1) units
bax = plt.axes([0.3, 0.9, 0.4, 0.1])
radio = RadioButtons(bax, ('Weekly earnings', 'Unemployment rate'))

# Define the function for updating the displayed values
# when the radio button is clicked
def radiofunc(label):
	# Select columns from dataframe depending on label
	if label == 'Weekly earnings':
		data = df["Median usual weekly earnings ($)"]
		ax.set_xlabel('Median weekly earnings (USD)')
	elif label == 'Unemployment rate':
		data = df["Unemployment rate (%)"]
		ax.set_xlabel('Unemployment rate (%)')
	
	# Update the bar heights
	for i, rect in enumerate(rects):
		rect.set_width(data[i])

	# Rescale the x-axis range
	ax.set_xlim(xmin=0, xmax=data.max()*1.1)
	
	# Redraw the figure
	plt.draw()
radio.on_clicked(radiofunc)

plt.show()