import math, re, sympy
from fractions import Fraction 

def lcm(lst):  # finds least common multiple in lst
    in_lcm = lst[0]
    for i in lst[1:]:
        in_lcm = abs(in_lcm * i) // math.gcd(in_lcm, i)
    return in_lcm

def arrange(array):
    A,temp = "" , array[-1:][0]
    for i in temp:
        if i.isdigit(): A+=i
        else:
            temp = temp.replace(A, '')
            break
    array[len(array)-1] = A
    array[0]+=temp
    return array

def full_eq_split(full_eq):  # splits inputted string eq to a list of reactants, '-->', and products.
    global r_compounds, p_compounds, r_compounds_wpai, p_compounds_wpai
    initial_list = full_eq.split()   # Splits the strings
    initial_list = list(filter(lambda a: a != '+', initial_list)) # removes all the + from the equation
    n = initial_list.index('-->') # prints position of --> in this list
    r_compounds_wpai = initial_list[:n]  # reactants compunds in this list
    p_compounds_wpai = initial_list[n + 1:] # product compound in this list)
    for w, item in enumerate(initial_list):  # this loop converts Ca3(PO4)2 --> Ca3P2O8 # w - position and item - present at that position
        if '(' in item:  # finds PAIs
            split_pai = re.split('[(-)]', item) # spilts with the brakets
            print(split_pai)
            try:
                if split_pai[0] == '' or (split_pai[len(split_pai)-1][0].isdigit and split_pai[len(split_pai)-1][1].isalpha):
                    split_pai = arrange(split_pai) # solved the issue if bracket is first
            except:
                pass
            first_element = split_pai.pop(0)  # remove first element
            if split_pai[-1] == '':  # gives 1 mutiplier to empty space
                split_pai[-1] = '1'
            #print(split_pai)
            mod = [s for s in re.split("([A-Z][^A-Z]*)", split_pai[0]) if s]  # extract each element with their frequency
            mod_elem = [re.sub('[1-9]', '', x) for x in mod] # only elements
            mod_elem_num = [re.sub('[a-zA-Z]', '', x) for x in mod] # only frequency
            for n, element in enumerate(mod_elem_num):  # n - is the index elements is their frequency
                try:
                    mod_elem_num[n] = str(int(element) * int(split_pai[-1])) # multiplies with each element
                except ValueError:  # when element == ''
                    mod_elem_num[n] = split_pai[-1]
            final_lst = [mod_elem[x] + mod_elem_num[x] for x in range(len(mod_elem))] # array after mutpily with eah element
            final_str = ''.join(final_lst) # convert list into a string
            initial_list[w] = first_element + final_str #adds this to the ccompound
    n = initial_list.index('-->')
    r_compounds = initial_list[:n] # again spilts it into reactants
    p_compounds = initial_list[n + 1:] # and products


global r_compounds, p_compounds, r_compounds_wpai, p_compounds_wpai  # this line made PyCharm happy


def dict_convert(lst_compounds):  # converts compounds into dict. Ex. ['NO2'] --> {N: 1, O: 2}
    joined_str = ''.join(lst_compounds)
    mod = [s for s in re.split("([A-Z][^A-Z]*)", joined_str) if s]
    comp_num_lst = []
    comp_num_lst.extend(mod)
    for item in comp_num_lst:
        t = comp_num_lst.index(item)
        check = any(c.isdigit() for c in item)
        if check is False:
            comp_num_lst[t] = '{}1'.format(comp_num_lst[t])
    length = len(comp_num_lst)
    for item in comp_num_lst:
        match = re.match(r"([a-z]+)([0-9]+)", item, re.I)
        if match:
            items = list(match.groups())
            for element in items:
                comp_num_lst.append(element)
    del comp_num_lst[0:length]
    res_dct = {}
    for i in comp_num_lst:
        x = comp_num_lst.index(i)
        entry = comp_num_lst.pop(x)
        if entry in res_dct:
            res_dct[entry] += int(comp_num_lst[x])
        else:
            res_dct[entry] = int(comp_num_lst[x])
    return res_dct


