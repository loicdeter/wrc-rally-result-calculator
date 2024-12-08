points_powerstage = [5,4,3,2,1]
points_overal = [25,23,21,19,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]

def category_points(list_category: list):
    list_category.sort(key=lambda x: x[3])
    set_points(list_category, points_overal, 1, 1)
    return list_category

def powerstage_points(list_powerstage: list):
    list_powerstage.sort(key=lambda x: x[4])
    set_points(list_powerstage, points_powerstage, 0, 0)
    return list_powerstage

def overall_points(list_overall: list):
    list_overall.sort(key=lambda x: x[3])
    set_points(list_overall, points_overal, 1, 0)
    return list_overall

def set_points(list: list, points_list: list, default_points: int, dnf_points: int):
    i = 0
    for item in list:
        points = default_points
        if i < len(points_list):
            points = points_list[i]
        if item[3] == "DNF":
            points = dnf_points

        item.append(points)
        i = i+1