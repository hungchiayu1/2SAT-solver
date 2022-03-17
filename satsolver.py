import sys
import time
def compute_reverse_graph(graph):
    vertice = graph.keys()
    reverse_graph = {k:[] for k in graph.keys()}
    for curr_node in graph.keys():
        neighbours = graph[curr_node]
        for neighbour in neighbours: ## There is an edge from curr_node->neighbour
            ##Hence we loop through to find all the edge
            reverse_graph[neighbour].append(curr_node)
    return reverse_graph

def dfs(graph):
    visited = {k:[-1,-1] for k in graph.keys()}## first element of the list store whether it was visited. 
    ##Second element store the post order
    time = 1
    post_order = [] ## keep track of post order in ascending order
    for node,visit in visited.items():
        if visit[0]==-1:
            time,post_order = dfs_visit(graph,node,visited,time,post_order)
    return visited,post_order


def dfs_visit(graph,node,visited,time,post_order):
   
    if visited[node]==1: ## This node has been visited
        return time
    time +=1
    visited[node][0] = 1; ## mark this node as visited
    for neighbour in graph[node]:
        if visited[neighbour][0]==-1:
            time,stack = dfs_visit(graph,neighbour,visited,time,post_order)
    visited[node][1] = time
    post_order.append(node)
    time +=1
    return time,post_order

def explore_node(graph,node,visited,nodes):
    if visited[node]==1: ## This node has been visited
        return nodes
            
    nodes.append(node)
    visited[node] = 1; ## mark this node as visited
    for neighbour in graph[node]:
        if visited[neighbour]==-1:
            nodes = explore_node(graph,neighbour,visited,nodes)
    return nodes

def check_complement(SCC):
    temp = [abs(i) for i in SCC]
    if len(set(temp))==len(SCC): 
        ## if a SCC dont contain complements, they should have the same length after turning all the node into positive number
        return True
    return False
def assignment(nodes,res):
    for i in nodes:
        if res[abs(i)-1] == 0 :  ## havent assigned
            if i<0:
                res[abs(i)-1] = -1 ## if we find the negative edge first,assigned it false
                 ## this imply comp[u]<comp[~u]
            else:
                res[abs(i)-1] = 1
    return res
            
            
def find_SCC(graph):
    reverse_graph = compute_reverse_graph(graph) ## O(V+E) time
    _,post_order = dfs(reverse_graph) ## O(V+E)
    first = 1
    visited = {k:-1 for k in graph.keys()}
    satisfiable = True
    result = [0]*int(len(post_order)/2)
    for i in reversed(post_order):
        if(visited[i]==-1):
            nodes = explore_node(graph,i,visited,[])  ## O(V+E) time total
            ## nodes contain all the node in a single SCC
        if not check_complement(nodes):## O(V) time total
            print("UNSATISFIABLE")
            return
        result = assignment(nodes,result) ## O(V) time
    return result

def read_clauses(path):
    clauses = []

    try:
        file = open(path,"r")
        n_var = 0
        n_clause = 0
        clauses_lines = False
        clause=[]
        temp = ''
        neg = 0
        for line in file:
            if line.startswith("p"):
                clauses_lines = True
                n_var = int(line.split()[-2])
                n_clause = int(line.split()[-1])
                continue
            if line.startswith('c'):
                continue
            if clauses_lines:
                num = ''
                char_prev=''
                for char in line:
                    if char=='\n':
                        continue
                    if char ==' ':
                        char_prev = char
                        clause.append(num)
                        num=''
                        continue
                    if char=='0' and char_prev==' ':
                        clauses.append(clause)
                        clause = []
                        continue
        
                    num+=char
                    char_prev = char
        file.close()       
    except IOError:
        print("Can not find input file or read data")
        exit()
    return clauses,n_var

def create_graph_from_clause(clauses,n_var):
    graph = {k:[]  for k in range(-n_var,n_var+1) if k!=0}
    for i in clauses:
        if len(i)<=1:
            continue
        edge_1= (-int(i[0]),int(i[1])) ## edge from 1st to 2nd
        edge_2 = (-int(i[1]),int(i[0]))
        graph[edge_1[0]].append(edge_1[1])
        graph[edge_2[0]].append(edge_2[1])
    return graph

def sat_solver(file):
    clauses,n_var = read_clauses(file)
    graph = create_graph_from_clause(clauses,n_var)
    result = find_SCC(graph) ## Total time is O(V+E)
    return result
            
if __name__ == '__main__':
    file = sys.argv[1]
    start_time = time.time()
    result = sat_solver(file)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(result)
    
