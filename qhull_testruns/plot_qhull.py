import plotly.graph_objects as go
import numpy as np

def plot_qhull_output(data_file='data_output.txt'):
    with open(data_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    dim = int(lines[0])
    n_points, n_facets, n_ridges = map(int, lines[1].split())

    # Read points
    points = []
    for i in range(2, 2 + n_points):
        coords = list(map(float, lines[i].split()))
        points.append(coords)
    points = np.array(points)

    # Read facets (indices are 0-based)
    facets = []
    for i in range(2 + n_points, 2 + n_points + n_facets):
        parts = list(map(int, lines[i].split()))
        n_vertices = parts[0]
        indices = parts[1:]  # Already 0-based
        facets.append(indices)

    # Create the figure
    fig = go.Figure()

    # Add points
    fig.add_trace(go.Scatter(
        x=points[:, 0],
        y=points[:, 1],
        mode='markers',
        name='Points',
        marker=dict(
            size=8,
            color='blue',
            symbol='circle'
        )
    ))

    # Add facets
    for i, facet in enumerate(facets):
        # Close the polygon by repeating the first point at the end
        facet_closed = facet + [facet[0]] if len(facet) > 1 else facet
        polygon = points[facet_closed]
        
        fig.add_trace(go.Scatter(
            x=polygon[:, 0],
            y=polygon[:, 1],
            mode='lines',
            name=f'Facet {i+1}',
            line=dict(
                color='red',
                width=2
            ),
            showlegend=False
        ))

    # Update layout
    fig.update_layout(
        title='Qhull Output: Points and Polygon',
        xaxis_title='X',
        yaxis_title='Y',
        template='plotly_white',  # Clean, modern template
        hovermode='closest',
        width=800,
        height=800,
        showlegend=True
    )

    # Make the plot square
    fig.update_xaxes(
        scaleanchor="y",
        scaleratio=1,
    )

    # Save the plot as an HTML file for interactive viewing
    fig.write_html('qhull_visualization.html')
    
    # Also show the plot in the notebook if running in a Jupyter environment
    fig.show()

if __name__ == "__main__":
    plot_qhull_output() 