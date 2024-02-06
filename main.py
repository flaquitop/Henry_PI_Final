from fastapi import FastAPI
import pandas as pd

df_userforgenre = pd.read_csv('./data/user_for_genre.csv')

app = FastAPI()

@app.get("/UsrForGenre")
def get_user_for_genre(genero: str = None )-> dict:
    """reune el jugador que mas ah jugado por genero especifico    
    Argumentos:
        genero (str, optional): insertar genero del juego. Defaults to None.
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
        'Usuario con mas horas jugadas para el genero {}'.format(genero) : max_tiempo_x_usuario,
        'horas jugadas ': lista_x_anio
    }

    return resultado
