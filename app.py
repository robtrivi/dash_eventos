import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import os

# --------------------------------------------------------------------
# LECTURA DE DATOS
# --------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_VENTAS = os.path.join(BASE_DIR, "ventas_eventos.csv")
PATH_VISTAS = os.path.join(BASE_DIR, "vistas_eventos.csv")

df_ventas = pd.read_csv(PATH_VENTAS, parse_dates=["Fecha"])
df_vistas = pd.read_csv(PATH_VISTAS, parse_dates=["Fecha"])

# --------------------------------------------------------------------
# INICIALIZAR APP
# --------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# --------------------------------------------------------------------
# ESTILOS DE TABS
# --------------------------------------------------------------------
tabs_styles = {
    "height": "45px",
    "border": "none",
}
tab_style = {
    "padding": "8px",
    "fontWeight": "bold",
    "backgroundColor": "#e9ecef",
    "borderRadius": "5px",
    "margin": "2px",
    "color": "#333",
    "border": "none"
}
tab_selected_style = {
    "padding": "8px",
    "fontWeight": "bold",
    "backgroundColor": "#007bff",
    "color": "white",
    "borderRadius": "5px",
    "margin": "2px",
    "border": "none"
}

# --------------------------------------------------------------------
# LAYOUT
# --------------------------------------------------------------------
app.layout = dbc.Container(
    fluid=True,
    style={
        "height": "100vh",
        "overflow": "hidden",  
        "backgroundColor": "#f0f2f5",
        "padding": "0"
    },
    children=[

        # ENCABEZADO
        dbc.Row(
            style={"height": "60px", "backgroundColor": "white", "margin": "0.5rem"},
            children=[
                dbc.Col(
                    html.H1(
                        "Dashboard de Métricas de Eventos",
                        style={"textAlign": "center", "margin": "0.5rem"}
                    ),
                    width=12
                )
            ],
        ),

        # CONTENEDOR DE TABS (OCUPA EL RESTO DE LA ALTURA)
        dbc.Row(
            style={"height": "calc(100vh - 60px)", "margin": "0"},
            children=[
                dbc.Col(
                    dcc.Tabs(
                        style=tabs_styles,
                        children=[

                            # ========== TAB 1: TASA DE CONVERSIÓN ========== 
                            dcc.Tab(
                                label="Tasa de Conversión de Ventas",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Row(
                                        style={"height": "100%", "margin": "0"},
                                        children=[
                                            # Columna de FILTROS (width=2)
                                            dbc.Col(
                                                width=2,
                                                style={
                                                    "backgroundColor": "#ffffff",
                                                    "padding": "1rem",
                                                    "borderRadius": "5px",
                                                    "maxHeight": "100%",
                                                    "overflowY": "visible"
                                                },
                                                children=[
                                                    html.H5("Filtros", style={"marginBottom": "1rem"}),

                                                    html.P(
                                                        "La tasa de conversión de ventas mide cuántas "
                                                        "visualizaciones se convirtieron en ventas exitosas.",
                                                        style={"marginBottom": "1rem"}
                                                    ),

                                                    html.Label("Tipo de análisis:"),
                                                    dcc.RadioItems(
                                                        id="tipo-analisis-conversion",
                                                        options=[
                                                            {"label": "Mostrar todo", "value": "todo"},
                                                            {"label": "Comparar por ciudades", "value": "comparar"}
                                                        ],
                                                        value="todo",
                                                        inline=True,
                                                        style={"marginBottom": "1rem"}
                                                    ),

                                                    html.Label("Rango de fechas:"),
                                                    dcc.DatePickerRange(
                                                        id="rango-fechas-conversion",
                                                        start_date=df_ventas["Fecha"].min(),
                                                        end_date=df_ventas["Fecha"].max(),
                                                        display_format="YYYY-MM-DD",
                                                        style={"marginBottom": "1rem"}
                                                    ),

                                                    html.Label("Filtrar por ciudad:"),
                                                    dcc.Dropdown(
                                                        id="filtro-ciudad-conversion",
                                                        options=[{"label": c, "value": c} 
                                                                 for c in df_ventas["Ubicación"].unique()],
                                                        value=df_ventas["Ubicación"].unique(),
                                                        multi=True,
                                                        style={"marginBottom": "1rem"}
                                                    ),
                                                ]
                                            ),

                                            # Columna de GRÁFICA (width=10)
                                            dbc.Col(
                                                width=10,
                                                style={"padding": "1rem", "overflowY": "auto"},
                                                children=[
                                                    dcc.Graph(id="grafico-conversion", style={"height": "100%"})
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),

                            # ========== TAB 2: ÍNDICE DE RENTABILIDAD ========== 
                            dcc.Tab(
                                label="Índice de Rentabilidad",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Row(
                                        style={"height": "100%", "margin": "0"},
                                        children=[
                                            # Columna FILTROS (width=2)
                                            dbc.Col(
                                                width=2,
                                                style={
                                                    "backgroundColor": "#ffffff",
                                                    "padding": "1rem",
                                                    "borderRadius": "5px",
                                                    "maxHeight": "100%",
                                                    "overflowY": "visible"
                                                },
                                                children=[
                                                    html.H5("Filtros", style={"marginBottom": "1rem"}),

                                                    html.Label("Filtrar por categoría:"),
                                                    dcc.Dropdown(
                                                        id="filtro-categoria",
                                                        options=[{"label": cat, "value": cat} 
                                                                 for cat in df_ventas["Categoría"].unique()],
                                                        value=df_ventas["Categoría"].unique(),
                                                        multi=True,
                                                        style={"marginBottom": "1rem"}
                                                    ),

                                                    html.Label("Filtrar por ciudad:"),
                                                    dcc.Dropdown(
                                                        id="filtro-ciudad-rentabilidad",
                                                        options=[{"label": c, "value": c} 
                                                                 for c in df_ventas["Ubicación"].unique()],
                                                        value=df_ventas["Ubicación"].unique(),
                                                        multi=True,
                                                        style={"marginBottom": "1rem"}
                                                    ),
                                                    html.P(
                                                        "Visualizamos la evolución a lo largo del tiempo "
                                                        "para ver tendencias en la rentabilidad.",
                                                        style={"fontSize": "80%", "color": "#666"}
                                                    )
                                                ]
                                            ),

                                            # Columna de GRÁFICA (width=10)
                                            dbc.Col(
                                                width=10,
                                                style={"padding": "1rem", "overflowY": "auto", "height": "100%"},
                                                children=[
                                                    dcc.Graph(id="grafico-rentabilidad", style={"height": "100%"})
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),

                            # ========== TAB 3: SATISFACCIÓN DEL CLIENTE (SIN FECHAS) ==========
                            dcc.Tab(
                                label="Satisfacción del Cliente",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Row(
                                        style={"height": "100%", "margin": "0"},
                                        children=[
                                            # Filtros (width=2)
                                            dbc.Col(
                                                width=2,
                                                style={
                                                    "backgroundColor": "#ffffff",
                                                    "padding": "1rem",
                                                    "borderRadius": "5px",
                                                    "maxHeight": "100%",
                                                    "overflowY": "visible"
                                                },
                                                children=[
                                                    html.H5("Filtros", style={"marginBottom": "1rem"}),

                                                    html.Label("Tipo de análisis:"),
                                                    dcc.RadioItems(
                                                        id="tipo-analisis-satisfaccion",
                                                        options=[
                                                            {"label": "Comparar por eventos", "value": "comparar"},
                                                            {"label": "Promedio general", "value": "general"}
                                                        ],
                                                        value="general",
                                                        inline=True,
                                                        style={"marginBottom": "1rem"}
                                                    ),
                                                    html.Label("Filtrar por evento:"),
                                                    dcc.Dropdown(
                                                        id="filtro-evento",
                                                        options=[{"label": e, "value": e} 
                                                                 for e in df_ventas["Evento"].unique()],
                                                        value=df_ventas["Evento"].unique(),
                                                        multi=True,
                                                        style={"marginBottom": "1rem"}
                                                    ),
                                                    html.Label("Filtrar por ciudad:"),
                                                    dcc.Dropdown(
                                                        id="filtro-ciudad-satisfaccion",
                                                        options=[{"label": c, "value": c} 
                                                                 for c in df_ventas["Ubicación"].unique()],
                                                        value=df_ventas["Ubicación"].unique(),
                                                        multi=True,
                                                        style={"marginBottom": "1rem"}
                                                    ),
                                                    html.Div(
                                                        "Este gráfico muestra solo la calificación promedio "
                                                        "por Evento y Ciudad, sin usar la fecha.",
                                                        style={"fontSize": "80%", "color": "#666"}
                                                    )
                                                ]
                                            ),
                                            # Gráfica (width=10)
                                            dbc.Col(
                                                width=10,
                                                style={"padding": "1rem", "overflowY": "auto"},
                                                children=[
                                                    dcc.Graph(id="grafico-satisfaccion", style={"height": "100%"})
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    width=12
                )
            ]
        )
    ]
)

# --------------------------------------------------------------------
# CALLBACKS
# --------------------------------------------------------------------

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
        conversion_total["Tasa de Conversión"] = (
            conversion_total["Entradas Vendidas"] / conversion_total["Tiempo de Visualización"]
        )
        fig = px.line(
            conversion_total,
            x="Fecha",
            y="Tasa de Conversión",
            title="Tasa de Conversión de Ventas Total",
            labels={"Tasa de Conversión": "Tasa de Conversión"}
        )

    return fig

@app.callback(
    Output("grafico-rentabilidad", "figure"),
    Input("filtro-categoria", "value"),
    Input("filtro-ciudad-rentabilidad", "value")
)
def actualizar_rentabilidad(categorias_seleccionadas, ciudades_seleccionadas):
    df_filtrado = df_ventas[
        (df_ventas["Categoría"].isin(categorias_seleccionadas)) &
        (df_ventas["Ubicación"].isin(ciudades_seleccionadas))
    ]
    # Margen Bruto = Ventas (Total) - Descuento
    df_filtrado["Margen Bruto"] = df_filtrado["Total"] - df_filtrado["Descuento"]
    # Índice de Rentabilidad = Margen Bruto / Ventas (Total)
    df_filtrado["Índice de Rentabilidad"] = df_filtrado["Margen Bruto"] / df_filtrado["Total"]

    # AGRUPAMOS POR FECHA Y CATEGORÍA para ver la evolución en el tiempo
    df_grouped = df_filtrado.groupby(["Fecha", "Categoría"])["Índice de Rentabilidad"].mean().reset_index()

    # Gráfico de líneas
    fig = px.line(
        df_grouped,
        x="Fecha",
        y="Índice de Rentabilidad",
        color="Categoría",
        title="Índice de Rentabilidad a lo largo del tiempo",
        labels={"Índice de Rentabilidad": "Índice de Rentabilidad"}
    )
    return fig


@app.callback(
    Output("grafico-satisfaccion", "figure"),
    Input("filtro-evento", "value"),
    Input("filtro-ciudad-satisfaccion", "value"),
    Input("tipo-analisis-satisfaccion", "value")
)
def actualizar_satisfaccion(eventos_seleccionados, ciudades_seleccionadas, tipo_analisis):
    """
    Queremos ver la satisfacción: SÓLO 'Evento' y 'Ciudad'
    - 'comparar': agrupar por [Evento, Ubicación]
    - 'general': agrupar solo por [Evento]
    """
    df_filtrado = df_ventas[
        (df_ventas["Evento"].isin(eventos_seleccionados)) &
        (df_ventas["Ubicación"].isin(ciudades_seleccionadas))
    ]
    df_filtrado["Satisfacción"] = pd.to_numeric(df_filtrado["Satisfacción"], errors="coerce")
    df_filtrado = df_filtrado.dropna(subset=["Satisfacción"])

    if tipo_analisis == "comparar":
        # Agrupamos por Evento y Ubicación
        df_grouped = df_filtrado.groupby(["Evento", "Ubicación"])["Satisfacción"].mean().reset_index()
        # Graficamos BARRAS con x=Evento, color=Ubicación
        fig = px.bar(
            df_grouped,
            x="Evento",
            y="Satisfacción",
            color="Ubicación",
            barmode="group",  # Barras agrupadas
            title="Satisfacción Promedio por Evento y Ciudad",
            labels={"Satisfacción": "Promedio de Satisfacción"}
        )
    else:
        # Agrupamos sólo por Evento
        df_grouped = df_filtrado.groupby("Evento")["Satisfacción"].mean().reset_index()
        fig = px.bar(
            df_grouped,
            x="Evento",
            y="Satisfacción",
            title="Satisfacción Promedio General por Evento",
            labels={"Satisfacción": "Promedio de Satisfacción"}
        )

    # Ajustar el rango de 1 a 5
    fig.update_yaxes(range=[1, 5])
    return fig


# --------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
