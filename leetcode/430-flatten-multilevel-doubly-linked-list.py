# You are given a doubly linked list which in addition to the next 
# and previous pointers, it could have a child pointer, which may 
# or may not point to a separate doubly linked list. These child 
# lists may have one or more children of their own, and so on, to 
# produce a multilevel data structure, as shown in the example below.

# Flatten the list so that all the nodes appear in a single-level, 
# doubly linked list. You are given the head of the first level of the list.

# 44 ms - 24.01%
# 14.8 MB 0 52.72%

# Definition for a Node.
class Node:
    def __init__(self, val, prev = None, next = None, child = None):
        if type(val) is list and val:
            self._from_list(val)
        else:    
            self.val = val
            self.prev = prev
            self.next = next
            self.child = child
    def _from_list(self,arr):
        self.val = arr[0]
        self.next = None
        self.prev = None
        self.child = None
        previous_node = self
        building_lower_chain = False
        started_adding_child = False
        parent_head = self
        parent_iteration_node = self
        for i in range(1,len(arr)):
            if building_lower_chain:
                # we have a higher level node we are building a lower one
                if arr[i] is None and not started_adding_child:
                    # we're at the start and are waiting for a non-null value
                    parent_iteration_node = parent_iteration_node.next
                elif arr[i] is not None:
                    # we're making a new chain
                    current_node = Node(arr[i])
                    if started_adding_child:
                        current_node.prev = previous_node
                        if previous_node is not None:
                            previous_node.next = current_node
                        previous_node = current_node
                    # link it to parent node if it's the first one
                    else:
                        started_adding_child = True
                        parent_iteration_node.child = current_node
                        parent_head = current_node
                        previous_node = current_node
                else:
                    # we've added children and now have found an end
                    parent_iteration_node = parent_head
                    started_adding_child = False
                    previous_node = None
            else:
                # we're at the start and need to create the parent chain
                if arr[i] is not None:
                    # we're adding  
                    current_node = Node(arr[i])
                    current_node.prev = previous_node
                    previous_node.next = current_node
                    previous_node = current_node
                else: # we're done making the parent chain
                    building_lower_chain = True
                    previous_node = None
    def level_items(self):
        output = []
        current_node = self
        while current_node is not None:
            output.append(current_node.val)
            current_node = current_node.next
        return output



class Solution:
    def flatten(self, head: 'Node') -> 'Node':
        previous_node = None
        current_node = head
        next_nodes = []
        while current_node is not None or next_nodes:
            if current_node is None:
                # there's a higher level to start stitching to
                previous_node.next = next_nodes.pop()
                current_node = previous_node.next
                if current_node is not None:
                    current_node.prev = previous_node
            elif current_node.child is None:
                # no child, we're just moving down the line
                previous_node = current_node
                current_node = current_node.next
            else:
                # found a child need to mark the next node
                # and start inserting the children
                next_nodes.append(current_node.next)
                current_node.next = current_node.child
                current_node.next.prev = current_node
                current_node.child = None
                previous_node = current_node
                current_node = current_node.next
        return head

answer = Solution()
sample1 = Node([1,2,3,4,5,6,None,None,None,7,8,9,10,None,None,11,12])
answer.flatten(sample1)
sample1.level_items()


