import numpy as np

# ----------------------------------- Carga Única del Archivo OBJ -----------------------------------

def load_mesh(mesh_object):
    """Carga las caras y vértices de un archivo OBJ una sola vez."""
    faces = []
    vertices = []
    try:
        with open(mesh_object, 'r') as mesh:
            for line in mesh:
                if line.startswith('v '):
                    vertices.append(np.array(list(map(float, line.strip().split()[1:]))))
                elif line.startswith('f '):
                    indices = [int(i.split('/')[0]) for i in line.strip().split()[1:]]
                    faces.append(indices)
    except FileNotFoundError:
        print(f"Error: El archivo '{mesh_object}' no se encuentra.")
    except ValueError as e:
        print(f"Error al procesar el archivo OBJ: {e}")
    return vertices, faces

# ---------------------------------- Optimización en Cálculos -----------------------------------

def get_face_vertices(face, vertices):
    """Obtiene los vértices de una cara dados los índices."""
    return [vertices[index - 1] for index in face]  # Los índices OBJ empiezan en 1

def cross_product(v1, v2):
    """Calcula el producto cruzado entre dos vectores."""
    return np.cross(v1, v2)

def normalize_vect(vect):
    """Normaliza un vector."""
    norm = np.linalg.norm(vect)
    return vect if norm == 0 else vect / norm

def matrix_for_error(face, vertices):
    """Calcula la matriz de error cuadrático para una cara."""
    A, B, C = get_face_vertices(face, vertices)
    vector_1, vector_2 = B - A, C - A
    normal = normalize_vect(cross_product(vector_1, vector_2))
    D = -np.dot(normal, A)
    return np.array([
        [normal[0]**2, normal[0]*normal[1], normal[0]*normal[2], normal[0]*D],
        [normal[1]*normal[0], normal[1]**2, normal[1]*normal[2], normal[1]*D],
        [normal[2]*normal[0], normal[2]*normal[1], normal[2]**2, normal[2]*D],
        [D*normal[0], D*normal[1], D*normal[2], D**2]
    ])

def faces_for_vertex(vertex_index, faces):
    """Obtiene las caras asociadas a un índice de vértice."""
    return [face for face in faces if vertex_index + 1 in face]

def matrix_sum(vertex_index, faces, vertices):
    """Calcula la suma de matrices de error cuadrático para un vértice."""
    Qfinal = np.zeros((4, 4))
    associated_faces = faces_for_vertex(vertex_index, faces)

    for face in associated_faces:
        Qfinal += matrix_for_error(face, vertices)
    return Qfinal

def precalculate_matrices(list_faces, list_vertex):
    """Precalcula todas las matrices Q para los vértices y las almacena."""
    Q_matrices = []
    for i in range(len(list_vertex)):
        Q_matrices.append(matrix_sum(i, list_faces, list_vertex))
    return Q_matrices

def quadratic_error(vertex, Q_matrix):
    """Calcula el error cuadrático para un vértice dado su matriz Q precalculada."""
    vertex_4d = np.append(vertex, 1)
    return np.dot(vertex_4d, np.dot(Q_matrix, vertex_4d))  # Producto doble para evitar resta y cuadrado

def quadratic_error_list(list_vertex, Q_matrices):
    """Calcula los errores cuadráticos para todos los vértices usando matrices precalculadas."""
    errors = [quadratic_error(vertex, Q_matrices[i]) for i, vertex in enumerate(list_vertex)]
    return sorted(errors)

# ---------------------------------- Ejecución Optimizada -----------------------------------

archivo = "camel_b.obj"  # Reemplaza con el nombre de tu archivo OBJ

# Carga única de vértices y caras
vertices, faces = load_mesh(archivo)

# Precalcular todas las matrices Q
Q_matrices = precalculate_matrices(faces, vertices)

# Calcular errores cuadráticos para todos los vértices
all_errors = quadratic_error_list(vertices, Q_matrices)
print("Errores cuadráticos ordenados:", all_errors)


