# Problema de la galería de arte
Se resuelve el problema de la galeria de arte triangulando con ear-clipping y pygame como gui para introducir los vértices de un polígono simple.
Se requiere Python 3 con pygame y numpy para ejecutar con `python3 run.py`. El uso es el siguiente:
- Se seleccionan los vértices del poligono, dando clic en la ventana, de una forma **contraria a las manecillas del reloj** <- *importante!*.
- Para completar el polígono haga clic en el vértice rojo para cerrarlo.
- Se mostrará la triangulación y coloración de éste, además, en el encabezado de la ventana y en la consola se imprimirá el color óptimo de los guardias.
    
Referencias:
- https://www.geometrictools.com/Documentation/TriangulationByEarClipping.pdf
- https://www.researchgate.net/publication/256309448_Three-coloring_the_vertices_of_a_triangulated_simple_polygon
