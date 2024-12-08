import pandas as pd
import point_calculator as pc
import configparser
import database_handler as dbh

config = configparser.ConfigParser()
config.read('config.ini')

# set for each import
rallye = '7'
folder = 'S10-Estonia/'
# ------------

path = config['settings']['path'] + folder
plat_final_csv_file = "Platine_Final.csv"
plat_overall_csv_file = "Platine_Overall.csv"
plat_power_csv_file = "Platine_PowerStage.csv"
gold_final_csv_file = "Gold_Final.csv"
gold_overall_csv_file = "Gold_Overall.csv"
gold_power_csv_file = "Gold_PowerStage.csv"
silver_final_csv_file = "Silver_Final.csv"
silver_overall_csv_file = "Silver_Overall.csv"
silver_power_csv_file = "Silver_PowerStage.csv"
bronze_final_csv_file = "Bronze_Final.csv"
bronze_overall_csv_file = "Bronze_Overall.csv"
bronze_power_csv_file = "Bronze_PowerStage.csv"

name_mapping = pd.read_csv(path + '../name_mapping.csv').values.tolist()

plat_final = pd.read_csv(path + plat_final_csv_file).values.tolist()
plat_overall = pd.read_csv(path + plat_overall_csv_file).values.tolist()
plat_power = pd.read_csv(path + plat_power_csv_file).values.tolist()
gold_final = pd.read_csv(path + gold_final_csv_file).values.tolist()
gold_overall = pd.read_csv(path + gold_overall_csv_file).values.tolist()
gold_power = pd.read_csv(path + gold_power_csv_file).values.tolist()
silver_final = pd.read_csv(path + silver_final_csv_file).values.tolist()
silver_overall = pd.read_csv(path + silver_overall_csv_file).values.tolist()
silver_power = pd.read_csv(path + silver_power_csv_file).values.tolist()
bronze_final = pd.read_csv(path + bronze_final_csv_file).values.tolist()
bronze_overall = pd.read_csv(path + bronze_overall_csv_file).values.tolist()
bronze_power = pd.read_csv(path + bronze_power_csv_file).values.tolist()

#--------------------
def lecture_resultats(final, overall, power, categorie):
    resultats = []
    i = 0

    for participant in final:
        found = False
        nom = ""
        for over in overall:
            if participant[1] in over:
                found = True
                vehicule = over[2]
                temps_total = over[3][:-4]

        for ps in power:
            if participant[1] in ps:
                if len(ps[3]) > 8:
                    temps_power = ps[3][:-4]
                else:
                    temps_power = ps[3]

        for name in name_mapping:
            if participant[1] in name:
                nom = name[1]
        
        if not found:
            vehicule = "-"
            temps_total = "DNF"
            temps_power = "DNF"

        new_item = [categorie, participant[1], vehicule, temps_total, temps_power, nom]
        resultats.append(new_item)
        i = i+1
    
    return resultats
#-------------------

resultats_plat = lecture_resultats(plat_final, plat_overall, plat_power, "Platine")
resultats_gold = lecture_resultats(gold_final, gold_overall, gold_power, "Gold")
resultats_silver = lecture_resultats(silver_final, silver_overall, silver_power, "Silver")
resultats_bronze = lecture_resultats(bronze_final, bronze_overall, bronze_power, "Bronze")

resultats_plat = pc.category_points(resultats_plat)
resultats_gold = pc.category_points(resultats_gold)
resultats_silver = pc.category_points(resultats_silver)
resultats_bronze = pc.category_points(resultats_bronze)

#set power stage results
resultats_plat_gold_power = resultats_plat + resultats_gold
pc.powerstage_points(resultats_plat_gold_power)

resultats_bronze_silver_power = resultats_silver + resultats_bronze
pc.powerstage_points(resultats_bronze_silver_power)

#set overal results
resultats_global = resultats_plat + resultats_gold + resultats_silver + resultats_bronze
pc.overall_points(resultats_global)

# calcul total
for resultat in resultats_global:
    resultat.append(resultat[6] + resultat[7] + resultat[8])

resultats_plat.sort(key=lambda x: x[3])
resultats_gold.sort(key=lambda x: x[3])
resultats_silver.sort(key=lambda x: x[3])
resultats_bronze.sort(key=lambda x: x[3])


for resultat in resultats_global:
    res = dbh.FindResult(resultat[0], rallye, resultat[1])
    if res == None:
        dbh.InsertResult(resultat[0], rallye, resultat[1], resultat[5], resultat[2], resultat[3], resultat[4], resultat[6], resultat[7], resultat[8])
