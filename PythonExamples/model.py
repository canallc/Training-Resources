from pyomo.environ import * # For Pyomo 4.0 & later

model = AbstractModel()

## Define sets
model.Spas = Set()
model.Supplies = Set()

## Define parameters
model.profits = Param(model.Spas)
model.available = Param(model.Supplies)
model.required = Param(model.Spas, model.Supplies)

## Define variables
model.numberToMake = Var(model.Spas, within = NonNegativeIntegers)

## Define Objective Function
def totalProfitRule(model):
   return sum(model.profits[i] * model.numberToMake[i] for i in model.Spas)
model.SolverResult=Objective(rule=totalProfitRule, sense=maximize)

## Satisfy availability
def AvailabilityRule(model,supplies):
    return sum(model.numberToMake[i]*model.required[i,supplies] for i in model.Spas) <= model.available[supplies]
model.availabilityConstraint = Constraint(model.Supplies, rule=AvailabilityRule)
