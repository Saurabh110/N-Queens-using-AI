import copy
import sys
import time


number_of_solutions = 0                                                        # Counter for Number of Solutions
number_of_backtracks = 0                                                       # Counter for Number of Backtracks

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QueenGraph:                                                              # Class representing the problem                                                                        
    def __init__(self):
        self.neighbours = []                                                   # Neighbors for each queen 
        self.N = int(sys.argv[2])                                              # N is total number of queens 
        self.all_dom = []
        self.all_arcs = []
        for i in range(1,self.N+1):
            self.all_dom.append(copy.deepcopy(list(range(1,int(sys.argv[2])+1))))   # Domains of all queens initialized
            temp = []
            for j in range(1,self.N+1):
                if i==j:
                    continue
                temp.append(j)
            self.neighbours.append(copy.deepcopy(temp))                        # Initialized Neighbours for each queen 
        
        for i in range(0,self.N):
            for j in self.neighbours[i]:  
                self.all_arcs.append([i+1,j])                                  # Every arc between two queens is in all_arcs
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def print_to_Cfile(N,all_dom):                                                 # Prints Cfile 
    constraints1 = ''
    constraints2 = ''
    variables = ""
    domains_to_print = ""
    for i in range(1, N+1):
        constraints1 += "Q"+str(i)+" != "
        variables+= "Queen"+str(i)+" --->"+" Q"+str(i)+"\n"
        domains_to_print += "Q"+str(i)+" ---> "+ str(all_dom[i-1]) + "\n"
        for j in range(i+1,N+1):
            if j ==i+1:
                constraints2+="Constraints with Queen"+str(i)+ "-->"
            constraints2+= " [Q"+str(i)+" - Q"+str(j)+" != " + str(abs(i-j)) + "]  "
        constraints2+="\n"
    constraints1 = constraints1[:-4] + "\n"
    f = open(sys.argv[3], "w")
    print("Variables: \n" + variables,file=f)
    print("\nDomains: \n" + domains_to_print,file=f)
    print("\nConstraints: \n" + constraints1, file=f)
    print( constraints2, file=f)
    f.close()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def print_to_Rfile(solution,N):                                                # Prints Rfile                     
    if number_of_solutions == 1:
        f = open(sys.argv[4], "w")
        print("Printing solutions for \'"+str(N)+"-Queens\' using \'"+sys.argv[1]+"\' \n\n",file=f)
    else:
        f = open(sys.argv[4], "a")
    temp_list = solution.split(",")
    temp_list.pop(0)
    print_str ="SOLUTION: "+ str(number_of_solutions)+"\n"
    
    for i in range(1,N+1):
        print_str = print_str + "Q"+str(i)+"--->" + str(temp_list[i-1])+"\n"
    
    print_str +="\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    
    for i in range(1,N+1):
        for j in range(1,N+1):
            if j == int(temp_list[i-1]):
#                print(" \'Q"+str(i)+"\'",end = '')
                if i>9:
                    print_str +=" \'Q"+str(i)+"\'"
                else:
                    print_str +=" \'Q"+str(i)+"\' "
            else:
#                print(" ----",end = '')
                print_str +=" ---- "
#        print("\n")
        print_str+="\n\n"
    
    print_str += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    print_str += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    print(print_str, file=f)
    f.close()
    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def FOR (queen, curr_placement, domains, N):                                   # Forward Checking 
    domains = copy.deepcopy(domains)
    for i in range(queen+1,N):                                                 # Queen+1 because we have to check constraints of next remaining queens
        try:
            domains[i].remove(curr_placement)                                  # Remove value of current_placement of previous queen from next remaining queens' domains
        except ValueError:                                                     # Try-Catch to catch error if value is already removed                   
            pass
        each= 0                                                                # each is used to keep track of current position in the domain currently being checked 
        while True:
            if each == len(domains[i]):                                        # Break if every element of the domain is checked 
                break
            if abs(curr_placement - domains[i][each]) == abs(queen - i):       # Logic to remove diagonal inconsistancy 
                domains[i].remove(domains[i][each])
                each-=1
            each+=1
        if domains[i] == []:                                                   # Return False if current domain gets empty 
            global number_of_backtracks
            number_of_backtracks+=1                                            # Increase the number of backtracks 
            return False

        
    return copy.deepcopy(domains)                                              # Return updated domains 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def BackTracking (number_of_queen, received_domains, final_solution, N, flag_for_solution,neighbours,all_arcs):
    global number_of_solutions
    
    
