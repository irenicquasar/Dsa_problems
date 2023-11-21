#longest sunsequence problem
#return the length of the longest subsequence
def lcs(str1,str2):
    #construct a dynamic table
    #row =str1
    #column =str2
    table = []
    for i in range (len(str1)+1):
        table.append([])
        for j in range(len(str2)+1):
            table[i].append(0)
    #filling vlaues in the table
    for i in range(len(str1)+1):
        for j in range(len(str2)+1):
            #to check if the row or column represent ""
            if (i==0) or (j==0):
                table[i][j]=0
            elif (str1[i-1]==str2[j-1]):
                table[i][j]=table[i-1][j-1]+1
            else:
                table[i][j]=max(table[i-1][j],table[i][j-1])
                      
    return table[len(str1)][len(str2)]

print(lcs("abcde","def"))