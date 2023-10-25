#eulerian circuits for undirected graphs
#to check if given graph is eulerian or not
#input is an adjacency list of an undirected graph
#output is a circular list of edges that forms an eulerian path like (x,y),(y,z),(z,x)
#we will use the Hierholzer's algorithm

#first let us check if each vertice has even degree
def check_degree(adj_list):
    degree = {}
    for i in range(0,len(adj_list)):
        degree[i] = len(adj_list[i])
    for i in degree:
        if degree[i] % 2 != 0:
            return "Not Eulerian"
    return True

#function to find the eulerian path
def eulerian_path(adj_list,final_cycle,curr_path):
    curr_vertex = curr_path[-1]
    if len(adj_list[curr_vertex]) != 0:
        temp=curr_vertex
        curr_path.append(adj_list[curr_vertex].pop())
        curr_vertex = curr_path[-1]
        adj_list[curr_vertex].remove(temp)
        eulerian_path(adj_list,final_cycle,curr_path)
    else:
        final_cycle.append(curr_path.pop())
        if len(curr_path) != 0:
            curr_vertex = curr_path[-1]
        if len(curr_path) != 0:
            eulerian_path(adj_list,final_cycle,curr_path)
        else:
            return final_cycle[::-1]
        
#main function to call the above functions
def main():
    adj_list=[[1,4,5,6],[0,2,4,4],[1,3],[2,4],[0,1,1,3],[0,6],[5,0]]
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
#adj_list=[[1,2,3,5],[0,2],[0,1,3,5],[0,2,4,5],[3,5],[0,2,3,4]]
#adj_list=[[1,4,5,6],[0,2,4,4],[1,3],[2,4],[0,1,1,3],[0,6],[5,0]]
#adj_list=[[0,1,3,0],[0,2],[1,3],[0,2]]