#~~~~~~ Comment this if loop to get Count of TOTAL POSSIBLE SOLUTIONS ~~~~~~~~    
    if (number_of_solutions > 2*int(N)-1):
        return True
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    curr_domains = copy.deepcopy(received_domains)                              
    for place in range(0,len(curr_domains[number_of_queen])):                  # Place current queen on each place available in it's domain         
        
        new_domains = FOR(number_of_queen, curr_domains[number_of_queen][place] , curr_domains, N)  # Update domains using Forward Checking
        if not new_domains:                                                    # Skip this placement if Forward Checking returns false 
            continue
        
        if sys.argv[1] == "MAC":                                               # If asked to run MAC  
            new_domains = ac3(number_of_queen,new_domains,neighbours,all_arcs) # Update domains using AC3 Algorithm
        
        if new_domains:                                                        # If AC3 returns Domains and not false
            if number_of_queen+1 == N:                                         # If currently placed queen is the last queen     
                number_of_solutions+=1                                         # We got a solution 
                if(number_of_solutions < 2*int(N)+1):                          # To print only 2*N solutions         
                    print_to_Rfile(final_solution + "," + str(curr_domains[number_of_queen][place]),N)
                flag_for_solution = True                                       # Set flag to return
            else:   
                flag_for_solution = BackTracking (number_of_queen+1,new_domains,final_solution+","+str(curr_domains[number_of_queen][place]), N, flag_for_solution,neighbours,all_arcs) #Recursive Call
 
    return flag_for_solution                                                   # Return True or False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def ac3 (queen, og_domains,neighbours,all_arcs):                               # AC3 Algorithm 
    new_arcs = []                                                              # Initialized new_arcs
    domains = copy.deepcopy(og_domains)
    for x in all_arcs:                                                         # Loop to remove arcs consisting current_queen  
        if not (x[0] <= queen+1 or x[1]<=queen+1):
            new_arcs.append(copy.deepcopy(x))
    while new_arcs:                                                            # new_arcs will have arcs which we have to check consistancy of 
        curr_arc = new_arcs.pop(0)                                             # Remove one arc from all_arcs 
        if arc_reduce(curr_arc,domains):
            if not domains[curr_arc[0]-1]:                                     # If domain of 1st Queen in arc gets emptied (No value is consitant)
                global number_of_backtracks
                number_of_backtracks+=1
                return False                                                   # Return false indicating backtrack
            else:
                for x in neighbours[curr_arc[0]-1]:                            # Loop to add queens to check consistant because of recent changes 
                    if x == curr_arc[1] or x <= queen +1 or x == curr_arc[0]:
                        continue
                    else:
                        new_arcs.append([x,curr_arc[0]])                       # Add the arc of that queen and current queen 
    return copy.deepcopy(domains)
            
def check_constraints(x, y, domains, curr_arc):                                # Function to check if x,y hold consistant
    if x == y:                                                                 # Linear Constraint 
        return False
    elif abs(curr_arc[0] - curr_arc[1]) == abs(x - y):                         # Diagonal constraint 
        return False
    else:
        return True


def arc_reduce(curr_arc, domains):                                             # Function to reduce the domain of queen in arc 
    temp_domains = copy.deepcopy(domains)
    flag = False
    for x in temp_domains[curr_arc[0]-1]:                                      # Take every element of current domain of 1st queen in the arc
        in_flag = True
        for y in temp_domains[curr_arc[1]-1]:                                  # Take every element of current domain of 2nd queen in the arc
            if not in_flag:
                break
            if check_constraints(x, y, domains, curr_arc):                     # Check if x and y consistant  
               in_flag = False
            else:
               in_flag = True
        if in_flag:                                                            # If no value is found to be consistant with x in domain of Queen2 
            domains[curr_arc[0]-1].remove(x)                                   # Remove that x 
            flag = True                                                        # Set flag that value of domain is changed
    return flag                                                                # Return flag

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

start = time.time()

Object_of_QueenGraph = QueenGraph()                                            # Object of QueenGraph is initiated 

print_to_Cfile(Object_of_QueenGraph.N,Object_of_QueenGraph.all_dom)

if BackTracking(0, Object_of_QueenGraph.all_dom, "",Object_of_QueenGraph.N, False, Object_of_QueenGraph.neighbours, Object_of_QueenGraph.all_arcs):
    end = time.time()
    f = open(sys.argv[4], "a")                                                 # Print to Rfile 
    print("Time Taken: ", end - start, file =f)
    print("Number of Solutions: ", number_of_solutions, file =f)
    print("Number of Backtracks: ", number_of_backtracks, file =f)
    f.close()   
else:
    end = time.time()
    f = open(sys.argv[4], "a")
    print("No Solution", file = f)
    print("Time Taken: ", end - start," Seconds", file = f)
    f.close()

