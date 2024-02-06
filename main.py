from fastapi import FastAPI
import pandas as pd

df_userforgenre = pd.read_csv('./data/user_for_genre.csv')

app = FastAPI()

@app.get('/UsrForGenre')
def get_user_for_genre(genero: str = None ) -> dict:
    """reune el jugador que mas ah jugado por genero especifico    
    Argumentos:
        genero (str, optional): insertar genero del juego. Defaults to None.
    Returns:
        dict:
    """
    df_filtrado_por_genero = df_userforgenre[df_userforgenre['genres'] == genero]
    usuario_horas = df_filtrado_por_genero.groupby('user_id')['playtime_forever'].sum()
    max_tiempo_x_usuario = usuario_horas.idxmax()

    return {
        'Usuario con mas horas jugadas para el genero{}'.format(genero) : max_tiempo_x_usuario
        }