def get_element_list(r_or_p):  # converts list of compounds to list of the elements in the reaction, w/o cof.
    joined_str = ''.join(r_or_p)
    mod = [s for s in re.split("([A-Z][^A-Z]*)", joined_str) if s]
    comp_num_lst = []
    comp_num_lst.extend(mod)
    for item in comp_num_lst:
        t = comp_num_lst.index(item)
        check = any(c.isdigit() for c in item)
        if check is False:
            comp_num_lst[t] = '{}1'.format(comp_num_lst[t])
    for element in comp_num_lst:
        n = comp_num_lst.index(element)
        mod = ''.join([i for i in element if not i.isdigit()])
        comp_num_lst.remove(element)
        comp_num_lst.insert(n, mod)
    comp_num_lst.sort()
    for element in comp_num_lst:  # removes duplicates
        n = comp_num_lst.index(element)
        try:
            if comp_num_lst[n] == comp_num_lst[n+1]:
                comp_num_lst.remove(element)
        except IndexError:
            pass
    return comp_num_lst


def main_script(eq):
    eq = eq.replace("->", "-->")
    eq = eq.replace("=", "-->")
    eq = eq.replace("→", "-->")
    print(eq)
    full_equation = eq

    full_eq_split(full_equation)  # step 1

    reaction_elements = get_element_list(r_compounds)

    n = len(r_compounds) + len(p_compounds)
    m = len(get_element_list(r_compounds))

    initial_array = [[0] * n for i in range(m)]  # this is the array where RREF will be preformed before values appended
    final_array = [[0] * n for i in range(m)]  # saved for the end

    for item in r_compounds:  # converts compounds in list to dict, then appends cof into array to prepare for RREF
        n = r_compounds.index(item)
        compound_dict = dict_convert(item)
        for key in compound_dict:
            if key in reaction_elements:
                m = reaction_elements.index(key)
                initial_array[m][n] = compound_dict['{}'.format(key)]
            else:
                m = reaction_elements.index(key)
                initial_array[m][n] = 0

    for item in p_compounds:  # same as above but for products' list
        n = p_compounds.index(item) + len(r_compounds)
        compound_dict = dict_convert(item)
        for key in compound_dict:
            if key in reaction_elements:
                m = reaction_elements.index(key)
                initial_array[m][n] = -1 * compound_dict['{}'.format(key)]  # for RREF to work, products have to be * -1
            else:
                m = reaction_elements.index(key)
                initial_array[m][n] = 0

    initial_matrix = sympy.Matrix(initial_array)  # convert array to matrix then RREF
    reduced_matrix = initial_matrix.rref()
    reduced_matrix = list(reduced_matrix[0])

    y = 0  # converts from reduced matrix to a final array
    while True:
        if y == len(reduced_matrix):
            break
        c = y // (n + 1)
        r = y - (c * (n + 1))
        final_array[c][r] = float(reduced_matrix[y])
        y += 1

    n = len(r_compounds) + len(p_compounds)
    m = len(get_element_list(r_compounds))

# At this point, our matrix's results are fractions. The answer works, but fractions aren't expected.
# So, we get lcm of the denominators of those fractions and multiply through by result.
# This gives lowest possible whole number answers.

    denominators = []
    fraction_values = []
    x = 0
    while True:  # extracts denom and fraction values of results into their separate lists
        if x > m - 1:
            break
        insert_den = Fraction(final_array[x][n - 1]).limit_denominator().denominator
        if insert_den != '0':
            denominators.append(insert_den)
        insert_float = Fraction(final_array[x][n - 1]).limit_denominator()
        fraction_values.append(insert_float)
        x += 1

    den_lcm = lcm(denominators)

    coefficient_values = [int(abs(x * den_lcm)) for x in fraction_values]
    for n, item in enumerate(coefficient_values):
        if item == 0:  # if it's 0, means it was a free variable in the RREF matrix
            coefficient_values[n] = den_lcm
    mod_eq = r_compounds_wpai + p_compounds_wpai
    for n, item in enumerate(mod_eq):  # adds cof behind compound to get it ready for ''.join
        try:
            mod_eq[n] = '{}'.format(coefficient_values[n]) + ' ' + item
        except IndexError:
            mod_eq[n] = '{}'.format(den_lcm) + ' ' + item

    for i in range((len(r_compounds_wpai) + len(p_compounds_wpai)) * 2):  # adds the '+' back
        if i % 2 != 0:
            mod_eq.insert(i, ' + ')
    if mod_eq[-1] == ' + ':
        del mod_eq[-1]

    mod_eq.insert(len(r_compounds_wpai) * 2, ' --> ')  # adds the arrow
    del mod_eq[mod_eq.index(' --> ') - 1]

    final_eq = ''.join(mod_eq)
    print(final_eq)
    return (final_eq)


main_script("C + O2 = CO2 + H2O")