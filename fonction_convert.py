import config_fr

SPECIAL_NUMBERS_NAMES = config_fr.SPECIAL_NUMBERS_NAMES
TEN_POWERS_NAMES = config_fr.TEN_POWERS_NAMES
 

for i in range(0,10):
    SPECIAL_NUMBERS_NAMES['0' + str(i)] = SPECIAL_NUMBERS_NAMES[str(i)]

for i in range(7, 10):
    SPECIAL_NUMBERS_NAMES['1' + str(i)] = "dix-" + SPECIAL_NUMBERS_NAMES[str(i)]

for i in range(2, 7):
    SPECIAL_NUMBERS_NAMES[str(i) + '1'] = SPECIAL_NUMBERS_NAMES[str(i) + '0'] + "-et-un"

SPECIAL_NUMBERS_NAMES['71'] = "soixante-et-onze"

for i in range(2, 10):
    SPECIAL_NUMBERS_NAMES[str(i) + '00'] = SPECIAL_NUMBERS_NAMES[str(i)] + "-cents"

TEN_PREFIXES = {}
for i in range(2, 10):
    if i == 7:
        TEN_PREFIXES[str(i)] = SPECIAL_NUMBERS_NAMES[str(i-1) + '0'] + "-"
    elif i == 8:
        TEN_PREFIXES[str(i)] = SPECIAL_NUMBERS_NAMES[str(i) + '0'][:-1] + "-"
    elif i == 9:
        TEN_PREFIXES[str(i)] = SPECIAL_NUMBERS_NAMES[str(i-1) + '0'][:-1] + "-"
    else:
        TEN_PREFIXES[str(i)] = SPECIAL_NUMBERS_NAMES[str(i) + '0'] + "-"

THE_POWERS = {}
MAX_POWER = {}
THE_BIGGER_NAME = {}
 
for oneConvention in TEN_POWERS_NAMES:

    THE_POWERS[oneConvention] = sorted([0] + [ x for x in TEN_POWERS_NAMES[oneConvention] if x != 3 ])
    MAX_POWER[oneConvention] = THE_POWERS[oneConvention][-1]
    THE_BIGGER_NAME[oneConvention] = TEN_POWERS_NAMES[oneConvention][ THE_POWERS[oneConvention][-1] ]

def orderMagnitude(number):
    """
    For example, 123456 becomes 123000, and 12345 becomes 12000
    """
    l = len(number) // 3
    i = len(number) - 3*l
 
    if i == 0:
        i += 3
        l -= 1
 
    return number[:i] + '0'*l*3
 
 
def floor(number, tenPowerPrecision = 0):
    """
    This function changes the tenPowerPrecision right digits with zeros.
    """
    if type(tenPowerPrecision) != int or \
            tenPowerPrecision < 0:
        raise ValueError("""tenPowerPrecision = "' + str(tenPowerPrecision) + '" is not allowed.
 
tenPowerPrecision can only be equal to a natural n with 10^n is the precision needed.
""")
    number = str(number)
 
    if tenPowerPrecision > 0 and len(number) > tenPowerPrecision:
        number = number[:len(number) - tenPowerPrecision] + '0'*(tenPowerPrecision)
 
    return number
 
 
def cleanInteger(number):
    """
    None is return when the number is not an integer.
    """
 
    number = str(number).replace(' ', '')
 
    test = number
    for i in range(10):
        test = test.replace(str(i), '')
 
    if test:
        return None
 
    return number
 
 
def boringFrenchGrammaticalRuleForCENT(litteralNumber):
    if litteralNumber[-5:] == 'cents':
        litteralNumber = litteralNumber[:-1]
    return litteralNumber
 
 
def printer(number, checkValidity = True, convention = "everyday"):
    if checkValidity:
        if convention not in TEN_POWERS_NAMES:
            raise ValueError('convention = "' + str(convention) + '" is unknown.')
        number = cleanInteger(number)
        if not number:
            raise ValueError('number = "' + str(number) + '" is not an integer.')

    if number in SPECIAL_NUMBERS_NAMES:

        answer = SPECIAL_NUMBERS_NAMES[number]
 
        if answer == TEN_POWERS_NAMES[convention][6]:
            answer = 'un ' + answer
 
        return answer

    if len(number) == 2:
        if number[0] in ['7', '9']:
            return  TEN_PREFIXES[number[0]] + SPECIAL_NUMBERS_NAMES['1' + number[1]]
        else:
            return  TEN_PREFIXES[number[0]] + SPECIAL_NUMBERS_NAMES[number[1]]

    if len(number) == 3:
        if number[0] == '0':
            hundredName = ''
        else:
            hundredName = SPECIAL_NUMBERS_NAMES['100']
            if number[0] != '1':
                hundredName = SPECIAL_NUMBERS_NAMES[number[0]] + '-' + hundredName
            hundredName += '-'
 
        return hundredName + printer( number = number[1:],
                                   checkValidity = False )

    ten_powers_names = TEN_POWERS_NAMES[convention]

    if len(number) <= 6:
        hundredPart = printer( number = number[-3:],
                               checkValidity = False )
