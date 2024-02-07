import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import gzip

app = FastAPI()

'''
Cargamos los datos con los que se trabajaran
'''

df_userforgenre = pd.read_csv('./data/user_for_genre.csv')
df_user_reviews = pd.read_csv('./data/user_reviews.csv')

def function_df(ruta):
    # Descomprimir el archivo JSON usando gzip y cargar los datos en un DataFrame
    with gzip.open(ruta, "rb") as archivo_comprimido:
    # Cargar los datos JSON
        df = pd.read_json(archivo_comprimido, lines=True)
    return df

df_steam_games = function_df('./data/clean_steam_games.json.gz')
df_user_reviews = function_df('./data/clean_user_reviews.json.gz')
df_user_items = function_df('./data/clean_user_items.json.gz')

# Convierte la columna 'release_date' a tipo datetime
df_steam_games['release_date'] = pd.to_datetime(df_steam_games['release_date'], errors='coerce')

# Elimina los registros con NaT en la columna 'release_date'
df_steam_games = df_steam_games.dropna(subset=['release_date'])

@app.get("/Desarrollador")
async def developer( desarrollador : str ):
    '''
    Calcula cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora

    Parametros: desarrollador : str Ejemplos: Valve, poppermost productions, bethesda

    Retorno
    -------
    Año, Cantidad de items, porcentaje contenido free

    '''
    #Transformar la columna "developer" y "price" en str en letra minuscula
    df_steam_games['developer'] = df_steam_games['developer'].astype(str).str.lower()
    df_steam_games['price'] = df_steam_games['price'].astype(str).str.lower()
    desarrollador.lower()

    #Filtrar por desarrollador
    developer_df = df_steam_games[df_steam_games['developer'].str.contains(desarrollador, case=False)]

    if developer_df.empty:
        print(f"No hay existe el desarrollador {desarrollador}.")
        return None

    estadisticas_desarrolladores = []

    for developer, juegos in developer_df.groupby('developer'):
        total_juegos = len(juegos)
        juegos_free = juegos[juegos['price'].str.contains('free', case=False)]
        total_juegos_free = len(juegos_free)

        porcentaje_free = (total_juegos_free / total_juegos) * 100 if total_juegos > 0 else 0

        estadisticas = {
            'desarrollador': developer,
            'total_juegos': total_juegos,
            'porcentaje_free': porcentaje_free
        }

        estadisticas_desarrolladores.append(estadisticas)

    return estadisticas_desarrolladores



@app.get("/UDS x Usuarios")
async def userdata( User_id : str ):
    '''
    Calcula:
        cantidad de dinero gastado por un usuario
        porcentaje de recomendación en base a reviews.recommend
        cantidad de items

    Parametros: User_id : str Ejemplos: evcentric, DJKamBer, 76561198254993106, kimjongadam

    Retorno
    -------
    {"Usuario X" : nombre de usuario, "Dinero gastado": x USD, "% de recomendación": x%, "cantidad de items": x}

    '''
    df_merged = pd.merge(df_steam_games, df_user_reviews, on='item_id')
    juegos_comprados = df_merged[df_merged['user_id'] == User_id].copy()
    juegos_comprados['price'] = juegos_comprados['price'].astype(str)
    juegos_comprados.loc[juegos_comprados['price'].str.contains(r'(?i)\bfree\b'), 'price'] = 0
    juegos_comprados['price'] = juegos_comprados['price'].astype(float)
    juegos_comprados['price'] = pd.to_numeric(juegos_comprados['price'], errors='coerce')
    # Dinero gastado por el usuario
    dinero_gastado = round(juegos_comprados['price'].sum(), 2)

    # Porcentaje de recomendación
    total_reviews = juegos_comprados.shape[0]
    reviews_recomendadas = juegos_comprados[juegos_comprados['recommend'] == True].shape[0]
    porcentaje_recomendacion = (reviews_recomendadas / total_reviews) * 100 if total_reviews > 0 else 0

    # Cantidad de items
    cantidad_items = juegos_comprados.shape[0]

    return {
        "Usuario           ": User_id,
        "Dinero gastado    ": f"{dinero_gastado} USD",
        "% de recomendación": f"{porcentaje_recomendacion}%",
        "Cantidad de items ": cantidad_items
    }




@app.get("/UsrForGenre")
def get_user_for_genre(genero: str = None )-> dict:
    """Muestra el jugador que mas a jugado por genero especifico y horas totales por año

    Argumentos:
        genero (str, optional): insertar genero del juego.
        Ej: action, adventure, casual, free to play, indie, rpg, simulation, strategy
    Returns:
        dict:
    """
    df_filtrado_por_genero = df_userforgenre[df_userforgenre['genres'] == genero]
    usuario_horas = df_filtrado_por_genero.groupby('user_id')['playtime_forever'].sum()
    max_tiempo_x_usuario = usuario_horas.idxmax()

    df_max_usuario = df_filtrado_por_genero[df_filtrado_por_genero['user_id'] == max_tiempo_x_usuario]
    horas_x_anio = df_max_usuario.groupby('release_year')['playtime_forever'].sum().reset_index()
    lista_x_anio = [
        {'Año':year ,  'Horas': hours} for year, hours in zip(horas_x_anio['release_year'], horas_x_anio['playtime_forever'])
    ]

    resultado = {
        'USUARIO con mas horas jugadas para el genero: {}'.format(genero) : max_tiempo_x_usuario,
        'Cantida de horas jugadas por año: ': lista_x_anio
    }

    return resultado



@app.get("/Mejores Desarrolladores")
async def best_developer_year( año : int ):
    '''
    Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado.
    (reviews.recommend = True y comentarios positivos)

    Parametros: año : int Ejemplos: desde el año 1995 al 2017

    Retorno
    -------
    [{"Puesto x1" : X}, {"Puesto x2" : Y},{"Puesto x3" : Z}]

    '''
    # Convierte la columna 'release_date' a tipo datetime
    df_steam_games['release_date'] = pd.to_datetime(df_steam_games['release_date'], errors='coerce')
    df_completo = pd.merge(df_steam_games, df_user_reviews, on='item_id', how='inner')
    juegos_del_año = df_completo[df_completo['release_date'].dt.year == año]
    juegos_recomendados = juegos_del_año[juegos_del_año['recommend'] == True]
    comentarios_positivos = juegos_del_año[juegos_del_año['sentiment_analysis'] == 2]
    recomendaciones_por_desarrollador = juegos_recomendados.groupby('developer').size()
    comentarios_por_desarrollador = comentarios_positivos.groupby('developer').size()

    # Calcular la puntuación total por desarrollador sumando recomendaciones y comentarios positivos
    puntuacion_por_desarrollador = recomendaciones_por_desarrollador.add(comentarios_por_desarrollador, fill_value=0)

    # Seleccionar los tres primeros desarrolladores con la puntuación más alta
    top_3_desarrolladores = puntuacion_por_desarrollador.nlargest(3)

    # Crear la lista de retorno en el formato especificado
    retorno = [{"Puesto {}: {}".format(i+1, desarrollador): puntuacion} for i, (desarrollador, puntuacion) in enumerate(top_3_desarrolladores.items())]

    if top_3_desarrolladores.empty:
        print(f"No hay registros para el año {año}.")
        return None
    
    return retorno



@app.get("/sentiment_analysis/{año}", response_model=dict)
def sentiment_analysis(año: int):
    try:
        sentiment_counts = df_user_reviews[df_user_reviews['año'] == año]['sentiment_analysis'].value_counts().to_dict()
        return sentiment_counts

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
