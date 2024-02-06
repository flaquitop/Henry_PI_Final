![alt text](data\mlops.jpg)

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1 - Machine Learning Operations (MLOps)** </h1>



## Descripción del proyecto:

### Este proyecto individual tiene como objetivo poner en práctica los conocimientos adquiridos en la etapa de labs sobre Machine Learning Operations (MLOps). Se te asignará el rol de un MLOps Engineer y deberás desarrollar un sistema de recomendación de videojuegos para la plataforma Steam.

### Contexto:

### Te has unido al equipo de Data Science de Steam y te encomiendan la tarea de crear un sistema de recomendación de videojuegos para mejorar la experiencia de usuario.

### Tareas a realizar:

#### Preparación de datos:

## Datos

Los datos empleados para este proyecto se encuentran en tres archivos JSON con una estructura anidada:

- australian_user_reviews.json: contiene las reseñas de los usuarios sobre los juegos que han jugado.
- australian_users_items.json: contiene la información de los usuarios, los juegos que poseen y las horas que han jugado.
- output_steam_games.json: contiene la información de los juegos disponibles en Steam, como el nombre, el género, el precio, etc.


Limpiar y transformar los datos proporcionados.

Crear la nueva columna 'sentiment_analysis' mediante análisis de sentimiento con NLP.

Eliminar las columnas que no sean necesarias.



## Desarrollo de la API:

### Implementar la API usando el framework FastAPI.



Definir las siguientes funciones para los endpoints:

**`developer(desarrollador: str):`** Devuelve la cantidad de items y el porcentaje de contenido Free por año según empresa desarrolladora.

**`userdata(User_id: str):`** Devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y la cantidad de items.

**`UserForGenre(genero: str):`** Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

**`best_developer_year(año: int):`** Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado.

**`developer_reviews_analysis(desarrolladora: str):`** Devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.



# Análisis exploratorio de datos (EDA):

### Investigar las relaciones entre las variables del dataset.

### Detectar outliers o anomalías.

### Identificar patrones interesantes.



# Modelo de aprendizaje automático:

Implementar un sistema de recomendación basado en similitud del coseno o filtro user-item.

Entrenar el modelo de ML.

Definir las funciones recomendacion_juego(id_producto: int) y recomendacion_usuario(id_usuario: int) en la API.


### Video:

Crear un video de máximo 7 minutos que muestre:

Presentación del proyecto.

Funcionamiento de las consultas de la API.

Breve explicación del modelo de ML utilizado.


### Recursos:

Dataset: Carpeta con el archivo que requieren ser procesados.

Diccionario de datos: Diccionario con algunas descripciones de las columnas disponibles en el dataset.


### Criterios de evaluación:


Código: Prolijidad, uso de clases y/o funciones, comentarios.

Repositorio: Nombres de archivo adecuados, uso de carpetas, README.md.

Cumplimiento de los requerimientos de aprobación.

Link de acceso al video (alojado en YouTube, Drive o similar).

Diferencia entre MVP y producto completo:

Un MVP cumple con las funcionalidades básicas del sistema.
Un producto completo incluye funcionalidades adicionales, pruebas exhaustivas y documentación completa.



Este README.md es una guía inicial. Puedes sugerir modificarlo y ampliarlo según consideres necesario al 

#### email martinmolina@gmail.com

¡Buena suerte!