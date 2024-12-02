import time

class Node:
    def __init__(self, id: tuple, *parents):

        self.parents: list[Node] = list(parents)
        self.id = id

        self.children = []
        if(self.parents != []):
            for p in self.parents:
                p.children.append(self)

        self.states = set()
        self.safe = None


class WumpusLogic:
    def __init__(self, start_node, move_func):
        start_node.states.add("V")
        # V represents that the node is visited

        self.move = move_func

        # all nodes stored in a dictionary where their coordinates are the key
        self.nodes = { start_node.id: start_node }

        self.safe = None

        # pos is the robot's current position
        self.pos = start_node.id

        # posW is the position of the wumpus
        # posP is a list of pit positions
        self.posW = (None, None)
        self.posP = []

    def getNodesByState(self, state: str):
        res = []
        for id, node in self.nodes.items():
            if(state in node.states):
                res.append(id)
        return res

    def _back(self):
        valid_nodes = []
        while len(valid_nodes) == 0:

            if(len(self.nodes[self.pos].parents) == 0):
                return self._think
            # move back to parent
            # ---MOVEMENT CODE---
            y,x = (
                self.nodes[self.pos].parents[0].id[0]-self.pos[0],
                self.nodes[self.pos].parents[0].id[1]-self.pos[1]
            )

            # -------------------
            self.pos = self.nodes[self.pos].parents[0].id

            list(filter(
            lambda node: not (node == None or node in self.posP or node == self.posW),
            self._getANodes()
            ))

            for node in list(filter(
                lambda node: not (node == None or node in self.posP or node == self.posW),
                self._getANodes()
            )):
                node = self.nodes[node]
                if(node.safe == True and "V" not in node.states):
                    valid_nodes.append(node.id)
        
        return self._map
        

    def _getANodes(self, *pos):
        if(len(pos) == 0):
            pos = self.pos
        else:
            pos = pos[0]
        return [
            (pos[0]+1, pos[1]) if pos[0]+1 < 4 and pos[0]+1 > -1 else None,
            (pos[0], pos[1]+1) if pos[1]+1 < 4 and pos[1]+1 > -1 else None,
            (pos[0]-1, pos[1]) if pos[0]-1 < 4 and pos[0]-1 > -1 else None,
            (pos[0], pos[1]-1) if pos[1]-1 < 4 and pos[1]-1 > -1 else None,
        ]

    def _map(self):
        # direction priorities is up, right, down, left
        adj_nodes = self._getANodes()

        # filter out-of-bounds and unsafe nodes
        adj_nodes = list(filter(
            lambda node: not (node == None or node in self.posP or node == self.posW),
            adj_nodes
        ))

        #---GET DATA HERE---
        data = [0,0,0]
        

        #-------------------

        g, s, b = data

        for node in adj_nodes:

            if(node not in self.nodes.keys()):
                node = Node(node, self.nodes[self.pos])
            else:
                node = self.nodes[node]
            
            if(g == 1):
                self.nodes[self.pos].states.add("g")
            if(s == 1 and node.safe != True):
                self.nodes[self.pos].states.add("s")
                node.safe = False
            if(b == 1 and node.safe != True):
                self.nodes[self.pos].states.add("b")
                node.safe = False
            
            if(1 not in [s,b]):
                node.safe = True

            self.nodes[node.id] = node

        # filter out unsafe nodes
        adj_nodes = list(filter(
            lambda id:self.nodes[id].safe == True and ("V" not in self.nodes[id].states),
            adj_nodes
        ))

        if(len(adj_nodes) == 0):
            return self._back
        
        #---MOVEMENT CODE HERE---
        y,x = (adj_nodes[0][0]-self.pos[0], adj_nodes[0][1]-self.pos[1])



        #------------------------

        self.pos = adj_nodes[0]
        self.nodes[self.pos].states.add("V")

        return self._map

    def _think(self):
        B_nodes = self.getNodesByState("b")
        S_nodes = self.getNodesByState("s")
        G_nodes = self.getNodesByState("g")

        pits = set()
        for i in range(len(B_nodes)):
            node = self.nodes[B_nodes[i]]
            p_cands = list(filter(
                lambda x: not (x == None or self.nodes[x].safe == True),
                self._getANodes(node.id)
            ))
            pits = pits.union(set(p_cands))

        if(len(pits) > 2):
            # overlap between pits
            # choose the set of two that are furthest away from each other
            for i in range(len(pits)):
                temp_pits = list(pits)
                j = i + 1
                if(j > len(pits)-1):
                    j = 0
                pair = [temp_pits[i], temp_pits[j]]
                if(pair[1] not in self._getANodes(pair[0])):
                    pits = set(pair)

        wumpus = set()
        for i in range(len(S_nodes)):
            node = self.nodes[S_nodes[i]]
            w_cands = list(filter(
                lambda x: not (x == None or self.nodes[x].safe == True),
                self._getANodes(node.id)
            ))
            wumpus = wumpus.union(set(w_cands))
        
        golds = set()
        for i in range(len(G_nodes)):
            node = self.nodes[G_nodes[i]]
            g_cands = list(filter(
                lambda x: not (x == None),
                self._getANodes(node.id)
            ))
            for elem in g_cands:
                adj_nodes = self._getANodes(elem)
                adj_nodes = filter(lambda x: x != None, adj_nodes)
                adj_states = list(self.nodes[e].states for e in adj_nodes)
                if("g" in adj_states[0].intersection(*adj_states[1:])):
                    golds.add(elem)

        golds = golds.difference(pits)
        golds = golds.difference(wumpus)

        self.posP = list(pits)
        self.posW = list(wumpus)[0]

        for node in self.posP + [self.posW]:
            for node in self._getANodes(node):
                if(node != None):
                    self.nodes[node].safe = True

        if(len(golds) == 0):
            return self._map

        self._pathtogold(list(golds)[0])
        return

    def _pathtogold(self, pos):

        while self.pos != pos:

            adj_nodes = list(filter(
                lambda x: x != None and self.nodes[x].safe == True,
                self._getANodes()
            ))

            if(self.pos[0] < pos[0]):
                next_node = sorted(adj_nodes, reverse=True)[0]
            elif(self.pos[0] > pos[0]):
                next_node = sorted(adj_nodes, reverse=False)[0]
            elif(self.pos[1] < pos[0]):
                adj_nodes = list((x,y) for y,x in adj_nodes)
                next_node = tuple(reversed(sorted(adj_nodes, reverse=True)[0]))
            elif(self.pos[1] > pos[0]):
                adj_nodes = list((x,y) for y,x in adj_nodes)
                next_node = tuple(reversed(sorted(adj_nodes, reverse=False)[0]))
            
            # ---MOVEMENT CODE HERE---
            movement = (
                next_node[0]-self.pos[0],
                next_node[1]-self.pos[1]
            )



            # ------------------------

            self.pos = next_node

    def loop(self):

        # any setup code can go here

        phase = self._map()
        while phase != None:
            phase = phase()
