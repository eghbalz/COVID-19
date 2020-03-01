import matplotlib.pyplot as plt
import csv
import pandas as pd
import math
import numpy as np

fname='csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'

population_normalise = True
min_infected = 5

def isNaN(num):
    return num != num


countries = ['Italy', 'Austria', 'Iran','Switzerland','Germany','Mainland China']
population = {'Italy':60.48e6, 'Austria':8.822e6, 'Iran':81.16e6,'Switzerland':8.57e6,'Germany':82.79e6,'Mainland China':1.386e9}


for country in countries:
    df = pd.read_csv(fname)
    country_results = df[(df['Country/Region'] ==country)]

    dates=['1/24/20', '1/25/20', '1/26/20', '1/27/20', '1/28/20', '1/29/20',
           '1/30/20', '1/31/20', '2/1/20', '2/2/20', '2/3/20', '2/4/20', '2/5/20',
           '2/6/20', '2/7/20', '2/8/20', '2/9/20', '2/10/20', '2/11/20', '2/12/20',
           '2/13/20', '2/14/20', '2/15/20', '2/16/20', '2/17/20', '2/18/20',
           '2/19/20', '2/20/20', '2/21/20', '2/22/20', '2/23/20', '2/24/20',
           '2/25/20', '2/26/20', '2/27/20', '2/28/20', '2/29/20']

    infected = []

    for day in dates:
        total_infected_state = 0
        for state in country_results['Province/State']:
            if not isNaN(state):
                infected_state = df[(df['Country/Region'] == country) & (df['Province/State'] == state)]
            else:
                infected_state = df[(df['Country/Region'] == country)]
            total_infected_state +=infected_state[day].values[0]

        infected.append(total_infected_state)
    # find first non-zero infected date
    ix = np.argmax(np.array(infected) >= min_infected)
    synched_infected = np.array(infected[ix:],dtype=np.float32)

    if population_normalise:
        synched_infected/=population[country]

    plt.plot(synched_infected,label=country)

plt.legend()
plt.title('Infections')
plt.xlabel('Days')
if population_normalise:
    plt.ylabel('Total Infected (% of population)')
else:
    plt.ylabel('Total Infected (person)')
plt.tight_layout()
# plt.yscale('log',basey=2)
# plt.show()
plt.savefig('infected_plots')

print('done')
