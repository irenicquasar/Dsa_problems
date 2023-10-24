#eulerian circuits for directed graphs
#to check if given graph is eulerian or not
#input is an adjacency list of a directed graph
#output is a circular list of edges that forms an eulerian path like (x,y),(y,z),(z,x)
#we will use the Hierholzer's algorithm

#first let us check if every vertex has equal in and out degree
#let us create 2 dictionaries for in and out degree
#we will use the adjacency list to create these dictionaries
def check_degree(adj_list):
    in_degree = {}
    out_degree = {}
    for i in range(0,len(adj_list)):
        out_degree[i] = len(adj_list[i])
        for j in adj_list[i]:
            if j in in_degree:
                in_degree[j] += 1
            else:
                in_degree[j] = 1
    for i in in_degree:
        if in_degree[i] != out_degree[i]:
            return "Not Eulerian"
    return True

#function to find the eulerian path    

def eulerian_path(adj_list,final_cycle,curr_path):
    curr_vertex = curr_path[-1]
    if adj_list[curr_vertex]:
        curr_path.append(adj_list[curr_vertex].pop())
        curr_vertex = curr_path[-1]
        eulerian_path(adj_list,final_cycle,curr_path)
    else:
        final_cycle.append(curr_path.pop())
        if curr_path:
            curr_vertex = curr_path[-1]
            eulerian_path(adj_list,final_cycle,curr_path)
        else:
            return

#main function to call the above functions

def main():
    adj_list=[[1,5],[2,4],[3],[4],[1,0],[6],[0]]
    if len(adj_list) == 0:
        print("list is empty")
    final_cycle = []
    curr_path = [0]
    if check_degree(adj_list) == True:
        eulerian_path(adj_list,final_cycle,curr_path)
        final_cycle = final_cycle[::-1]
        for i in range(0,len(final_cycle)-1):
            print((final_cycle[i],final_cycle[i+1]),end=",")
    else:
        print(check_degree(adj_list))

main()

#example inputs
#adj_list=[[1],[2],[0]]
#adj_list=[[1, 6], [2], [0, 3], [4], [2, 5], [0], [4]]
#adj_list=[[3,2],[0],[1,3],[4,5],[5],[0,2]]
#adj_list=[[1,5],[2,4],[3],[4],[1,0],[6],[0]]
#ad_list=[[0,1],[2],[3],[0]]
#adj_list=[]
