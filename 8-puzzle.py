# Permutations ('sigma') are implemented as dictionaries (basically two-row notation),
# e.g., {1:3, 2:1, 3:2, 4:4, 5:5, 6:6, 7:8} maps 1 to 3, etc.
# Cycles are implented as lists, e.g. [1, 3, 2] is the 3-cycle (1 3 2).

n = 8
domain = range(1, n+1)
identity = {i:i for i in domain} # identity map

def next_element(cycle, element): # return the image of an element in a cycle
    assert(element in cycle)
    index = cycle.index(element)
    next_element = cycle[(index + 1) % len(cycle)]
    return(next_element)

def permutation(cycle): # convert a cycle to a permutation 
    sigma = {i:i for i in domain} # identity map
    for element in cycle:
        sigma[element] = next_element(cycle, element)
    return sigma

def cycle_decomp(sigma): # return a list of disjoint cycles of length > 1 whose product is sigma
    # First check if sigma is a cycle and convert to a permutation if necessary:
    if type(sigma) == list:
        sigma = permutation(sigma)    
    cycles = []
    while sigma:
        # Find the first cycle:
        first_element = next(iter(sigma)) 
        cycle = [first_element]
        next_element = sigma[first_element]
        while next_element != first_element:
            cycle.append(next_element)
            next_element = sigma[next_element]
        # Add cycle to list unless its length is 1:
        if len(cycle) > 1:
            cycles.append(cycle)
        # Truncate sigma:
        sigma = {i:sigma[i] for i in sigma if i not in cycle}
    return cycles

def transposition_decomp(sigma): # return a list of transpositions whose product is sigma
    if type(sigma) == list: # i.e., if sigma is a cycle
        return [ [sigma[0], element] for element in reversed(sigma[1:]) ] # see proof of 5.4
    # Make a list containing the transpositions that make up the cycles in sigma:
    transpositions = []
    for cycle in cycle_decomp(sigma):
        transpositions += transposition_decomp(cycle)
    return transpositions

def sign(sigma):
    return pow(-1, len(transposition_decomp(sigma)))

def three_cycle_decomp(sigma): # return a list of 3-cycles whose product is sigma
    assert( sign(sigma) == 1 )
    transpositions = transposition_decomp(sigma)
    cycles = []
    for i in range(0, len(transpositions)-1, 2): # looping in steps of 2
        (a, b) = transpositions[i]
        (c, d) = transpositions[i+1]
        # Write the product of (a b) and (c d) as a product of 3-cycles by cases:
        if {a, b} & {c, d} == set(): # disjoint transpositions
            new_cycles = [[a, b, c], [b, c, d]]
        if a == c:
            new_cycles = [[a, d, b]]
        if a == d:
            new_cycles = [[a, c, b]]
        if b == c:
            new_cycles = [[a, b, d]]
        if b == d:
            new_cycles = [[a, b, c]]
        cycles += new_cycles
    return cycles

def compose(sigma, tau): # return the product of two permutations (or cycles)
    # First check if sigma or tau is a cycle and convert to a permutation if necessary:
    if type(sigma) == list:
        sigma = permutation(sigma)
    if type(tau) == list:
        tau = permutation(tau)
    return {i:sigma[tau[i]] for i in domain}

def product(permutations): # return the product of a list of permutations (or cycles)
    product = identity 
    for sigma in permutations:
        product = compose(product, sigma)
    return product

# Sample usage:

alpha = [5, 6, 1, 4, 2]
sigma = {1:2, 2:3, 3:1, 4:4, 5:5, 6:6, 7:7, 8:8}
tau = {1:2, 2:4, 3:5, 4:1, 5:3, 6:6, 7:8, 8:7}

print(three_cycle_decomp(alpha))
print(three_cycle_decomp(sigma))
print(three_cycle_decomp(tau))
