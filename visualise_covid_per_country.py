import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

from utils import *

fname='csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'


current_growth_rate = 1.15
# normalise infected by the country polulation
population_normalise = False

# how many weeks to estimate by exponential function
num_weeks = 11

# syncronise the beginning of infection by the minimum infected
syncronise = False
# the minimum infected for synchrinisation
min_infected = 20
# how much zoom in
zoom = 5
# sub region of the original plot
start_date, end_date, start_infection, end_infection = 35, 45, 0, 4000

simulate_country='Italy'

countries = ['Italy', 'Austria', 'Iran','Switzerland','Germany','Mainland China']

population = {'Italy':60.48e6, 'Austria':8.822e6, 'Iran':81.16e6,'Switzerland':8.57e6,'Germany':82.79e6,'Mainland China':1.386e9}
country_dict ={'Italy':'IT', 'Austria':'AT', 'Iran':'IR','Switzerland':'CH','Germany':'DE','Mainland China':'CN'}

fig, ax = plt.subplots(figsize=[5,4])



# plot infections
plot_infections(countries, fname, ax,min_infected,
                population_normalise,population,country_dict,
                simulate_country,num_weeks,syncronise,current_growth_rate)
# zoom in
axins = zoomed_inset_axes(ax, zoom, loc=10)
# plot again for the zoomed-in region
plot_infections(countries, fname, axins,min_infected,
                population_normalise,population,country_dict,
                simulate_country,num_weeks,syncronise,current_growth_rate)


# limit the borders of the zoom plot
axins.set_xlim(start_date, end_date)
axins.set_ylim(start_infection, end_infection)

# set ticks off for zoomed in plot
# plt.xticks(visible=False)
# plt.yticks(visible=False)

# put zoommed in plot in place
mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.5")

# set legends, title, etc
ax.legend(loc=1)
ax.set_title('Infections')
ax.set_xlabel('Days')
if population_normalise:
    ax.set_ylabel('Total Infected (% of population)')
else:
    ax.set_ylabel('Total Infected (person)')
plt.tight_layout()
# plt.yscale('log',basey=2)
# plt.show()
plt.savefig('infected_plots')

print('done')
