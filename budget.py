class Category:
  name = ""
  ledger = list()
  
  def __init__(self, nameInput):
    self.name = formatName(nameInput)
    self.ledger = []
    #print(self.name, "constructed")

  def __del__(self):
    pass #print(self.name, "destructed")

  def get_balance(self):
    balance = 0
    for mov in self.ledger: balance += mov["amount"]
    return balance

  def check_funds(self, amount):
    balance = self.get_balance()
    return amount <= balance
  
  def deposit (self, amount, description = ""):
    self.ledger.append({ "amount": amount, "description": description })

  def withdraw (self, amount, description = ""):
    if self.check_funds(amount):
      self.deposit(amount.__neg__(), description)
      return True
    return False

  def transfer (self, amount, budgetCategory):
    if self.check_funds(amount):
      self.withdraw(amount, "Transfer to " + budgetCategory.name)
      budgetCategory.deposit(amount, "Transfer from " + self.name)
      return True
    return False

  def __str__(self):
    title = self.name.center(30, "*")
    ledgerLimit = len(self.ledger)
    movements = ""
    for k,v in enumerate(self.ledger):
      movements += v["description"][0:23].ljust(23, " ") + getSevenDigitsNumber(v["amount"]).rjust(7, " ")
      if k+1 == ledgerLimit: break
      movements += "\n"
    total = "Total: " + formatInTwoDecimals(self.get_balance())
    return title + "\n" + movements + "\n" + total

######################################################
######## class Category: AUXILIARY FUNCTIONS #########
######################################################
def formatInTwoDecimals(n):
  return "%0.2f"%(n) # or return "{:0.2f}".format(n)

def getSevenDigitsNumber(n):
  sNumber = formatInTwoDecimals(n)
  length = len(sNumber)
  if len(sNumber) <= 7: return sNumber
  else: return ">7char" #return sNumber[length-7 : length]

def formatName(name):
  return name.lower().capitalize()
######################################################




#def create_spend_chart(categories):
def create_spend_chart(categoryList):

  # creates new dictionary list format:
  #   [ { "name", "percentage" }, ...]
  # sorted by most spent percentage (descending)
  percentagesDictList = createSortedCategoryPercentagesDictList(categoryList)

  # construct individual parts
  title = "Percentage spent by category"
  percentages = constructChartPercentages(percentagesDictList)
  dashes = constructChartHorizontalDashes(percentagesDictList)
  labels = constructChartNameLabels(percentagesDictList)

  # construct chart
  chart = title+"\n" + percentages+"\n" + dashes+"\n" + labels

  return chart

######################################################
######## chart function: AUXILIARY FUNCTIONS #########
######################################################
def getTotalSpent(budgetCategory):
  total = 0
  for mov in budgetCategory.ledger:
    if mov["amount"] < 0: total += mov["amount"]
  return total

def getTotalSpentFromCategoryList(categoryList):
  total = 0
  for cat in categoryList:
    total += getTotalSpent(cat)
  return total

def roundDownPercentageToNearest10(n):
  return ((n/10).__trunc__()) * 10

def getPercentageFromTotalSpent(budgetCategory, categoriesTotalSpent):
  catTotalSpent = getTotalSpent(budgetCategory)
  totalPercentage = (catTotalSpent / categoriesTotalSpent) * 100
  return roundDownPercentageToNearest10( totalPercentage )


# creates list of dictionaries {} with the categories's name and calculated spend percentage: [ { "name", "percentage" }, ...]
def createSortedCategoryPercentagesDictList(categoryList):
  l = list()
  categoriesTotalSpent = getTotalSpentFromCategoryList(categoryList)
  for c in categoryList:
    percentage = getPercentageFromTotalSpent(c, categoriesTotalSpent)
    l.append( { "name": c.name, "percentage": percentage } )
  return l
  #return sortPercentagesDictListByMostSpentDescending(l)

def sortPercentagesDictListByMostSpentDescending(percentagesList):
  return sorted(percentagesList, key=lambda item: item["percentage"], reverse=True)

def getMaxCategoryNameLengthFromSortedPercentagesDictList(percentagesList):
  maxNameLengthDict = max(percentagesList, key=lambda item: len(item["name"]))
  return len(maxNameLengthDict["name"])

def constructChartPercentages(percentagesList):
  percentagesPart = ""
  value = "o  "
  empty = "   "
  percentage = 100
  while percentage >= 0:
    percentagesPart += str(percentage).rjust(3, " ") + "| "
    for item in percentagesList:
      if item["percentage"] >= percentage:
        percentagesPart += value
      else:
        percentagesPart += empty
    if percentage-10 >= 0: percentagesPart += "\n"
    percentage -= 10
  return percentagesPart

def constructChartHorizontalDashes(percentagesList):
  dashesPart = ""
  dashDiv = "-".rjust(5, " ")
  dashesPart += dashDiv
  for item in percentagesList:
    dashesPart += "---"
  return dashesPart

def constructChartNameLabels(percentagesList):
  labelsPart = ""
  labelDiv = "".rjust(5, " ")
  empty = "   "
  labelMaxHeight = getMaxCategoryNameLengthFromSortedPercentagesDictList(percentagesList)
  letterIndex = 0
  while letterIndex < labelMaxHeight:
    labelsPart += labelDiv
    for item in percentagesList:
      if letterIndex < len(item["name"]):
        labelsPart += item["name"][letterIndex] + "  "
      else:
        labelsPart += empty
    if letterIndex+1 < labelMaxHeight: labelsPart += "\n"
    letterIndex += 1
  return labelsPart
######################################################