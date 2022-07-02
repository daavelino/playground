from lib.logic import *

"""
1. If it didn't rain, Harry visited Hagrid today.
2. Harry visited Hagrid or Dumbledore today, but not both.
3. Harry visited Dumbledore today.
Question: is it raining today?
"""
rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")

knowledge = And(
    Implication(Not(rain), hagrid), 
    Or(hagrid, dumbledore),         
    Not(And(hagrid, dumbledore)),
    dumbledore
    )

print(knowledge.formula())
model_check(knowledge, rain)

