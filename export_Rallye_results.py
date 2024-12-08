import pandas as pd
import configparser
import database_handler as dbh

config = configparser.ConfigParser()
config.read('config.ini')

# set for each export
rallye = '7'
# ------------

# ------------------------
def formatage_categorie(cat):
    resultats = []
    cat.sort(key=lambda x: x[2])
    i = 1
    for resultat in cat:
        resultats.append([i, resultat[0], resultat[1], format_time_string(resultat[2]),format_time_string(resultat[3]),resultat[4],resultat[5],resultat[6],calcul_total(resultat[4],resultat[5],resultat[6])])
        i = i+1
    return resultats

def format_time_string(time):
    if time[:4] == "00:0":
        time = time[4:]
    if time[:3] == "00:":
        time = time[3:]
    if time[:1] == "0":
        time = time[1:]
    if time[-4:][:1] != '.' and time[-4:][:1] != 'D':
        time = time + ".000"
    return time

def calcul_total(categorie, powerstage, general):
    return categorie + powerstage + general
# ------------------------

resultats_global = dbh.GetRallyResults(rallye)

res_global = []
i = 1
for resultat in resultats_global:
    res_global.append([i, resultat[4],resultat[5],format_time_string(resultat[6]),resultat[10], '***'])
    i = i+1

resultats_plat = []
resultats_gold = []
resultats_silver = []
resultats_bronze = []

for resultat in resultats_global:
    match resultat[1]:
        case 'Platine':
            resultats_plat.append([resultat[4], resultat[5], resultat[6], resultat[7], resultat[8], resultat[9], resultat[10]])
        case 'Gold':
            resultats_gold.append([resultat[4], resultat[5], resultat[6], resultat[7], resultat[8], resultat[9], resultat[10]])
        case 'Silver':
            resultats_silver.append([resultat[4], resultat[5], resultat[6], resultat[7], resultat[8], resultat[9], resultat[10]])
        case 'Bronze':
            resultats_bronze.append([resultat[4], resultat[5], resultat[6], resultat[7], resultat[8], resultat[9], resultat[10]])

res_plat = formatage_categorie(resultats_plat)
res_gold = formatage_categorie(resultats_gold)
res_silver = formatage_categorie(resultats_silver)
res_bronze = formatage_categorie(resultats_bronze)

columns_cat = ['position','Nom', 'Voiture/Car', 'Temps', 'Temps Power Stage', 'Points', 'Power Stage', 'Bonus Overall', 'Total']
# Create a DataFrame from the list
df = pd.DataFrame(res_global, columns=['position','Nom', 'Voiture', 'Temps', 'Points', 'Promo'])
df_plat = pd.DataFrame(res_plat, columns=columns_cat)
df_gold = pd.DataFrame(res_gold, columns=columns_cat)
df_silver = pd.DataFrame(res_silver, columns=columns_cat)
df_bronze = pd.DataFrame(res_bronze, columns=columns_cat)
# Save it as an Excel file
excel_file = 'Resultat_Rallye.xlsx'
with pd.ExcelWriter(config['settings']['path'] + excel_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name="Global", index=False)
    df_plat.to_excel(writer, sheet_name="Platine", index=False)
    df_gold.to_excel(writer, sheet_name="Gold", index=False)
    df_silver.to_excel(writer, sheet_name="Silver", index=False)
    df_bronze.to_excel(writer, sheet_name="Bronze", index=False)