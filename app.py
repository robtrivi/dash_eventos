import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Cargar datos sintéticos
df_ventas = pd.read_csv("ventas_eventos.csv", parse_dates=["Fecha"])
df_vistas = pd.read_csv("vistas_eventos.csv", parse_dates=["Fecha"])

# Crear aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Métricas de Eventos", style={"textAlign": "center"}),
    dcc.Tabs([
        dcc.Tab(label="Tasa de Conversión de Ventas", children=[
            html.Div([
                dcc.Graph(id="grafico-conversion"),
                html.Label("Filtrar por rango de fechas:"),
                dcc.DatePickerRange(
                    id="rango-fechas-conversion",
                    start_date=df_ventas["Fecha"].min(),
                    end_date=df_ventas["Fecha"].max(),
                    display_format="YYYY-MM-DD"
                ),
                html.Label("Filtrar por ciudad:"),
                dcc.Dropdown(
                    id="filtro-ciudad-conversion",
                    options=[{"label": ciudad, "value": ciudad} for ciudad in df_ventas["Ubicación"].unique()],
                    value=df_ventas["Ubicación"].unique(),
                    multi=True
                )
            ])
        ]),
        dcc.Tab(label="Índice de Rentabilidad", children=[
            html.Div([
                dcc.Graph(id="grafico-rentabilidad"),
                html.Label("Filtrar por categoría:"),
                dcc.Dropdown(
                    id="filtro-categoria",
                    options=[{"label": cat, "value": cat} for cat in df_ventas["Categoría"].unique()],
                    value=df_ventas["Categoría"].unique(),
                    multi=True
                ),
                html.Label("Filtrar por ciudad:"),
                dcc.Dropdown(
                    id="filtro-ciudad-rentabilidad",
                    options=[{"label": ciudad, "value": ciudad} for ciudad in df_ventas["Ubicación"].unique()],
                    value=df_ventas["Ubicación"].unique(),
                    multi=True
                )
            ])
        ]),
        dcc.Tab(label="Satisfacción del Cliente", children=[
            html.Div([
                dcc.Graph(id="grafico-satisfaccion"),
                html.Label("Filtrar por evento:"),
                dcc.Dropdown(
                    id="filtro-evento",
                    options=[{"label": evento, "value": evento} for evento in df_ventas["Evento"].unique()],
                    value=df_ventas["Evento"].unique(),
                    multi=True
                ),
                html.Label("Filtrar por ciudad:"),
                dcc.Dropdown(
                    id="filtro-ciudad-satisfaccion",
                    options=[{"label": ciudad, "value": ciudad} for ciudad in df_ventas["Ubicación"].unique()],
                    value=df_ventas["Ubicación"].unique(),
                    multi=True
                )
            ])
        ]),
        dcc.Tab(label="Tiempo de Visualización", children=[
            html.Div([
                dcc.Graph(id="grafico-visualizacion"),
                html.Label("Filtrar por rango de fechas:"),
                dcc.DatePickerRange(
                    id="rango-fechas-visualizacion",
                    start_date=df_vistas["Fecha"].min(),
                    end_date=df_vistas["Fecha"].max(),
                    display_format="YYYY-MM-DD"
                )
            ])
        ])
    ])
])

# Callback para la tasa de conversión de ventas
@app.callback(
    Output("grafico-conversion", "figure"),
    Input("rango-fechas-conversion", "start_date"),
    Input("rango-fechas-conversion", "end_date"),
    Input("filtro-ciudad-conversion", "value")
)
def actualizar_conversion(start_date, end_date, ciudades_seleccionadas):
    # Filtrar datos según las selecciones
    df_ventas_filtrado = df_ventas[
        (df_ventas["Fecha"] >= start_date) &
        (df_ventas["Fecha"] <= end_date) &
        (df_ventas["Ubicación"].isin(ciudades_seleccionadas))
    ]
    df_vistas_filtrado = df_vistas[
        (df_vistas["Fecha"] >= start_date) &
        (df_vistas["Fecha"] <= end_date)
    ]
    
    # Agrupar datos por fecha
    ventas_agrupadas = df_ventas_filtrado.groupby("Fecha")["Entradas Vendidas"].sum().reset_index()
    vistas_agrupadas = df_vistas_filtrado.groupby("Fecha")["Tiempo de Visualización"].count().reset_index()
    
    # Combinar datos de ventas y vistas
    conversion = pd.merge(ventas_agrupadas, vistas_agrupadas, on="Fecha", how="inner")
    conversion["Tasa de Conversión"] = conversion["Entradas Vendidas"] / conversion["Tiempo de Visualización"]
    
    # Crear gráfico de línea
    fig = px.line(
        conversion,
        x="Fecha",
        y="Tasa de Conversión",
        title="Tasa de Conversión de Ventas",
        labels={"Tasa de Conversión": "Tasa de Conversión"}
    )
    return fig

