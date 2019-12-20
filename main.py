import numpy as np
# import pygame
# from gui import drawEdge, drawVertex
from collections import defaultdict

def convexVertex(v1, v2, v3):
    v1,v2,v3=np.array(v1),np.array(v2),np.array(v3)
    a,b=v1-v2,v3-v2

    det=a[0]*b[1]-b[0]*a[1]
    return True if det>0 else False

def trianglearea(v1, v2, v3):
    return abs( v1[0]*(v2[1]-v3[1])
               +v2[0]*(v3[1]-v1[1])
               +v3[0]*(v1[1]-v2[1]) )/2

def isinsidetriangle(v1, v2, v3, p):
    a=trianglearea(v1,v2,v3)
    a1=trianglearea(p,v2,v3)
    a2=trianglearea(v1,p,v3)
    a3=trianglearea(v1,v2,p)

    return True if a==a1+a2+a3 else False

def isEar(v1,v2,v3, refl_vert):
    return False if any((isinsidetriangle(v1,v2,v3,p) for p in refl_vert)) else True

def split_convexreflex_idxs(vertices):
    convex, reflex=set(), set()
    n=len(vertices)
    for i in range(len(vertices)):
        if convexVertex(vertices[i-1], vertices[i], vertices[(i+1)%n]):
            convex.add(i)
        else:
            reflex.add(i)

    return convex, reflex

def triangulation(vertices):
    #reference: https://www.geometrictools.com/Documentation/TriangulationByEarClipping.pdf
    edges=set()

    while len(vertices)>=4:
        foundear=False
        vlen=len(vertices)
        convex_idx, reflex_idx=split_convexreflex_idxs(vertices)

        #display process
        # screen=pygame.display.get_surface()
        # screen.fill((255,255,255))
        # for i in reflex_idx:
        #     drawVertex(*vertices[i], 10, 10, color=(255,0,0))
        # for i in convex_idx:
        #     drawVertex(*vertices[i], 10, 10, color=(0,255,0))
        # for i in range(vlen):
        #     drawEdge(vertices[i],vertices[(i+1)%vlen], color=(0,0,0))
        # pygame.display.update()

        #find ear
        for pos in convex_idx:
            p,c,n=vertices[pos-1],vertices[pos],vertices[(pos+1)%vlen]

            reflex_left=(vertices[i] for i in reflex_idx.difference(((pos-1)%vlen,pos,(pos+1)%vlen)))
            if isEar(p,c,n, reflex_left):
                foundear=True
                # drawVertex(*vertices[pos], 10, 10, color=(0,0,255))
                # pygame.display.update()
                break
        
        assert foundear==True, 'Esto no deberia pasar. Checa porqué no hay ninguna oreja!!, ¿seguro que seleccionaste el poligono en forma counter-clockwise?'

        edges.add((p,n))
        del vertices[pos]

        # pygame.time.wait(1000)

    return edges

def edges_to_graph(edges):
    G=defaultdict(set)
    for v1,v2 in edges:
        G[v1].add(v2)
        G[v2].add(v1)

    return G

def calculateguards(edges, vertices):
    #reference: https://www.researchgate.net/publication/256309448_Three-coloring_the_vertices_of_a_triangulated_simple_polygon
    assert len(vertices)>=3, 'Debe haber 3 o más vertices!!'
    G=edges_to_graph(edges)
    colors={v:0 for v in G.keys()}#0 is None; 1,2,3 are the colors
    color_map={0:(0,0,0), 1:(255,255,50), 2:(255,50,255), 3:(50,255,255)}
    color_name={0:'negro', 1:'amarillo', 2:'rosa', 3:'aqua'}

    colors[vertices[0]]=1
    colors[vertices[1]]=2
    for i in range(1, len(vertices)-1):
        if len(G[vertices[i]])%2==1:
            color=colors[vertices[i-1]]
        else:
            color=6-colors[vertices[i-1]]-colors[vertices[i]]
        colors[vertices[i+1]]=color
        
    guards=set((color_map[colors[v]],v) for v in G.keys())
    vals=list(colors.values())
    min_color=min(set(vals), key=vals.count)

    return guards, color_name[min_color]

def main(vertices):
    # edges=[(v1,v2) for v1 in vertices for v2 in vertices]
    poligon_edges=set((vertices[i],vertices[i+1]) for i in range(-1, len(vertices)-1))
    edges=triangulation(vertices.copy())
    guards,min_color=calculateguards(edges.union(poligon_edges), vertices)
    print(f'El color óptimo de los guardias es {min_color}')
    return edges, guards, min_color