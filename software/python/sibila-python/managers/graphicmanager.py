import networkx as nx
from networkx import adjacency_graph
import matplotlib.pyplot as plt


class GraphicManager:

    def draw(self, G,labels):
        pos = nx.planar_layout(G)
        color_map = ['red'] + ['orange']*(G.order()-1)
        nx.draw_networkx_nodes(G, pos, node_size=500,
                            node_color=color_map, alpha=0.7)

        nx.draw_networkx_edges(G, pos, width=0.5, alpha=1, edge_color='black',
                            connectionstyle='arc3,rad=0.05', arrowsize=20)

        nx.draw_networkx_labels(G, pos, font_size=16,
                                font_family='sans-serif', font_color='black')
                                
        for arc in labels:
            nx.draw_networkx_edge_labels(
                G, pos, {(arc[0], arc[1]): str(arc[2])}, label_pos=0.3)
        
        return G


# En lugar de recibir un solo vector de respuestas, que reciba varias respuestas.
#  Intentar recibir varias ramas a partir de un mismo nodo. O varios gráficos que salen del mismo nodo.

    def showOneResponse(self, lst1: [str], lst2: [str] = []):
        
        G = nx.DiGraph()       

        if lst2 == []:
            # Asumir que pasan un solo array de la forma ["Concepto","Relacion","Concepto","Rel","Concepto"]
            labels = []
            for i in range(len(lst1)):
                if (i % 2) == 0:
                    G.add_node(lst1[i])

                    if i > 0:
                        G.add_edge(lst1[i-2], lst1[i])

                else:
                    labels.append([lst1[i-1], lst1[i+1], lst1[i]])

        else:
            # Pasan dos array: lst1 donde vienen los conceptos, lst2 donde están las relaciones
            labels = []

            for i in range(len(lst1)):
                G.add_node(lst1[i])
                if i > 0:
                    G.add_edge(lst1[i-1], lst1[i])

            for j in range(len(lst2)):
                labels.append([lst1[j], lst1[j+1], lst2[j]])

        G = self.draw(G,labels)     
        plt.axis('off')
        return plt.show()


    def showMultipleResponse(self,lst1: [str],lst2: [str] =[]):
        plt.figure(figsize=(20,20))
        G = nx.DiGraph()
        labels = []
        for k in range(len(lst1)):
            if lst2==[]:
            ### Asumir que pasan un solo array de la forma ["ConceptoRaiz","Relacion","Concepto"]                  
                for i in range(len(lst1[k])):
                    if (i % 2) == 0:            
                        G.add_node(lst1[k][i]) 

                        if i > 0:                 
                            G.add_edge(lst1[k][i-2],lst1[k][i])

                    else:
                        labels.append([lst1[k][i-1],lst1[k][i+1],lst1[k][i]])        

            else:
            ### Pasan dos array: lst1 donde vienen los conceptos, lst2 donde están las relaciones                
                for i in range(len(lst1[k])):                      
                    G.add_node(lst1[k][i]) 
                    if i > 0:
                        G.add_edge(lst1[k][i-1],lst1[k][i])

                for j in range(len(lst2[k])):
                    labels.append([lst1[k][j],lst1[k][j+1],lst2[k][j]])

        G = self.draw(G,labels)
        plt.axis('off')
        return plt.show()

        