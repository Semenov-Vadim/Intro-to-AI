from copy import deepcopy  # для удаления элементов списка во время прохода по списку
from random import uniform
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox

# название города и кол-во сотен зараженных
cityNameInfected = {0: ["Kyiv", 87848],
                    1: ["Poltava", 50900],
                    2: ["Sumy", 54104],
                    3: ["Chernihiv", 39473],
                    4: ["Zhytomyr", 65592],
                    5: ["Vinnytsia", 51762],
                    6: ["Cherkasy", 53630],
                    7: ["Kharkiv", 95416],
                    8: ["Dnipro", 83909],
                    9: ["Kropyvnytskyi", 12034],
                    10: ["Zaporizhia", 74449],
                    11: ["Mykolaiv", 48575],
                    12: ["Rivne", 53714],
                    13: ["Khmelnytskyi", 57280],
                    14: ["Chernivtsi", 65939]}

# нормализация (приведение значений к отрезку [0 ; 1])
cityInfectedNorm = {}
for city in cityNameInfected:
    cityInfectedNorm[city] = (cityNameInfected[city][1] - 12034) / (95416 - 12034)

# матрица расстояний между городами (0 если нет возможности посетить город, не задев другой город)
distanceCities = [[0, 337, 346, 134, 150, 240, 180, 0, 0, 0, 0, 0, 0, 0, 0],
                  [337, 0, 178, 0, 0, 0, 224, 142, 169, 241, 264, 0, 0, 0, 0],
                  [346, 178, 0, 290, 0, 0, 0, 183, 0, 0, 0, 0, 0, 0, 0],
                  [134, 0, 290, 0, 290, 0, 0, 0, 0, 0, 0, 0, 481, 0, 0],
                  [180, 0, 0, 290, 0, 126, 0, 0, 0, 0, 0, 0, 186, 180, 0],
                  [240, 0, 0, 0, 126, 0, 341, 0, 0, 315, 0, 423, 271, 122, 285],
                  [146, 224, 0, 0, 0, 0, 341, 0, 283, 119, 0, 0, 0, 0, 0],
                  [0, 142, 183, 0, 0, 0, 0, 0, 213, 0, 286, 0, 0, 0, 0],
                  [0, 169, 0, 0, 0, 0, 283, 213, 0, 248, 84, 324, 0, 0, 0],
                  [0, 241, 0, 0, 0, 315, 119, 0, 248, 0, 305, 182, 0, 0, 579],
                  [0, 264, 0, 0, 0, 0, 0, 286, 84, 305, 0, 345, 0, 0, 0],
                  [0, 0, 0, 0, 0, 423, 0, 0, 324, 182, 345, 0, 0, 0, 628],
                  [0, 0, 0, 481, 186, 271, 0, 0, 0, 0, 0, 0, 0, 198, 322],
                  [0, 0, 0, 0, 180, 122, 0, 0, 0, 0, 0, 0, 198, 0, 191],
                  [0, 0, 0, 0, 0, 285, 0, 0, 0, 579, 0, 628, 322, 191, 0]]

# нормализация
distanceCitiesNorm = []
for i in range(15):
    distanceCitiesNorm.append(list())

for city in range(len(distanceCities)):
    for city2 in range(len(distanceCities[city])):
        if distanceCities[city][city2] != 0:
            distanceCitiesNorm[city].append((distanceCities[city][city2] - 84) / (628 - 84))
        else:
            distanceCitiesNorm[city].append(0)

# город, из которого начинается проход по остальным городам
startCity = 0


# возвращает список городов, к которым можно пройти из текущего города
def findNeighbor(curCity):
    neighbor = []
    counter = -1
    for city in distanceCities[curCity]:
        counter += 1
        if city != 0:
            neighbor.append(counter)
    return neighbor


# возвращает список городов, к которым можно пройти из текущего города (без учета посещенных городов)
def findNeighborCitiesNotVisited(curCity, PopulationIndiv):
    neighbor = findNeighbor(curCity)
    neighborCitiesNotVisited = deepcopy(neighbor)
    for city in neighbor:
        if city in PopulationIndiv.visited:
            neighborCitiesNotVisited.remove(city)
    return neighborCitiesNotVisited


class PopulationIndividual:
    def __init__(self, coefKilometers, coefPeople, startCity):
        self.coefKilometers = float(coefKilometers)
        self.coefPeople = float(coefPeople)
        self.peopleVaccinated = 0
        self.kilometers = 0
        self.visited = [startCity]

    def fitness(self):
        try:
            return self.peopleVaccinated / self.kilometers
        except ZeroDivisionError:
            return 0


# возвращает ключ из словаря с наибольшим значением value
def getGreatestKeyInDictByValue(cities):
    for key in cities:
        greatestKey = key
        break
    greatestVal = cities[key]
    for key in cities:
        if cities[key] > greatestVal:
            greatestKey = key
            greatestVal = cities[key]
    return greatestKey