# Callback para el índice de rentabilidad
@app.callback(
    Output("grafico-rentabilidad", "figure"),
    Input("filtro-categoria", "value"),
    Input("filtro-ciudad-rentabilidad", "value")
)
def actualizar_rentabilidad(categorias_seleccionadas, ciudades_seleccionadas):
    # Filtrar datos según las selecciones
    df_filtrado = df_ventas[
        (df_ventas["Categoría"].isin(categorias_seleccionadas)) &
        (df_ventas["Ubicación"].isin(ciudades_seleccionadas))
    ]
    
    df_filtrado["Margen Bruto"] = df_filtrado["Total"] - df_filtrado["Descuento"]
    df_filtrado["Índice de Rentabilidad"] = df_filtrado["Margen Bruto"] / df_filtrado["Total"]
    
    # Agrupar por categoría y calcular el promedio del índice de rentabilidad
    df_grouped = df_filtrado.groupby("Categoría")["Índice de Rentabilidad"].mean().reset_index()
    
    # Crear gráfico de barras
    fig = px.bar(
        df_grouped,
        x="Categoría",
        y="Índice de Rentabilidad",
        title="Índice de Rentabilidad de Operaciones por Categoría",
        labels={"Índice de Rentabilidad": "Índice de Rentabilidad Promedio"}
    )
    
    # Agregar etiquetas a las barras
    fig.update_traces(text=df_grouped["Índice de Rentabilidad"].round(2), textposition="outside")
    return fig
# Callback para la satisfacción del cliente
@app.callback(
    Output("grafico-satisfaccion", "figure"),
    Input("filtro-evento", "value"),
    Input("filtro-ciudad-satisfaccion", "value")
)
def actualizar_satisfaccion(eventos_seleccionados, ciudades_seleccionadas):
    df_filtrado = df_ventas[
        (df_ventas["Evento"].isin(eventos_seleccionados)) &
        (df_ventas["Ubicación"].isin(ciudades_seleccionadas))
    ]
    df_filtrado["Satisfacción"] = pd.to_numeric(df_filtrado["Satisfacción"], errors="coerce")
    df_filtrado = df_filtrado.dropna(subset=["Satisfacción"])
    df_grouped = df_filtrado.groupby("Fecha")["Satisfacción"].mean().reset_index()
    fig = px.line(
        df_grouped,
        x="Fecha",
        y="Satisfacción",
        title="Satisfacción Promedio del Cliente",
        labels={"Satisfacción": "Promedio de Satisfacción"}
    )
    fig.update_yaxes(range=[1, 5])  # Fijar el rango de 1 a 5
    return fig

# Callback para el tiempo de visualización
@app.callback(
    Output("grafico-visualizacion", "figure"),
    Input("rango-fechas-visualizacion", "start_date"),
    Input("rango-fechas-visualizacion", "end_date")
)
def actualizar_visualizacion(start_date, end_date):
    df_filtrado = df_vistas[
        (df_vistas["Fecha"] >= start_date) &
        (df_vistas["Fecha"] <= end_date)
    ]
    df_grouped = df_filtrado.groupby("Fecha")["Tiempo de Visualización"].sum().reset_index()
    fig = px.line(
        df_grouped,
        x="Fecha",
        y="Tiempo de Visualización",
        title="Tiempo Total de Visualización por Fecha",
        labels={"Tiempo de Visualización": "Tiempo Total (segundos)"}
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
