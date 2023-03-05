import graphviz
class Node:
    def __init__(self, value=None, color ='b', p=None, left=None, right=None):
        self.value = value
        self.color = color
        self.p = p
        self.left = left
        self.right = right
        
    def print_node(self):
        print(f"{self.color}:{self.value}, P:{self.p.value} L: {self.left.value} R:{self.right.value}")

class RedBlackTree:
    def __init__(self):
        ''' Initialize the red black tree: just create the T.nil node. '''
        self.nil_node = Node() # the color of nil_node is black
        self.root = self.nil_node # now self.node and self.nil_node are pointed to the same class instance
        self.out_put_DOT = ''
        self.lr_sequence = []

    def rotate(self, mode, x):
        '''
            mode: left rotate & right rotate
            x: the node that to be rotated
        '''
        if mode == 'left':
            y = x.right
            # y.print_node() #FIXME
            x.right = y.left # let y.left tree be the right tree of x
            # y.left.print_node() #FIXME
            if y.left.value !=None:
                y.left.p = x # nil_node also has "parent" property!
            y.p = x.p
            if x.p.value == None: # x is the root 
                self.root = y
            elif x.p.left == x:
                x.p.left = y
            else:
                x.p.right = y
            y.left = x
            x.p = y
            self.lr_sequence.append(-1)

        if mode == 'right':
            y = x.left
            # y.print_node() #FIXME
            x.left = y.right# let y.left tree be the right tree of x
            # y.left.print_node() #FIXME
            if y.right.value != None:
                y.right.p = x # nil_node also has "parent" property!
            
            y.p = x.p
            if x.p.value == None: # x is the root 
                self.root = y
            elif x.p.left == x:
                x.p.left = y
            else:
                x.p.right = y
            
            y.right = x
            x.p = y
            self.lr_sequence.append(1)

    def insert(self, node_value):
        '''
            Insert node with node_value into the rbTree.
        '''
        self.lr_sequence = []
        z = Node(value= node_value)
        y = self.nil_node
        x = self.root
        while x.value != None:  # x != self.nil_node -> should be x.value != None
            y = x # Use y to record position of x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y.value == None: # When tree is empty!
            self.root = z
        elif z.value < y.value:
            y.left = z
        else :
            y.right = z
        z.left = self.nil_node
        z.right = self.nil_node
        z.color = 'r' # color is red 
        self.insert_fixup(z)
        if self.lr_sequence != []:
            return self.lr_sequence

    def insert_fixup(self,z):
        ''' z is a node'''
        father = z.p
        grand_father = father.p
        # print(father.color, father.value)  # FIXME
        while father.color == 'r': # z.p.p cannot be nil, since z.p is not the root
            if father == grand_father.left:
                uncle =  grand_father.right
                # case 1: move the conflict upwards to grandfather
                if uncle.color == 'r':
                    grand_father.color = 'r'
                    father.color = 'b'
                    uncle.color = 'b'
                    z = grand_father
               
                else:
                    # case 2
                    if z == father.right:
                        z = father
                        self.rotate('left',z)
                    # case 3
                    z.p.color = 'b'
                    z.p.p.color = 'r'
                    self.rotate('right',z.p.p)

            else: # father == grand_father.right
                uncle =  grand_father.left
                # case 1: move the conflict upwards to grandfather
                if uncle.color == 'r':
                    grand_father.color = 'r'
                    father.color = 'b'
                    uncle.color = 'b'
                    z = grand_father
                
                else:
                    # case 2
                    if z == father.left:
                        z = father
                        self.rotate('right',z)
                    # case 3
                    z.p.color = 'b'
                    z.p.p.color = 'r'
                    self.rotate('left',z.p.p)

            # update father and grand_father
            father = z.p
            grand_father = father.p

        # finally outside the while loop remember to set root be black
        self.root.color = 'b'
        # print(self.root.value) # FIXME
                 
    def insert_from_list(self,value_list):
        for item in value_list: 
            self.insert(item)

    def search(self, value):
        '''
            search the node with value in rbTree
        '''
        x = self.root
        while x != self.nil_node:
            if x.value == value:
                return x
            elif x.value < value:
                x = x.right
            else:
                x = x.left
        return None # If not found, return None
    
    def getmin(self, root_node):
        '''
            get the node with min value in the subtree with root_node as its root.
        '''
        x = root_node
        while x.left != self.nil_node:
            x = x.left
        return x
    
    def transplant(self, origin_node, new_node):
        '''
            transplant origin_node to new_node without changing left and right
        '''
        if origin_node.p == self.nil_node:
            self.root = new_node
        elif origin_node == origin_node.p.left:
            origin_node.p.left = new_node  
        else: 
            origin_node.p.right = new_node  
        new_node.p = origin_node.p

        return new_node

    def delete(self, z): 
        '''
            delete node z in rbTree, z need to be searched first.
        '''
        y = z
        y_origin_color = z.color # save the color of z
        
        if z.left == self.nil_node:
            x = z.right
            x = self.transplant(z,z.right) 
        elif z.right == self.nil_node:
            x = z.left
            x = self.transplant(z,z.left)

        # if z has left and right children
        else:
            y = self.getmin(z.right)
            y_origin_color = y.color
            x = y.right
            if y.p == z:    # y is the right child of z
                x.p = y
            else:
                x.p = y.p   # y is not the right child of z
                y.p.left = x
                
                y.right = z.right
                y.right.p = y

            # shared by both conditions:
            y = self.transplant(z,y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        del z
        if y_origin_color == 'b':
            # 3 conditions
            # print(x.p.value) # FIXME
            self.delete_fixup(x)
        if self.lr_sequence != []:
            return self.lr_sequence


    def delete_fixup(self, x):
        while x != self.root and x.color == 'b':
            if x == x.p.left:
                w = x.p.right
                # case 1
                if w.color == 'r':
                    w.color = 'b'
                    x.p.color = 'r'
                    self.rotate('left', x.p)
                    w = x.p.right
                # case 2: let black height - 1
                if w.left.color == 'b' and w.right.color == 'b':
                    w.color = 'r'
                    x = x.p
                else:
                    # case 3
                    if w.right.color == 'b':
                        w.left.color = 'b'
                        w.color = 'r'
                        self.rotate('right', w)
                        w = x.p.right
                    # case 4: let black height + 1
                    w.color = x.p.color
                    x.p.color = 'b'
                    w.right.color = 'b'
                    self.rotate('left', x.p)
                    x = self.root

            else: # x == x.p.right
                w = x.p.left
                # case 1
                if w.color == 'r':
                    w.color = 'b'
                    x.p.color = 'r'
                    self.rotate('right', x.p)
                    w = x.p.left
                # case 2: let black height - 1
                if w.right.color == 'b' and w.left.color == 'b':
                    w.color = 'r'
                    x = x.p
                else:
                    # case 3
                    if w.left.color == 'b':
                        w.right.color = 'b'
                        w.color = 'r'
                        self.rotate('left', w)
                        w = x.p.left
                    # case 4: let black height + 1
                    w.color = x.p.color
                    x.p.color = 'b'
                    w.left.color = 'b'
                    self.rotate('right', x.p)
                    x = self.root
        x.color = 'b'

    def draw_node(self,x):
        if x.value !=None:
            if x.color == 'r':
                self.out_put_DOT += f'{x.value}[color=white style=filled fillcolor="#F14F50" shape=circle fontcolor=white fontname="Minecraft" fontsize="16" penwidth=3]\n'
            else:
                self.out_put_DOT += f'{x.value}[color=white style=filled fillcolor=black shape=circle fontcolor=white fontname="Minecraft" fontsize="16" penwidth=3]\n'
            if x.left.value != None:
                self.out_put_DOT += f"{x.value} -> {x.left.value}[color=white arrowhead=none penwidth=3]\n"
            if x.right.value != None:
                self.out_put_DOT += f"{x.value} -> {x.right.value}[color=white arrowhead=none penwidth=3]\n"
            self.draw_node(x.left)
            self.draw_node(x.right)

    def draw(self, fname="rbTree"):
        '''
            draw rbTree using graphviz
        '''
        self.out_put_DOT = 'digraph G {\nbgcolor="#1E1E1E"\ndpi = "80"'
        self.draw_node(self.root)
        self.out_put_DOT += "}\n"
        src = graphviz.Source(self.out_put_DOT)
        return src.render(directory = '../graphics',format='png')

if __name__ == '__main__':
    print('-'*50)

    my_tree =RedBlackTree()
    for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]:
        my_tree.insert(i)
    print(my_tree.draw())