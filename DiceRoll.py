import random
from operator import itemgetter
# This is hideous, horribly written code, sorry
# Maybe I'll rewrite it one day, but not today
def GurpsRoll(difficulty):
    d61 = random.randint(1,6)
    d62 = random.randint(1,6)
    d63 = random.randint(1,6)
    total = d61+d62+d63
    if total <= difficulty:
        return " success by **"+str(difficulty-total)+"**("+str(d61)+","+str(d62)+","+str(d63)+")."
    else:
        return " failure by **"+str(total-difficulty)+"**("+str(d61)+","+str(d62)+","+str(d63)+")."
def PrintRoll(roll):
    i = 0
    prev_sep = "+"
    current_num = ""
    roll_result = 0
    dice_num = 1
    raw_roll = ""
    if len(roll) != 0:
        if roll[0] == 'd' or roll[0] == '+' or roll[0] == '-':
            prev_sep = roll[0]
            if prev_sep == "d":
                prev_sep = "+d" 
            i=1
        elif not roll[0].isnumeric():
            return ""
    else:
        return ""
    if not roll[-1].isnumeric():
        return ""
    while i < len(roll):
        if roll[i].isnumeric():
            current_num += roll[i]
        else:
            if len(current_num) == 0 and (roll[i] != "d"  or "d" in prev_sep):
                return ""
    
            if roll[i] == "d":
                if "d" in prev_sep:
                    return ""
                if len(current_num) > 0:
                    dice_num = int(current_num)
                    current_num = ""
                if dice_num == 0:
                    return ""
                prev_sep += "d"

            elif roll[i] == "+" or roll[i] == "-":
                if len(current_num) == 0:
                    return ""
                if "+d" == prev_sep:
                    if (int(current_num) == 0):
                        return ""
                    k = 0
                    while k < dice_num:
                        val = random.randint(1,int(current_num))
                        roll_result += val
                        raw_roll += ("+"+str(val))
                        k+=1
                    current_num = ""
                    dice_num = 1
                elif "-d" == prev_sep:
                    if (int(current_num) == 0):
                        return ""
                    k = 0
                    while k < dice_num:
                        val = random.randint(1,int(current_num))
                        roll_result -= val
                        raw_roll += ("-"+str(roll_result))
                        k+=1
                    current_num = ""
                    dice_num = 1                    
                elif "+" == prev_sep:
                    roll_result += int(current_num)
                    raw_roll += ("+"+current_num)
                    current_num = ""
                elif "-" == prev_sep:
                    roll_result -= int(current_num)
                    raw_roll += ("-"+current_num)
                    current_num = ""
                prev_sep = roll[i]
            else:
                return ""
        i+=1
    if "+d" == prev_sep:
        k = 0
        while k < dice_num:
            val = random.randint(1,int(current_num))
            roll_result += val
            raw_roll += ("+"+str(val))
            k+=1
    elif "-d" == prev_sep:
        k = 0
        while k < dice_num:
            val = random.randint(1,int(current_num))
            roll_result -= val
            raw_roll += ("-"+str(val))      
            k+=1        
    elif "+" == prev_sep:
        roll_result += int(current_num)
        raw_roll += ("+"+current_num)
    elif "-" == prev_sep:
        roll_result -= int(current_num)
        raw_roll += ("-"+current_num)
    if raw_roll[0] == "+":
        raw_roll = raw_roll[1:]
    if roll_result < 0:
        roll_result = 0
    return raw_roll+": "+str(roll_result)

def PrintRollsUnsorted(userin):
    rolls = ""
    cleaned_input = userin.replace(" ","").lower().split(",")
    if len(cleaned_input) == 0:
        return "Error: No Input Given"
    i = 0
    total = 0
    rollArr = []
    while i < len(cleaned_input):
        roll = PrintRoll(cleaned_input[i])
        if len(roll) == 0:
            return "Error: Roll Number " + str(i+1) + " Improperly Formatted"
        indRoll = [int(roll.split(":")[1].replace(" ","")),roll]
        rollArr.append(indRoll)
        rolls += roll + "\n"
        total += int(roll.split(":")[1].replace(" ",""))
        i += 1
    return rolls, total

def PrintRolls(userin):
    rolls = ""
    cleaned_input = userin.replace(" ","").lower().split(",")
    if len(cleaned_input) == 0:
        return "Error: No Input Given"
    i = 0
    total = 0
    rollArr = []
    while i < len(cleaned_input):
        roll = PrintRoll(cleaned_input[i])
        if len(roll) == 0:
            return "Error: Roll Number " + str(i+1) + " Improperly Formatted"
        indRoll = [int(roll.split(":")[1].replace(" ","")),roll]
        rollArr.append(indRoll)
        #rolls += roll + "\n"
        total += int(roll.split(":")[1].replace(" ",""))
        i += 1
    sortedRollArr = sorted(rollArr,key=itemgetter(0))
    for item in sortedRollArr:
        rolls += item[1] + "\n"
    return rolls, total