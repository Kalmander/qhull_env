import re
import plotly.graph_objects as go

# Load file
with open("output.off", "r") as file:
    content = file.read()

# Extract all OFF blocks
off_blocks = re.findall(r"\{(.*?)\}", content, re.DOTALL)

all_vertices = []
all_faces = []
vertex_offset = 0

for block in off_blocks:
    lines = block.strip().splitlines()
    if not lines or not lines[0].strip().startswith("OFF"):
        continue

    header = lines[0].strip().split()
    n_verts, n_faces = int(header[1]), int(header[2])
    verts = [list(map(float, line.strip().split())) for line in lines[1 : 1 + n_verts]]
    faces = [
        list(map(int, line.strip().split()[1:4]))
        for line in lines[1 + n_verts : 1 + n_verts + n_faces]
    ]

    # Adjust indices
    faces = [[v + vertex_offset for v in face] for face in faces]
    all_vertices.extend(verts)
    all_faces.extend(faces)
    vertex_offset += n_verts

# Prepare for plotting
x, y, z = zip(*all_vertices)
i, j, k = zip(*all_faces)

fig = go.Figure(
    data=[go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, opacity=0.6, color="lightblue")]
)
fig.update_layout(scene=dict(aspectmode="data"))
fig.show()