# We can have 123000.
        if hundredPart == SPECIAL_NUMBERS_NAMES['0']:
            hundredPart = ''
        else:
            hundredPart = ' ' + hundredPart
 
        thousandPart = printer( number = number[:-3],
                                checkValidity = False )
 

        if thousandPart == SPECIAL_NUMBERS_NAMES['0']:
            thousandPart = ''
        elif thousandPart == SPECIAL_NUMBERS_NAMES['1']:
            thousandPart = ten_powers_names[3]
        else:

            thousandPart = boringFrenchGrammaticalRuleForCENT(thousandPart) + ' ' + ten_powers_names[3]
 
        return thousandPart + hundredPart

    the_powers = THE_POWERS[convention]
    max_power = MAX_POWER[convention]
    len_number = len(number)
 
    if len_number <= max_power:
        answer = printer( number = number[-the_powers[1]:],
                          checkValidity = False )

        if answer == SPECIAL_NUMBERS_NAMES['0']:
            answer = ''
 
        for i in range(1, len(the_powers) - 1):
            if the_powers[i] > len_number:
                break
 
            numberOfIntermediatePart = printer( number = number[-the_powers[i+1]:-the_powers[i]],
                                                checkValidity = False )

            if numberOfIntermediatePart not in [SPECIAL_NUMBERS_NAMES['0'], '']:

                numberOfIntermediatePart = boringFrenchGrammaticalRuleForCENT(numberOfIntermediatePart)
 
                if numberOfIntermediatePart == SPECIAL_NUMBERS_NAMES['1']:
                    numberOfIntermediatePart += ' ' + ten_powers_names[the_powers[i]]
                else:
                    numberOfIntermediatePart += ' ' + ten_powers_names[the_powers[i]] + 's'
 
                if answer:
                    answer =  numberOfIntermediatePart + ' ' + answer
                else:
                    answer =  numberOfIntermediatePart
 
        return answer

    theBiggerName = THE_BIGGER_NAME[convention]
    currentBigPartName = ''
 
    answer = printer( number = number[-max_power:],
                      checkValidity = False )
    number = number[:-max_power]

    if answer == SPECIAL_NUMBERS_NAMES['0']:
        answer = ''
 
    while(number):
        numberOfIntermediatePart = printer( number = number[-max_power:],
                                            checkValidity = False )
        number = number[:-max_power]
 

        if numberOfIntermediatePart not in [SPECIAL_NUMBERS_NAMES['0'], '']:

            numberOfIntermediatePart = boringFrenchGrammaticalRuleForCENT(numberOfIntermediatePart)
 
            if numberOfIntermediatePart == SPECIAL_NUMBERS_NAMES['1']:
                numberOfIntermediatePart += ' ' + theBiggerName + currentBigPartName

            else:
                for onePower in ten_powers_names:
                    if onePower != 3:
                        nameToTest = ten_powers_names[onePower]
                        l = len(nameToTest)
 
                        if numberOfIntermediatePart[-l:] == nameToTest or \
                        numberOfIntermediatePart[-l-1:] == nameToTest + 's':
                            numberOfIntermediatePart += ' de'
                            break
 
                numberOfIntermediatePart += ' ' + theBiggerName + 's' + currentBigPartName
 
            if answer:
                answer =  numberOfIntermediatePart + ' ' + answer
            else:
                answer =  numberOfIntermediatePart
 
        currentBigPartName += ' de ' + theBiggerName + 's'
 
    return answer

if __name__ == '__main__':
    myConvention ="everyday"
    myConvention1 ="rowlett"
    myConvention2 ="chuquet"
 
    mytenPowerPrecision = 0
    onlyTheOrderOfMagnitude = True
 
    randomTest = True
    randomTest1 = False
    nMin = 0
    nMax = 10**18-1
    nbOfTest = 5   
 
    if randomTest:
       import random
       nMax += 1
       Nombre = [random.randint(nMin, nMax) for x in range(nbOfTest)]
       
       print(str(Nombre))
 
       Nombre = str(Nombre).strip().replace(' ', '')

                    
