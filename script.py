import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class Photo:
    def __init__(self, root, folder_path):
        self.root = root
        self.folder_path = folder_path
        self.photos = self.load_photos()
        self.photo_index = 0
        self.slide_show_active = False

        self.root.title("Visionneuse de Photos")
        self.root.geometry("800x600")

        # Cadre pour l'image
        self.frame_image = tk.Frame(root, width=800, height=540)  # Taille fixe pour l'image
        self.frame_image.place(x=0, y=0)

        # Widget pour afficher l'image
        self.image_label = tk.Label(self.frame_image)
        self.image_label.pack(fill="both", expand=True)

        # Cadre pour les boutons en bas (fond blanc)
        self.frame_controls = tk.Frame(root, bg="white", height=60, width=800)
        self.frame_controls.place(x=0, y=540)

        # Bouton précédent
        self.prec_button = tk.Button(self.frame_controls, text="< Précédent", command=self.prev_photo)
        self.prec_button.place(x=10, y=10)

        # Bouton suivant
        self.suiv_button = tk.Button(self.frame_controls, text="Suivant >", command=self.next_photo)
        self.suiv_button.place(x=700, y=10)

        # Bouton pour démarrer/arrêter le diaporama
        self.slide_button = tk.Button(self.frame_controls, text="Démarrer le Diaporama", command=self.toggle_slideshow)
        self.slide_button.place(x=350, y=10)

        # Ajouter les raccourcis clavier
        self.root.bind("<Left>", self.prev_photo)  # Flèche gauche
        self.root.bind("<Right>", self.next_photo)  # Flèche droite
        self.root.bind("<space>", self.toggle_slideshow)  # Espace pour démarrer/arrêter le diaporama

        self.update_photo()

    def load_photos(self):
        photos = [os.path.join(self.folder_path, filename) 
                  for filename in os.listdir(self.folder_path) 
                  if filename.lower().endswith((".jpg", ".png", ".jpeg", ".gif", ".bmp"))]
        return photos

    def update_photo(self):
        if not self.photos:
            print("Aucune image trouvée.")
            return

        img = Image.open(self.photos[self.photo_index])
        window_width, window_height = 800, 600
        img_width, img_height = img.size
        scale = min(window_width / img_width, window_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        img = img.resize((new_width, new_height), Image.LANCZOS)
        background = Image.new("RGB", (window_width, window_height), "black")
        x_offset = (window_width - new_width) // 2
        y_offset = (window_height - new_height) // 2
        background.paste(img, (x_offset, y_offset))

        img = ImageTk.PhotoImage(background)
        self.image_label.config(image=img)
        self.image_label.image = img

    def prev_photo(self, event=None):  # Raccourci pour la flèche gauche
        if self.photo_index > 0:
            self.photo_index -= 1
            self.update_photo()

    def next_photo(self, event=None):  # Raccourci pour la flèche droite
        if self.photo_index < len(self.photos) - 1:
            self.photo_index += 1
            self.update_photo()

    def toggle_slideshow(self, event=None):  # Raccourci pour l'espace
        self.slide_show_active = not self.slide_show_active
        if self.slide_show_active:
            self.slide_button.config(text="Arrêter le Diaporama")
            self.start_slide_show()
        else:
            self.slide_button.config(text="Démarrer le Diaporama")
            self.stop_slide_show()

    def start_slide_show(self):
        if self.slide_show_active:
            self.next_photo()
            self.slide_show_timer = self.root.after(3000, self.start_slide_show)  # Change image every 3 seconds

    def stop_slide_show(self):
        if self.slide_show_active:
            self.root.after_cancel(self.slide_show_timer)  # Stop the slideshow

if __name__ == "__main__":
    root = tk.Tk()

    folder_path = filedialog.askdirectory(title="Sélectionner un dossier contenant des images")
    if not folder_path:
        print("Aucun dossier sélectionné. Fermeture du programme.")
        root.destroy()
        exit()

    app = Photo(root, folder_path)
    root.mainloop()
