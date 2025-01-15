import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os

# Obtener el directorio donde se ejecuta el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta completa al archivo
PATH_VENTAS = os.path.join(BASE_DIR, "ventas_eventos.csv")
PATH_VISTAS = os.path.join(BASE_DIR, "vistas_eventos.csv")

# Leer el archivo CSV
df_ventas = pd.read_csv(PATH_VENTAS, parse_dates=["Fecha"])
df_vistas = pd.read_csv(PATH_VISTAS, parse_dates=["Fecha"])

# Crear aplicación Dash
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Dashboard de Métricas de Eventos", style={"textAlign": "center"}),
    dcc.Tabs([
        dcc.Tab(label="Tasa de Conversión de Ventas", children=[
            html.Div([
                dcc.Graph(id="grafico-conversion"),
                html.P("La tasa de conversión de ventas mide cuántas visualizaciones se convirtieron en ventas exitosas."),
                html.Label("Tipo de análisis:"),
                dcc.RadioItems(
                    id="tipo-analisis-conversion",
                    options=[
                        {"label": "Mostrar todo", "value": "todo"},
                        {"label": "Comparar por ciudades", "value": "comparar"}
                    ],
                    value="todo",
                    inline=True
                ),
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
                html.P("El índice de rentabilidad refleja el margen bruto promedio en relación al total de ingresos."),
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
                html.P("La satisfacción del cliente mide el promedio de calificaciones recibidas por evento."),
                html.Label("Tipo de análisis:"),
                dcc.RadioItems(
                    id="tipo-analisis-satisfaccion",
                    options=[
                        {"label": "Comparar por eventos", "value": "comparar"},
                        {"label": "Promedio general", "value": "general"}
                    ],
                    value="general",
                    inline=True
                ),
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
                html.P("El tiempo total de visualización muestra la cantidad de tiempo dedicada a visualizar contenido por fecha."),
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
    Input("filtro-ciudad-conversion", "value"),
    Input("tipo-analisis-conversion", "value")
)
def actualizar_conversion(start_date, end_date, ciudades_seleccionadas, tipo_analisis):
    df_ventas_filtrado = df_ventas[
        (df_ventas["Fecha"] >= start_date) &
        (df_ventas["Fecha"] <= end_date) &
        (df_ventas["Ubicación"].isin(ciudades_seleccionadas))
    ]
    df_vistas_filtrado = df_vistas[
        (df_vistas["Fecha"] >= start_date) &
        (df_vistas["Fecha"] <= end_date)
    ]
    print(df_ventas_filtrado.columns)
    ventas_agrupadas = df_ventas_filtrado.groupby(["Fecha", "Ubicación"])["Entradas Vendidas"].sum().reset_index()
    vistas_agrupadas = df_vistas_filtrado.groupby(["Fecha", "Ubicación"])["Tiempo de Visualización"].count().reset_index()
    conversion = pd.merge(ventas_agrupadas, vistas_agrupadas, on=["Fecha", "Ubicación"], how="inner")
    conversion["Tasa de Conversión"] = conversion["Entradas Vendidas"] / conversion["Tiempo de Visualización"]

    if tipo_analisis == "comparar":
        fig = px.line(
            conversion,
            x="Fecha",
            y="Tasa de Conversión",
            color="Ubicación",
            title="Tasa de Conversión de Ventas por Ciudad",
            labels={"Tasa de Conversión": "Tasa de Conversión"}
        )
    else:
        conversion_total = conversion.groupby("Fecha").agg({
            "Entradas Vendidas": "sum",
            "Tiempo de Visualización": "sum"
        }).reset_index()
        conversion_total["Tasa de Conversión"] = conversion_total["Entradas Vendidas"] / conversion_total["Tiempo de Visualización"]
        fig = px.line(
            conversion_total,
            x="Fecha",
            y="Tasa de Conversión",
            title="Tasa de Conversión de Ventas Total",
            labels={"Tasa de Conversión": "Tasa de Conversión"}
        )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