# возвращает город, к которому можно пройти с наибольшим приоритетом
def find_priority_city(curCity, availableCities, PopulationIndiv):
    priorities = {}
    for city in availableCities:
        priorities[city] = PopulationIndiv.coefKilometers * distanceCitiesNorm[curCity][city] + PopulationIndiv.coefPeople * cityInfectedNorm[city]
    # print(priorities)
    return getGreatestKeyInDictByValue(priorities)


# обход всех городов
def go(curCity, PopulationIndiv):
    PopulationIndiv.peopleVaccinated += cityNameInfected[curCity][1]
    while len(findNeighborCitiesNotVisited(curCity, PopulationIndiv)) != 0:
        nextCity = find_priority_city(curCity, findNeighborCitiesNotVisited(curCity, PopulationIndiv), PopulationIndiv)
        # print()
        # print("curCity ", curCity)
        # print("ind.visited ", ind.visited)
        # print("nextCity ", nextCity)
        PopulationIndiv.kilometers += distanceCities[curCity][nextCity]
        PopulationIndiv.visited.append(nextCity)
        go(nextCity, PopulationIndiv)
    return PopulationIndiv.fitness()


# возвращвет две лучшие особи из всей популяции
def findBestTwo(allPopulation):
    top1 = allPopulation[0]
    top1Fitness = top1.fitness()
    top2 = allPopulation[1]

    if top2.fitness() > top1Fitness:
        top1, top2 = top2, top1
        top1Fitness = top1.fitness()

    for ind in allPopulation[2:]:
        if ind.fitness() > top1Fitness:
            top2 = top1
            top1 = ind
            top1Fitness = ind.fitness()

    # print(top1.fitness, top2.fitness())
    return [top1, top2]


# возвращвет 9 новых особей на основе двух наилучших
def generateNewPopulation(allPopulation):
    top1, top2 = findBestTwo(allPopulation)

    # установка новых коэффициентов (вычисляем среднее значение между двумя лучшими особями и устанавливаем новые
    # коэффициенты с отклонением, равным разности между двумя коэффициентами +- 1)
    newCoef1 = (top1.coefKilometers + top2.coefKilometers) / 2
    rangeCoef1 = (abs(top1.coefKilometers - top2.coefKilometers) / 2) + 1
    newCoef2 = (top1.coefPeople + top2.coefPeople) / 2
    rangeCoef2 = (abs(top1.coefPeople - top2.coefPeople) / 2) + 1

    allPopulation.clear()
    for i in range(3):
        for j in range(3):
            allPopulation.append(PopulationIndividual(uniform(newCoef1 - rangeCoef1, newCoef1 + rangeCoef1),
                                                      uniform(newCoef2 - rangeCoef2, newCoef2 + rangeCoef2), startCity))
    return allPopulation


# создает начальную популяцию особей
def generateInitialPopulation(startCity):
    allPopulation = []
    for i in range(3):
        coef = [-3, 0, 3]
        for j in range(3):
            allPopulation.append(PopulationIndividual(coef[i], coef[j], startCity))
    return allPopulation


# возвращает особь с наибольшим показанием fitness, через указанное число эволюций
def findBestIndivid(numberOfPopulations, startCity):
    allPopulation = generateInitialPopulation(startCity)
    bestIndivid = allPopulation[0]

    for i in range(numberOfPopulations):
        print("generation ", i + 1)
        for ind in allPopulation:
            go(startCity, ind)
            # print()

        for ind in findBestTwo(allPopulation):
            if ind.fitness() > bestIndivid.fitness():
                bestIndivid = ind
            print(ind.coefKilometers, ind.coefPeople)
            print(ind.fitness())
            print()
        print()

        generateNewPopulation(allPopulation)
    return bestIndivid


# bestIndivid = findBestIndivid(10, 0)
#print("bestIndivid", bestIndivid.fitness())
#print(bestIndivid.coefKilometers, bestIndivid.coefPeople)


# ------------------------------------------------------------------------------------
# создание окна
window = Tk()
window.title("Нахождение оптимального маршрута движения")
window.geometry('700x600')

# очередность расположения строк
rowCity = 0
rowGenerationCount = 1
rowGenerationButton = 2
rowInfoPanel = 3

# значения, введенные пользователем
valCity = StringVar()
valGenerationCount = StringVar()

cities = ("Kyiv",
          "Poltava",
          "Sumy",
          "Chernihiv",
          "Zhytomyr",
          "Vinnytsia",
          "Cherkasy",
          "Kharkiv",
          "Dnipro",
          "Kropyvnytskyi",
          "Zaporizhia",
          "Mykolaiv ",
          "Rivne",
          "Khmelnytskyi",
          "Chernivtsi")

