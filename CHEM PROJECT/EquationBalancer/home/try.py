import re
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

