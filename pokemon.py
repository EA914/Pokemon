import tkinter as tk
import requests
import pygame
from io import BytesIO
from PIL import Image, ImageTk

pygame.init()

def get_pokemon_data(pokemon_name):
	url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
	response = requests.get(url)
	data = response.json()
	return data

def get_pokemon_evolution_chain(pokemon_name):
	url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"
	response = requests.get(url)
	data = response.json()
	evolution_chain_url = data["evolution_chain"]["url"]
	evolution_chain_response = requests.get(evolution_chain_url)
	evolution_chain_data = evolution_chain_response.json()
	return evolution_chain_data

def display_pokemon_image(pokemon_name):
	pokemon_data = get_pokemon_data(pokemon_name)
	sprite_url = pokemon_data["sprites"]["front_default"]
	response = requests.get(sprite_url)
	image_data = BytesIO(response.content)
	image = Image.open(image_data)
	photo = ImageTk.PhotoImage(image)
	image_label.config(image=photo)
	image_label.image = photo  # Keep a reference to prevent garbage collection

def display_evolution_chain(pokemon_name):
	# Destroy existing cry buttons and image
	for widget in root.winfo_children():
		if widget.winfo_class() == "Button" and widget.cget("text").startswith("Cry"):
			widget.destroy()
	image_label.config(image="")

	evolution_chain_data = get_pokemon_evolution_chain(pokemon_name)
	chain = evolution_chain_data["chain"]
	evolution_chain = []
	while chain:
		species_name = chain["species"]["name"]
		evolution_chain.append(species_name)
		if chain["evolves_to"]:
			chain = chain["evolves_to"][0]
		else:
			break
	evolution_chain_str = " --> ".join(evolution_chain)
	evolution_label.config(text=evolution_chain_str)

	# Create "Cry" buttons
	pokemon_data = get_pokemon_data(pokemon_name)
	cries = pokemon_data["cries"]
	for i, cry_url in enumerate(cries.values()):
		button = tk.Button(root, text=f"Cry {i+1}", command=lambda cry_url=cry_url: play_cry(cry_url))
		button.pack()

	# Display Pokémon image
	display_pokemon_image(pokemon_name)

def play_cry(cry_url):
	cry_response = requests.get(cry_url)
	cry_data = BytesIO(cry_response.content)
	pygame.mixer.music.load(cry_data)
	pygame.mixer.music.play()

def on_go_click():
	pokemon_name = pokemon_entry.get().lower()
	display_evolution_chain(pokemon_name)

root = tk.Tk()
root.title("Pokemon Explorer")

pygame.mixer.music.set_volume(0.5)	# Set initial volume

pokemon_label = tk.Label(root, text="Enter Pokemon Name:")
pokemon_label.pack()

pokemon_entry = tk.Entry(root)
pokemon_entry.pack()

go_button = tk.Button(root, text="Go", command=on_go_click)
go_button.pack()

evolution_label = tk.Label(root, text="")
evolution_label.pack()

image_label = tk.Label(root)
image_label.pack()

root.mainloop()
