import random

class Creature():

    CreatureType = 'Creature'
    IsAlive = True
    Age = 0                             #measured in days
    DayOfBirth = 0
    NaturalLifespan = 0                 #measured in days
    StarvationTime = 0                  #measured in days
    AccidentalDeathChance = 0           #0-1 probability  
    PredatorEvasionChance = .5          #0-1 probability
    CauseOfDeath = ''
    DayOfDeath = -1
    CaloriesProvided = 0
    
    IsPregnant = False
    PregnancyDuration = 0               #measured in days
    DayOfConception = 0
    MinimumReproductiveAge = 0          #measured in days
    ReproductionChance = 0              #0-1 probability

    IsHungry = True
    PreyCreatures = []                  #list of CreatureTypes that this CreatureType can eat
    PreysOnLivingCreatures = True
    DailyCaloriesNeeded = 0
    DailyCaloriesConsumed = 0

    def GetOlder(self):
        if self.IsAlive == True:
            self.StarvationTime = self.StarvationTime - 1
            self.Age = self.Age+1
            self.DailyCaloriesConsumed = 0
            self.IsHungry = True
            if self.StarvationTime <= 0:
                self.Die('Starvation')
            elif self.NaturalLifespan <= self.Age:
                self.Die('Old Age')
            else:
                DiceRoll = random.uniform(0, 1)
                if DiceRoll <= self.AccidentalDeathChance:
                    self.Die('Accident')

    def Die(self, cause):
        self.IsAlive = False
        self.CauseOfDeath = cause
        self.DayOfDeath = self.DayOfBirth + self.Age

    def GetPregnant(self):
        self.IsPregnant = True
        self.DayOfConception = self.DayOfBirth + self.Age

    def GiveBirth(self):
        self.IsPregnant = False
        
    def Status(self):
        if self.Age == 0 and self.IsAlive == True:
            return self.CreatureType + ' born today!'
        elif self.Age == 0 and self.IsAlive == False and self.CauseOfDeath == 'Eaten':
            return self.CreatureType + ' was Eaten'
        elif self.Age == 0 and self.IsAlive == False:
            return self.CreatureType + ' died at birth'
        elif self.IsAlive:
            return self.CreatureType + ' still alive after ' + str(self.Age) + ' days'
        else:
            return self.CreatureType + ' died of ' + self.CauseOfDeath + ' after ' + str(self.Age) + ' days'

class Human(Creature):

    def __init__(self, day):
        self.CreatureType = 'Human'
        self.DayOfBirth = day
        self.NaturalLifespan = 22000
        self.StarvationTime = 4
        self.AccidentalDeathChance = .001
        self.CaloriesProvided = 10000
        
        self.PregnancyDuration = 10 #300
        self.MinimumReproductiveAge =  10 #6600
        self.ReproductionChance = .8

        self.PreyCreatures = ['Big Fish', 'Small Fish']
        self.DailyCaloriesNeeded = 1200

    def Eat(self, calories):
        self.DailyCaloriesConsumed = self.DailyCaloriesConsumed + calories
        if self.DailyCaloriesConsumed >= self.DailyCaloriesNeeded:
            self.StarvationTime = 4
            self.IsHungry = False

class BigFish(Creature):

    def __init__(self, day):
        self.CreatureType = 'Big Fish'
        self.DayOfBirth = day
        self.NaturalLifespan = 3700
        self.StarvationTime = 2
        self.AccidentalDeathChance = .01
        self.CaloriesProvided = 1000

        self.PregnancyDuration = 5 #90
        self.MinimumReproductiveAge = 4 #400
        self.ReproductionChance = .8

        self.PreyCreatures = ['Small Fish']
        self.DailyCaloriesNeeded = 200

    def Eat(self, calories):
        self.DailyCaloriesConsumed = self.DailyCaloriesConsumed + calories
        if self.DailyCaloriesConsumed >= self.DailyCaloriesNeeded:
            self.StarvationTime = 2
            self.IsHungry = False

class SmallFish(Creature):

    def __init__(self, day):
        self.CreatureType = 'Small Fish'
        self.DayOfBirth = day
        self.NaturalLifespan = 2000
        self.StarvationTime = 2
        self.AccidentalDeathChance = .01
        self.CaloriesProvided = 300

        self.PregnancyDuration = 3 #50
        self.MinimumReproductiveAge = 2 #200
        self.ReproductionChance = .8

        self.PreyCreatures = ['Microbe']
        self.DailyCaloriesNeeded = 10

    def Eat(self, calories):
        self.DailyCaloriesConsumed = self.DailyCaloriesConsumed + calories
        if self.DailyCaloriesConsumed >= self.DailyCaloriesNeeded:
            self.StarvationTime = 2
            self.IsHungry = False

class Microbe(Creature):

    def __init__(self, day):
        self.CreatureType = 'Microbe'
        self.DayOfBirth = day
        self.NaturalLifespan = 100
        self.StarvationTime = 2
        self.AccidentalDeathChance = .01
        self.PredatorEvasionChance = .1
        self.CaloriesProvided = 4

        self.PregnancyDuration = 2
        self.MinimumReproductiveAge = 2 #5
        self.ReproductionChance = .8

        self.PreyCreatures = ['Microbe', 'Small Fish', 'Big Fish', 'Human']
        self.PreysOnLivingCreatures = False
        self.DailyCaloriesNeeded = 2

    def Eat(self, calories):
        self.DailyCaloriesConsumed = self.DailyCaloriesConsumed + calories
        if self.DailyCaloriesConsumed >= self.DailyCaloriesNeeded:
            self.StarvationTime = 25
            self.IsHungry = False
