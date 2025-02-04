#identity: عضو خنثی
#closure: شرکت پذیری
#inverse: وارون
#associative: شرکت پذیری
def find_identity(table, elements):
    """Find the identity element, if it exists.
    The identity element is an element e such that for every element a in the set,
    applying the operation should return a (e * a = a and a * e = a)."""
    for e in elements:
        valid = True
        for a in elements:
            if table[e][a] != a or table[a][e] != a:
                valid = False #if any condition fails, it's not an identity
                break
        if valid:
            return e
    return None  

def is_closed(table, elements):
    """Check if the operation table is closed over the set. 
    This means that applying the operation on any two elements should give another element in the set."""
    for i in elements:
        for j in elements:
            if table[i][j] not in elements:
                return False  # If any result is outside the set, it's not closed
    return True

def has_inverses(table, elements, identity):
    """Check if each element has an inverse.
    An element a has an inverse b if a * b = identity and b * a = identity."""
    for a in elements:
        found_inverse = False  #false means assume no inverse until proven otherwise
        for b in elements:
            if table[a][b] == identity and table[b][a] == identity:
                found_inverse = True  #true means found an inverse for a
                break
        if not found_inverse:
            return False 
    return True


def is_associative(table, elements):
    """Check associativity: (a * b) * c == a * (b * c) for all elements.
    This means that grouping of operations does not affect the result."""
    for a in elements:
        for b in elements:
            for c in elements:
                if table[table[a][b]][c] != table[a][table[b][c]]:
                    return False
    return True


def generate_operations(n):
    """Generate all possible operation tables for a set of size n without using itertools.
    This function creates all possible ways elements in the set can interact under an operation."""
    elements = list(range(n))  # The set contains numbers from 0 to n-1
    
    def generate_tables(index=0, current_table=None):
        if current_table is None:
            #initialize a table with placeholder values (-1 means unfilled)
            current_table = []
            for _ in range(n):
                row = [-1] * n  #create a row of n elements, all set to -1
                current_table.append(row)
        
        if index == n * n:
            copied_table = []
            for row in current_table:
                copied_table.append(row[:])  #create an empty copy of each row
            yield copied_table  #returns a deep copy of the table when complete
            return
        
        row, col = divmod(index, n)  #convert index into row and column position
        for value in elements:
            current_table[row][col] = value  #assign a value to the table position
            yield from generate_tables(index + 1, current_table)  # Move to the next index
    
    yield from generate_tables()


def find_distinct_groups_and_total_operations(n):
    """Find and count all distinct groups of order n and count valid operations.
    This checks all possible operation tables and filters those that satisfy group properties."""
    elements = list(range(n))
    unique_groups = []
    total_operations = 0
    
    for table in generate_operations(n):
        total_operations += 1
        if is_closed(table, elements) and is_associative(table, elements):#check closure and associativity
            identity = find_identity(table, elements)#find identity element if it exists
            if identity is not None and has_inverses(table, elements, identity):#check for inverses
                unique_groups.append(table)
    
    return unique_groups, total_operations


#baraye har n run mikone:
n = int(input("Please enter the amount of n:" + "\n"))
import datetime
clock = datetime.datetime.now()
groups, total_operations = find_distinct_groups_and_total_operations(n)
print(datetime.datetime.now() - clock)
print(f"Number of distinct groups for n={n}: {len(groups)}")
print(f"Total number of operation tables generated: {total_operations}")
