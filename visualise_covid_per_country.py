import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

import pandas as pd
import numpy as np

fname='csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'

# normalise infected by the country polulation
population_normalise = False

# how many weeks to estimate by exponential function
num_weeks = 12

# syncronise the beginning of infection by the minimum infected
syncronise = False
# the minimum infected for synchrinisation
min_infected = 20
zoom=5
def isNaN(num):
    return num != num

def synch(data, min_infected):
    if syncronise:
        ix = np.argmax(np.array(data) >= min_infected)
    else:
        ix = 0
    return ix

countries = ['Italy', 'Austria', 'Iran','Switzerland','Germany','Mainland China']
population = {'Italy':60.48e6, 'Austria':8.822e6, 'Iran':81.16e6,'Switzerland':8.57e6,'Germany':82.79e6,'Mainland China':1.386e9}
# countries = ['Italy', 'Austria', 'Iran','Switzerland','Germany']
country_dict ={'Italy':'IT', 'Austria':'AT', 'Iran':'IR','Switzerland':'CH','Germany':'DE','Mainland China':'CN'}


fig, ax = plt.subplots(figsize=[5,4])


def plot_infections(countries, fname, ax):
    len_inf = []
    synched_infected_dic = {}

    for country in countries:
        df = pd.read_csv(fname)
        country_results = df[(df['Country/Region'] == country)]

        dates = ['1/24/20', '1/25/20', '1/26/20', '1/27/20', '1/28/20', '1/29/20',
                 '1/30/20', '1/31/20', '2/1/20', '2/2/20', '2/3/20', '2/4/20', '2/5/20',
                 '2/6/20', '2/7/20', '2/8/20', '2/9/20', '2/10/20', '2/11/20', '2/12/20',
                 '2/13/20', '2/14/20', '2/15/20', '2/16/20', '2/17/20', '2/18/20',
                 '2/19/20', '2/20/20', '2/21/20', '2/22/20', '2/23/20', '2/24/20',
                 '2/25/20', '2/26/20', '2/27/20', '2/28/20', '2/29/20',
                 '3/1/20', '3/2/20', '3/3/20', '3/4/20', '3/5/20']

        infected = []

        for day in dates:
            total_infected_state = 0
            for state in country_results['Province/State']:
                if not isNaN(state):
                    infected_state = df[(df['Country/Region'] == country) & (df['Province/State'] == state)]
                else:
                    infected_state = df[(df['Country/Region'] == country)]
                total_infected_state += infected_state[day].values[0]

            infected.append(total_infected_state)
        # find first non-zero infected date
        ix = synch(infected, min_infected)
        synched_infected = np.array(infected[ix:], dtype=np.float32)

        if population_normalise:
            synched_infected /= population[country]

        ax.plot(synched_infected, label=country_dict[country])
        len_inf.append(len(synched_infected))
        synched_infected_dic[country] = synched_infected

    # prepare exponential data, double every week, for 10 weeks.
    exp_data = np.exp(range(num_weeks))
    exp_date_index = [7 * i for i in range(num_weeks)]

    # synch exponential data
    ix = synch(exp_data, min_infected)
    synched_exp_data = exp_data[ix:]
    synched_exp_data_index = [p - exp_date_index[ix] for p in exp_date_index[ix:]]

    # plot expo. data
    ax.plot(synched_exp_data_index, synched_exp_data, label='Exp.')


# plot infections
plot_infections(countries, fname, ax)
# zoom in
axins = zoomed_inset_axes(ax, zoom, loc=6)
# plot again for the zoomed-in region
plot_infections(countries, fname, axins)


# sub region of the original plot
start_date, end_date, start_infection, end_infection = 35, 45, 0, 5000
axins.set_xlim(start_date, end_date)
axins.set_ylim(start_infection, end_infection)
# set ticks off for zoomed in plot
# plt.xticks(visible=False)
plt.yticks(visible=False)
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
