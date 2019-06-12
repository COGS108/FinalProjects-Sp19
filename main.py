import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (20,10)#enlarge figure
import seaborn as sns
sns.set(style = 'white', font_scale=2)#set scale
from scipy.stats import uniform, norm, bernoulli, poisson
from matplotlib import rc
from sklearn.linear_model import LinearRegression


#load the dataset
def load_csv(file_path):
    data = pd.read_csv(file_path)
    return data

#data wrangling
def check_non_zero_values(data):
    print(data.astype(bool).sum(axis=0))
    print(data.count())
    ind = data.index[data['Emissions'] == 0].tolist()
    for x in ind:
        print(data.loc[x])

def data_wrangling(data):
    #remove rows missing values
    data = data.dropna()
    #drop code axis
    data = data.drop('Code', axis =1)
    data['Emissions']=data['Emissions']/1000
    return data

#extract usa from the datasets
def extract_country(data, name):
    data = data[data.Code == name]
    return data

#separate USA data into lists of 5 elements by industry
def separate_by_industry(data):
    list = []
    list.append(data[data.Sector == 'Transport'])
    list.append(data[data.Sector == 'Other industrial combustion'])
    list.append(data[data.Sector == 'Buildings'])
    list.append(data[data.Sector == 'Non-combustion'])
    list.append(data[data.Sector == 'Power Industry'])
    return list

#descriptive: line plot
def line_plot(ax,data,lab):
    ax.plot(data['Year'],data['Emissions'],label=lab)
    plt.legend()

#descriptive: central tendency and variability
def central_and_variability(data,lab):
    print('For ',lab,':')
    print('Mean:',(int)(data['Emissions'].mean()),'Tg/year')
    print('Median:',(int)(data['Emissions'].median()),'Tg/year')
    print('Range:',(int)(data['Emissions'].max()
          -data['Emissions'].min()),'Tg/year')
    up,low=np.percentile(data['Emissions'],[75,25])
    print('IQR:',(int)(up-low),'Tg/year')
    print('Standard Deviation:',(int)(data['Emissions'].std()),'Tg/year')
    print()

#exploratory: box plot
def box_plot(data):
    fig, axs = plt.subplots(3, 2)
    df = data.set_index('Sector')

    axs[0, 0].boxplot(df.loc['Transport', 'Emissions'], 0, 'rs', 0)
    axs[0, 0].set_title('Transport Sector')

    axs[0, 1].boxplot(df.loc['Other industrial combustion', 'Emissions'], 0, 'rs', 0)
    axs[0, 1].set_title('Other industrial combustion Sector')

    axs[1, 0].boxplot(df.loc['Buildings', 'Emissions'], 0, 'rs', 0)
    axs[1, 0].set_title('Buildings Sector')

    axs[1, 1].boxplot(df.loc['Non-combustion', 'Emissions'], 0, 'rs', 0)
    axs[1, 1].set_title('Non-combustion Sector')

    axs[2, 0].boxplot(df.loc['Power Industry', 'Emissions'], 0, 'rs', 0)
    axs[2, 0].set_title('Power Industry Sector')

    axs[2, 1].boxplot(df['Emissions'], 0, 'rs', 0)
    axs[2, 1].set_title('Total Emissions')

    plt.subplots_adjust(hspace=0.95)
    plt.show()

#exploratory: scatter plot and linear regression
def scatter_plot(data, sector):
    x = data['Year'].tolist()
    x = list(set(x))
    y = data.set_index('Sector')
    y = y.loc[sector]
    y = y['Emissions'].tolist()

    fig, ax=plt.subplots()
    plt.scatter(x, y, marker = 'x')
    ax.set(xlabel='Time (year)',ylabel='CO2 Emissions (Tg)',
    title='Changes of CO2 Emissions in the ' + sector + ' Industry (1970-2016)')

    x = np.array(x)
    x = x.reshape(-1, 1)
    y = np.array(y)
    y = y.reshape(-1, 1)

    linear_reg = LinearRegression()
    linear_reg.fit(x, y)
    y_pred = linear_reg.predict(x)
    plt.plot(x, y_pred, color='red')
    plt.show()

#exploratory: Pearson's correlation coefficient
def correlation(data, sector):
    x = data['Year'].tolist()
    x = list(set(x))
    y = data.set_index('Sector')
    y = y.loc[sector]
    y = y['Emissions'].tolist()

    coeff = np.corrcoef(x, y)
    print(sector + ": %.2f" %coeff[1, 0])

#adjust font size on subplots
def font_change():
        SMALL_SIZE = 18
        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
        plt.rc('figure', titlesize=SMALL_SIZE)  # fontsize of the figure title

def main():
    font_change()

    file_path = './edgar-co2-emissions.csv'
    data = load_csv(file_path)

    #descriptive: null value
    print('Checking missing data')
    print('The distribution of missing data:')
    print(data.isnull().sum())
    null_rows = data.isnull().any(axis=1)
    print('The size of missing data:',data[null_rows].shape)
    print('No data is missing.')
    print()

    #data wrangling
    data = extract_country(data, 'USA')
    data = data_wrangling(data)
    co2ByIndustry = separate_by_industry(data)
    print('Data wrangling completed')
    print()

    #descriptive: size
    print('Descriptive Data Analysis:')
    print('The size of data:', data.shape)
    print()

    #descriptive: central tendency and variability
    central_and_variability(co2ByIndustry[0],'Transport')
    central_and_variability(co2ByIndustry[1],'Other industrial combustion')
    central_and_variability(co2ByIndustry[2],'Buildings')
    central_and_variability(co2ByIndustry[3],'Non-combustion')
    central_and_variability(co2ByIndustry[4],'Power Industry')

    #descriptive: line plot
    fig, ax=plt.subplots()
    line_plot(ax,co2ByIndustry[0],'Transport')
    line_plot(ax,co2ByIndustry[1],'Other industrial combustion')
    line_plot(ax,co2ByIndustry[2],'Buildings')
    line_plot(ax,co2ByIndustry[3],'Non-combustion')
    line_plot(ax,co2ByIndustry[4],'Power Industry')
    ax.set(xlabel='Time (year)',ylabel='CO2 Emissions (Tg)',
           title='Changes of USA CO2 Emissions (1970-2016)')
    plt.show()

    #exploratory: Pearson's correlation coefficient
    print("Pearson's correlation coefficient for each sector:")
    correlation(data, 'Transport')
    correlation(data, 'Other industrial combustion')
    correlation(data, 'Buildings')
    correlation(data, 'Non-combustion')
    correlation(data, 'Power Industry')

    #exploratory: scatter plot + linear regression
    scatter_plot(data, 'Transport')
    scatter_plot(data, 'Other industrial combustion')
    scatter_plot(data, 'Buildings')
    scatter_plot(data, 'Power Industry')

    #exploratory: box plots
    box_plot(data)

main()
