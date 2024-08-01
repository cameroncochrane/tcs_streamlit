import TCS_pipeline as tcs

countries = tcs.country_list()
circle_icons = []

for i in range(0,len(countries)):
    circle_icons.append(f"{i+1}-circle")

a = ["house"] + circle_icons

print(a)