import pyvista as pv

# Cargar el archivo OBJ
mesh = pv.read("camel_b.obj")

# Mostrar la malla
plotter = pv.Plotter()
plotter.add_mesh(mesh, color="lightblue")
plotter.show()
