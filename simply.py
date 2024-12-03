import pyvista as pv
import numpy as np
# Cargar el archivo OBJ
mesh = pv.read("camel_b.obj")

# Mostrar la malla
plotter = pv.Plotter()
plotter.add_mesh(mesh, color="lightblue")
#plotter.show()

archivo = "camel_b.obj"

#--------------------------------getting structures form a object file---------------------------------------------
##getting the face from an object file
def get_faces(mesh_object):
    try:
        with open(mesh_object, 'r') as mesh:
            faces = []
            for line in mesh:
                if line.startswith('f '):
                    partes = line.strip().split()[1:]
                    face_indices = []
                    for i in partes:
                        
                        indices =int(i.split('/')[0])
                        face_indices.append(indices)
                    faces.append(face_indices)
            return faces
        
    except FileNotFoundError:
        print(f"Error: El archivo '{mesh_object}' no se encuentra.")
        return []
    except ValueError as e:
        print(f"Error al procesar el archivo OBJ: {e}")
        return []

def get_vertex(mesh_object):
    try:
        with open(mesh_object, 'r') as mesh:
            vertex = []
            for line in mesh:
                if line.startswith('v '):
                    partes = line.strip().split()[1:]
                    vertex_indices = []
                    for i in partes:
                        
                        vertex_indices = list(map(float, partes))
                        
                    vertex.append(np.array(vertex_indices))
            return vertex
        
    except FileNotFoundError:
        print(f"Error: El archivo '{mesh_object}' no se encuentra.")
        return []
    except ValueError as e:
        print(f"Error al procesar el archivo OBJ: {e}")
        return []
    


def get_edges(mesh_object):
    faces = get_faces(mesh_object)
    edges = []
    for face in faces:
        edge_1 = (face[0], face[1])
        edge_2 = (face[1], face[2])
        edge_3= (face[2], face[0])
        edges.append(edge_1)
        edges.append(edge_2)
        edges.append(edge_3)
    return edges


def is_edge(mesh_object, vertex_1, vertex_2):
    if (vertex_1,vertex_2) in get_edges(mesh_object):
        return 1
    else: 
        return 0

def get_face_vertices(face, vertices):
    face_vertices = []
    for index in face:
        if 0 <= index - 1 < len(vertices):  # Verificar si el índice está dentro del rango
            face_vertices.append(vertices[index - 1])
         # O manejarlo según sea necesario
         
  
    return face_vertices


##--------------------------------------------------checking quadritic error for a vertex-----------------------------
list_camel_vertex = get_vertex(archivo)
list_camel_faces = get_faces(archivo)

def cross_product(v1, v2):
    return np.cross(v1,v2)



def normalize_vect(vect):
    norm = np.sqrt(np.sum(vect ** 2))
    if norm == 0:
        return vect  # Devuelve el vector original si la norma es 0
    return vect / norm


def matrix_for_error(face, list_vert):
    look_vertex = get_face_vertices(face, list_vert)
    #print("lista de todos los vertices" , look_vertex)
    A = look_vertex[0]
    #print("this is A:",A)
    B = look_vertex[1]
    #print("this is B:", B)
    C = look_vertex[2]
    #print("this is C:" , C)

    vector_1 = B - A
    #print("this is vector_1: ",  vector_1)
    vector_2 = C - A
    #print("this is vector_2: ", vector_2)
    v1ProductV2 =  cross_product(vector_1, vector_2)
    #print("this is v1*v2" , v1ProductV2)
    normV1V2 = normalize_vect(v1ProductV2)
    #print("this is normalize vector", normV1V2)
    D = -np.dot(normV1V2, A)


    

    vector_3 = v1ProductV2 * normV1V2
    matrix = np.array([
        [vector_1[0], vector_1[1], vector_1[2],D],
        [vector_2[0], vector_2[1], vector_2[2],D],

        [vector_3[0], vector_3[1], vector_3[2],D],
        [0 , 0, 0, 1]
    ])
    return matrix


def faces_for_vertex(vertex, faces, vertices):
    associated_faces = []
    
    # Asegurarte de que el vértice sea un arreglo NumPy
    vertex = np.array(vertex)

    for face in faces:
        vertex_in_face = get_face_vertices(face, vertices)

        # Comparación tolerante con np.allclose
        if any(np.allclose(vertex, v) for v in vertex_in_face):
            associated_faces.append(face)
    
    return associated_faces

    

def matrix_sum(vertex, list_faces , list_vert):
    vertex = np.array(vertex)
    #rint(vertex)
    faces = faces_for_vertex(vertex, list_faces, list_vert)
    Qfinal  = np.zeros((4, 4))

    for i in faces:
        Q =  matrix_for_error(i, list_vert)
        Qfinal += Q
    return Qfinal




def quadratic_error(vertex, list_faces, list_vertex):
    vertex_4d = np.append(vertex,1)
    estimated =  np.dot(matrix_sum(vertex, list_faces, list_vertex),vertex_4d )
    error_association =  np.square(np.subtract(vertex_4d, estimated))

    return np.sum(error_association)



def quadratic_error_list(list_vertex, list_faces):
    all_errors = []
    for vertex in list_vertex:
        error  = quadratic_error(vertex, list_faces, list_vertex)
        all_errors.append(error)
    
    all_errors.sort()   
    return all_errors 





#------------------------------------------Testing matrix operations ------------------------------------------------------#





##Testing get_faces 

caras = get_faces(archivo)
vertex = get_vertex(archivo)
edges = get_edges(archivo)
# Mostrar el resultado
#print("Caras encontradas:")
cara = caras[0]
#print("estudiemos esta cara" ,cara)


#for verte in vertex[1:7]:
 #  print(type(verte))
  # print(verte)
 ##testing get_vertex
#print("vertex encontradas:")
#print(len(vertex))
#print(len(edges))
#print(is_edge(archivo, 1791, 2))

#cara = caras[0]
#matr = matrix_for_error(cara , vertex)
#print(matr)

vert = [ -0.001169, 36.485862 ,44.324899]


{}
#print(vertex[1:7])
print("LAS CARAS PARA ESTE VERTICE SON ",faces_for_vertex([vertex[17]], caras, vertex))
print(quadratic_error_list(vertex, caras))
#print("largo de lista de vertices: ", len(vertex))