lblStartCity = Label(window, text="Начальный город")
lblStartCity.grid(column=0, row=rowCity)

comboStartCity = Combobox(window)
comboStartCity['values'] = cities
comboStartCity.current(0)  # установите вариант по умолчанию
comboStartCity.grid(column=1, row=rowCity, pady=10)
lblStartCity = Entry(window, width=10, textvariable=valCity)
lblEmpty = Label(window, text="")  # создает третий столбик в grid для красивого вывода infoPanel
lblEmpty.grid(column=2, row=rowGenerationButton, padx=100)

lblGenerationCount = Label(window, text="Количество поколений")
lblGenerationCount.grid(column=0, row=rowGenerationCount, padx=0)
txtGenerationCount = Entry(window,width=10, textvariable=valGenerationCount)
txtGenerationCount.grid(column=1, row=rowGenerationCount, sticky=W, padx=5)
txtGenerationCount.insert(0, 5)


# проверяет введенные данные
def checkInput():
    if comboStartCity.get() not in cities:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Выберете город из выпадающего списка')
    elif valGenerationCount.get().isdigit() == False:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Количество генераций должно быть числом больше нуля')
    elif int(valGenerationCount.get()) <= 0:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Количество генераций должно быть числом больше нуля')
    else:
        return True


# выводит лучшие популяции и красиво выводит результирующую популяцию
def findBestIndividPretty(numberOfPopulations, startCity):
    infoPanel.delete(1.0, END)

    allPopulation = generateInitialPopulation(startCity)
    bestIndivid = allPopulation[0]
    bestGeneration = 1
    for i in range(numberOfPopulations):
        infoPanel.insert(INSERT, "generation ")
        infoPanel.insert(INSERT, (i + 1))
        infoPanel.insert(INSERT, '\n')
        for ind in allPopulation:
            go(startCity, ind)

        for ind in findBestTwo(allPopulation):
            if ind.fitness() > bestIndivid.fitness():
                bestIndivid = ind
                bestGeneration = i + 1
            infoPanel.insert(INSERT, 'coefKm: ')
            infoPanel.insert(INSERT, ('%.3f' %round(ind.coefKilometers, 3)))
            infoPanel.insert(INSERT, "  coefPeople ")
            infoPanel.insert(INSERT, ('%.3f' %round(ind.coefPeople, 3)))
            infoPanel.insert(INSERT, '\n')
            infoPanel.insert(INSERT, "fitness ")
            infoPanel.insert(INSERT, ind.fitness())
            infoPanel.insert(INSERT, '\n')
            break
        infoPanel.insert(INSERT, '\n')
        # print()

        generateNewPopulation(allPopulation)
    infoPanel.insert(INSERT, '\nbest generation:')
    infoPanel.insert(INSERT, '\ngeneration number: ')
    infoPanel.insert(INSERT, bestGeneration)
    infoPanel.insert(INSERT, '\ncoefKm: ')
    infoPanel.insert(INSERT, bestIndivid.coefKilometers)
    infoPanel.insert(INSERT, '\ncoefPeople: ')
    infoPanel.insert(INSERT, bestIndivid.coefPeople)
    infoPanel.insert(INSERT, '\npassed kilometers: ')
    infoPanel.insert(INSERT, bestIndivid.kilometers)
    infoPanel.insert(INSERT, '\npeople vaccinated: ')
    infoPanel.insert(INSERT, int(bestIndivid.peopleVaccinated))
    infoPanel.insert(INSERT, '\nnumber of visited cities: ')
    infoPanel.insert(INSERT, len(bestIndivid.visited))
    infoPanel.insert(INSERT, '\norder of cities: ')
    citiesOrder = []
    for city in bestIndivid.visited:
        citiesOrder.append(cityNameInfected[city][0])
    infoPanel.insert(INSERT, citiesOrder)
    return bestIndivid


#заускает проверку данных и вывод генераций
def findBestIndividButton():
    if not checkInput():
        return
    for key in cityNameInfected:
        if cityNameInfected[key][0] == comboStartCity.get():
            startCity = key
    findBestIndividPretty(int(valGenerationCount.get()), startCity)


btnGenerate = Button(window, text="Сгенерировать", command=findBestIndividButton)
btnGenerate.grid(column=0, row=rowGenerationButton, columnspan=1, padx=5, pady=5)


infoPanel = scrolledtext.ScrolledText(window, width=80, height=29)
infoPanel.grid(column=0, row=rowInfoPanel, columnspan=3, padx=5)
# infoPanel.pack(expand = True, fill=BOTH)


# Эта функция вызывает бесконечный цикл окна, поэтому окно будет ждать любого взаимодействия с пользователем, пока не будет закрыто
window.mainloop()
