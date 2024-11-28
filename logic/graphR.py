import plotly.graph_objects as go

# Crear una gráfica simple
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 11, 12, 13],
    mode='lines+markers',
    name='Datos'
))

fig.update_layout(
    title="Ejemplo de Gráfica",
    xaxis_title="Eje X",
    yaxis_title="Eje Y"
)

# Guardar la gráfica en un archivo PNG
fig.write_image("grafica_ejemplo.png")

print("Gráfica guardada como 'grafica_ejemplo.png'")
