# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
import requests

def conseguirimagenesAPI():
    url = "https://rickandmortyapi.com/api/character" 
    contenido = requests.get(url)
    if contenido.status_code == 200:
        return contenido.json().get('results', []) 
    return []


def getAllImages(input=None):
    
    json_collection = repositories.conseguirimagenesAPI() 
    
    images = []  
    
    for personaje in json_collection:
        card = {
            'name': personaje.get('name'),
            'url': personaje.get('image'),
            'status': personaje.get('status'),
            'last_location': personaje.get('location', {}).get('name', 'Desconocido'),
            'first_seen': personaje.get('origin', {}).get('name', 'Desconocido')[0]
        }
   
        if input:
            if input.lower() in card['name'].lower():
                images.append(card)
        else:
            images.append(card)
    
    return images


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request del template en una Card.
    fav.user = '' # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.