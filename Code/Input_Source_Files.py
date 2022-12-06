

#----------------------------------------------



nse_stocks = {}

for file in os.listdir(path + "/historic_data/csv/"):

    nse_stocks[file.split(".csv")[0]] = pd.read_csv(path + "/historic_data/csv/" + file)








