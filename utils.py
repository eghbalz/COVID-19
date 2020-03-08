import pandas as pd
import numpy as np

def isNaN(num):
    return num != num

def synch(data, min_infected, syncronise):
    if syncronise:
        ix = np.argmax(np.array(data) >= min_infected)
    else:
        ix = 0
    return ix

def exponen(data, current_growth_rate):
    return [current_growth_rate**d for d in data]

def sigmoid(x):
    x = np.array(x,dtype=np.float32)
    return 1/(1 + np.exp(-x))


def get_logistic(synched_infected):
    selected_sim = 2 * max(synched_infected)
    logistic_data_index = range(-len(synched_infected), len(synched_infected))
    # renormalise logistic
    logistic_data = sigmoid(logistic_data_index)
    logistic_data *= selected_sim
    logistic_data_index = range(2 * len(synched_infected))
    return logistic_data_index, logistic_data



def plot_infections(countries, fname, ax,min_infected,population_normalise,
                    population,country_dict,simulate_country,num_weeks,syncronise,current_growth_rate):
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
        ix = synch(infected, min_infected,syncronise)
        synched_infected = np.array(infected[ix:], dtype=np.float32)

        if population_normalise:
            synched_infected /= population[country]

        ax.plot(synched_infected, label=country_dict[country])
        len_inf.append(len(synched_infected))
        synched_infected_dic[country] = synched_infected
        if simulate_country==country:
            logistic_data_index, logistic_data = get_logistic(synched_infected)


    # prepare exponential data, double every week, for 10 weeks.
    exp_data = exponen(range(num_weeks*7),current_growth_rate)
    exp_date_index = [i for i in range(num_weeks*7)]




    # synch exponential data
    ix = synch(exp_data, min_infected,syncronise)
    synched_exp_data = exp_data[ix:]
    synched_exp_data_index = [p - exp_date_index[ix] for p in exp_date_index[ix:]]
    # synched_log_data_index = [p - exp_date_index[ix] for p in logistic_data_index[ix:]]
    # synched_log_data = logistic_data[ix:]

    # plot expo. data
    ax.plot(synched_exp_data_index, synched_exp_data, label='Exp.')
    # plot logistic data
    ax.plot(logistic_data_index, logistic_data, label='Log.')

