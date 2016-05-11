import random
import timeit
import time
import configparser
import os
from classfiles.CreatureClasses import *


class EcoSim():
    CreatureList = []
    DayCount = 100000
    AirTemperature = 75
    RunTimer = 0
    FoodTimer = 0
    SexTimer = 0

    def __init__(self):
        print('EcoSim started on', time.strftime('%b %d, %Y at %I:%M:%S %p'))
        print('Program running from', os.path.dirname(__file__))
        config = configparser.ConfigParser()
        config.read('./conf/creaturepopulations.conf')

        IntialBirthPopulations = config['INITIAL BIRTH POPULATIONS']
        for count in range(0,int(IntialBirthPopulations['MicrobeCount'])): #30000
            x = Microbe(self.DayCount)
            self.CreatureList.append(x)
        for count in range(0,int(IntialBirthPopulations['SmallFishCount'])): #800
            x = SmallFish(self.DayCount)
            self.CreatureList.append(x)
        for count in range(0,int(IntialBirthPopulations['BigFishCount'])):   #50
            x = BigFish(self.DayCount)
            self.CreatureList.append(x)
        for count in range(0,int(IntialBirthPopulations['HumanCount'])): #3
            x = Human(self.DayCount)
            self.CreatureList.append(x)

        InitialAdultPopulations = config['INITIAL ADULT POPULATIONS']
        for count in range(0,int(InitialAdultPopulations['MicrobeCount'])): #30000
            x = Microbe(self.DayCount - 5)
            self.CreatureList.append(x)
        for count in range(0,int(InitialAdultPopulations['SmallFishCount'])): #800
            x = SmallFish(self.DayCount - 5)
            self.CreatureList.append(x)
        for count in range(0,int(InitialAdultPopulations['BigFishCount'])):   #50
            x = BigFish(self.DayCount - 10)
            self.CreatureList.append(x)
        for count in range(0,int(InitialAdultPopulations['HumanCount'])): #3
            x = Human(self.DayCount - 25)
            self.CreatureList.append(x)
            
        InitialNonlivingPopulations = config['INITIAL NONLIVING POPULATIONS']
        for count in range(0,int(InitialNonlivingPopulations['MicrobeCount'])): #30000
            x = Microbe(0)
            x.Die('Old Age')
            x.DayOfDeath = self.DayCount
            self.CreatureList.append(x)
        for count in range(0,int(InitialNonlivingPopulations['SmallFishCount'])): #800
            x = SmallFish(0)
            x.Die('Old Age')
            x.DayOfDeath = self.DayCount
            self.CreatureList.append(x)
        for count in range(0,int(InitialNonlivingPopulations['BigFishCount'])):   #50
            x = BigFish(0)
            x.Die('Old Age')
            x.DayOfDeath = self.DayCount
            self.CreatureList.append(x)
        for count in range(0,int(InitialNonlivingPopulations['HumanCount'])): #3
            x = Human(0)
            x.Die('Old Age')
            x.DayOfDeath = self.DayCount
            self.CreatureList.append(x)

        print('Initial Populations:')
        self.GetCreatureTally()
        rt = timeit.Timer(lambda: self.RunSimForXDays(5))
        self.RunTimer = rt.timeit(1)
        print('Simulation ran for a total of', self.RunTimer, 'seconds')

    def GetCreatureTally(self):
        TypeList = ['Microbe', 'Small Fish', 'Big Fish', 'Human']
        for cType in TypeList:
            cList = [c for c in self.CreatureList if c.CreatureType == cType]
            DiedCount = 0
            EatenCount = 0
            StarveCount = 0
            OldAgeCount = 0
            AccidentCount = 0
            AliveCount = 0
            BornCount = 0
            for creature in cList:
                if creature.IsAlive == False:
                    if creature.DayOfDeath == self.DayCount:
                        DiedCount += 1
                        if creature.CauseOfDeath == 'Predation':
                            EatenCount += 1
                        elif creature.CauseOfDeath == 'Starvation':
                            StarveCount += 1
                        elif creature.CauseOfDeath == 'Old Age':
                            OldAgeCount += 1
                        elif creature.CauseOfDeath == 'Accident':
                            AccidentCount += 1
                    if creature.CauseOfDeath == 'Predation':
                        self.CreatureList.remove(creature)
                else:
                    AliveCount += 1
                    if creature.DayOfBirth == self.DayCount:
                        BornCount += 1
            print(DiedCount, 'deaths (', EatenCount, 'were eaten,', StarveCount, 'starved,', OldAgeCount, 'were too old, and', AccidentCount, 'had an accident) and', BornCount, 'births leaves', AliveCount, cType, 'creatures alive')

    def NextDay(self):
        self.DayCount = self.DayCount + 1
        for creature in self.CreatureList:
            creature.GetOlder()

    def RunSimForXDays(self, DaysToRun):
        for count in range(0,DaysToRun):
            LivingCreatureList = [c for c in self.CreatureList if c.IsAlive == True]
            if len(LivingCreatureList) > 0:
                print('Day', self.DayCount - 100000, 'summary:')
                self.FoodAndSex()
                print('Eating took', self.FoodTimer, 'sec')
                print('Sex took', self.SexTimer, 'sec')
                self.GetCreatureTally()
                self.NextDay()
            else:
                break

    def FoodAndSex(self):
        random.shuffle(self.CreatureList)
        self.FoodTimer = 0
        self.SexTimer = 0
        OptimizationList = [p for p in self.CreatureList if p.IsAlive == False and p.CauseOfDeath != 'Predation']
        for creature in self.CreatureList:
            if creature.CreatureType == 'Microbe':
                if len(OptimizationList) > 0:
                    if creature.IsAlive == True:
                        ft = timeit.Timer(lambda: self.EatSomething(creature))
                        self.FoodTimer += ft.timeit(1)
            else:
                if creature.IsAlive == True:
                    ft = timeit.Timer(lambda: self.EatSomething(creature))
                    self.FoodTimer += ft.timeit(1)
            if creature.IsAlive == True:
                st = timeit.Timer(lambda: self.Reproduce(creature))
                self.SexTimer += st.timeit(1)
                
    def EatSomething(self, hungryCreature):
        PreyList = [p for p in self.CreatureList if p.CreatureType in hungryCreature.PreyCreatures and
                    p.IsAlive == hungryCreature.PreysOnLivingCreatures and
                    p.CauseOfDeath != 'Predation' and
                    p != hungryCreature]
        AttemptedPredations = 0
        while hungryCreature.IsHungry == True and len(PreyList) > 0 and AttemptedPredations < 10:
            for creature in PreyList:
                if hungryCreature.IsHungry == True and AttemptedPredations < 10: 
                    DiceRoll = random.uniform(0, 1)
                    AttemptedPredations += 1
                    if DiceRoll > creature.PredatorEvasionChance:
                        hungryCreature.Eat(creature.CaloriesProvided)
                        creature.Die('Predation')
                        PreyList.remove(creature)
                else:
                    break

    def Reproduce(self, hornyCreature):
        if hornyCreature.IsPregnant:
            if hornyCreature.Age >= hornyCreature.DayOfConception + hornyCreature.PregnancyDuration:
                hornyCreature.GiveBirth()
                if hornyCreature.CreatureType == 'Human':
                    self.CreatureList.append(Human(self.DayCount))
                elif hornyCreature.CreatureType == 'Big Fish':
                    self.CreatureList.append(BigFish(self.DayCount))
                elif hornyCreature.CreatureType == 'Small Fish':
                    self.CreatureList.append(SmallFish(self.DayCount))
                elif hornyCreature.CreatureType == 'Microbe':
                    self.CreatureList.append(Microbe(self.DayCount))
        else:
            if hornyCreature.Age >= hornyCreature.MinimumReproductiveAge:
                DiceRoll = random.uniform(0, 1)
                if DiceRoll <= hornyCreature.ReproductionChance:
                    hornyCreature.GetPregnant()
