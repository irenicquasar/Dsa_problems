#huffman code
dictionary=dict()
huffman_code=dict()
node_dict=dict()

#counts the frequency of each character
def count_occurence(text):
    for i in text:
        if i not in dictionary:
            dictionary[i]=1
        else:
            dictionary[i]+=1
    return dictionary

#calculautes the probability of each character.
def prob_occ(dictionary, text):
    total_char=len(text)
    for i in dictionary:
        dictionary[i]=dictionary[i]/total_char
    return dictionary

#finds min 2 elements in the dictionary
def find_2_min(dictionary):
    # sorts the dictionary by its values and gets the keys
    sorted_keys = sorted(dictionary, key=dictionary.get)
    first_min_key = sorted_keys[0]
    second_min_key = sorted_keys[1]
    return first_min_key,second_min_key

class Node:
    def __init__(self, data=None, left=None, right=None, parent=None):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent

def construct(dictionary):
    node_dict = {key: Node(key) for key in dictionary}  # Create a Node for each key in dictionary

    while len(node_dict) > 1:
        first_min_key, second_min_key = find_2_min(dictionary)
        temp = first_min_key + second_min_key
        dictionary[temp] = dictionary[first_min_key] + dictionary[second_min_key]

        # Create a new Node with left and right set to the Nodes for first_min_key and second_min_key
        temp_node = Node(temp, node_dict[first_min_key], node_dict[second_min_key])

        # Set parent of left and right Nodes
        node_dict[first_min_key].parent = temp_node
        node_dict[second_min_key].parent = temp_node

        # Add the new Node to node_dict
        node_dict[temp] = temp_node

        # Remove the old Nodes from dictionary and node_dict
        del dictionary[first_min_key]
        del dictionary[second_min_key]
        del node_dict[first_min_key]
        del node_dict[second_min_key]

    return dictionary, node_dict

def generate_huffman_codes(node, code='', huffman_code={}):
    if node is not None:
        if node.left is None and node.right is None:  # leaf node
            huffman_code[node.data] = code
        generate_huffman_codes(node.left, code + '0', huffman_code)
        generate_huffman_codes(node.right, code + '1', huffman_code)
    return huffman_code

def display_huffman_code(text, huffman_code):
    encoded_text = ''
    for char in text:
        encoded_text += huffman_code[char]
    return f'Encoded text: {encoded_text}'

def output(text):
    dictionary = count_occurence(text)  # Count the occurrence of each character
    dictionary = prob_occ(dictionary, text)  # Calculate the probability of each character
    dictionary, node_dict = construct(dictionary)
    root = next(iter(node_dict.values()))  # Get the root node from node_dict
    huffman_code = generate_huffman_codes(root)  # Generate Huffman codes
    print(display_huffman_code(text, huffman_code))  # Display Huffman code
    print(huffman_code)

output()
