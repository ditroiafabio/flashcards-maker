import tkinter as tk
from tkinter import messagebox
from database import *
import random


class Application(tk.Tk):

  def __init__(self):
    super().__init__()
    self.title("Flashcards")
    self.geometry("600x600")
    self.configure(bg="#2c2d2e")

    # Initialisation de la base de donnees au demarrage
    initialiser_bd()

    # Definition des differentes vues de l'application
    self.homepage = tk.Frame(self, bg="#2c2d2e")
    self.subject_page = tk.Frame(self, bg="#2c2d2e")
    self.create_subject_page = tk.Frame(self, bg="#2c2d2e")

    # Construction des interfaces graphiques
    self.creer_homepage()
    self.creer_subject_page()
    self.creer_create_subject_page()

    # Affichage initial de la page d'accueil
    self.homepage.pack(fill="both", expand=True)

  def creer_homepage(self):
    # Titre principal
    title = tk.Label(
        self.homepage,
        text="Flashcards maker",
        font=("Arial", 30, "bold"),
        fg="#0f5d7b",
        bg="#2c2d2e",
    )
    title.pack(pady=40)

    # Bouton d' acces a la liste des sujets
    subject_list_btn = tk.Button(
        self.homepage,
        text="Subjects list",
        command=self.go_subject_list,
        font=("Arial", 15, "bold"),
        bg="#0f5d7b",
        fg="white",
    )
    subject_list_btn.pack(pady=10)

  def creer_subject_page(self):
    # Titre de la section
    title_subject_list = tk.Label(
        self.subject_page,
        text="Subjects list",
        font=("Arial", 30, "bold"),
        fg="#0f5d7b",
        bg="#2c2d2e",
    )
    title_subject_list.pack(pady=20)

    # Bouton de retour vers l'accueil
    btn_back = tk.Button(
        self.subject_page,
        text="Retour",
        command=self.go_homepage,
        font=("Arial", 12),
    )
    btn_back.pack(anchor="nw", padx=20, pady=10)

    # Bouton d' acces au formulaire de creation
    btn_go_create = tk.Button(
        self.subject_page,
        text="Creer un nouveau sujet",
        command=self.go_create_subject_page,
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
    )
    btn_go_create.pack(pady=10)

    # Cadre conteneur pour l'affichage dynamique des boutons de sujets
    self.frame_boutons_sujets = tk.Frame(self.subject_page, bg="#2c2d2e")
    self.frame_boutons_sujets.pack(fill="both", expand=True, padx=20, pady=10)

  def creer_create_subject_page(self):
    # Titre de la page de creation
    title_create = tk.Label(
        self.create_subject_page,
        text="Creer un sujet et des cartes",
        font=("Arial", 24, "bold"),
        fg="#0f5d7b",
        bg="#2c2d2e",
    )
    title_create.pack(pady=20)

    # Bouton de retour vers la liste des sujets
    btn_back = tk.Button(
        self.create_subject_page,
        text="Retour",
        command=self.go_subject_list,
        font=("Arial", 12),
    )
    btn_back.pack(anchor="nw", padx=20, pady=10)

    # Cadre du formulaire
    form_frame = tk.Frame(self.create_subject_page, bg="#2c2d2e")
    form_frame.pack(pady=10)

    # Champ de saisie du nom du sujet
    tk.Label(
        form_frame,
        text="Nom du sujet :",
        font=("Arial", 12),
        fg="white",
        bg="#2c2d2e",
    ).pack(anchor="w")
    self.entry_sujet = tk.Entry(form_frame, font=("Arial", 12), width=30)
    self.entry_sujet.pack(pady=5)

    # Champ de saisie de la question
    tk.Label(
        form_frame,
        text="Question :",
        font=("Arial", 12),
        fg="white",
        bg="#2c2d2e",
    ).pack(anchor="w", pady=(10, 0))
    self.entry_question = tk.Entry(form_frame, font=("Arial", 12), width=30)
    self.entry_question.pack(pady=5)

    # Champ de saisie de la reponse
    tk.Label(
        form_frame, text="Reponse :", font=("Arial", 12), fg="white", bg="#2c2d2e"
    ).pack(anchor="w", pady=(10, 0))
    self.entry_reponse = tk.Entry(form_frame, font=("Arial", 12), width=30)
    self.entry_reponse.pack(pady=5)

    # Bouton de validation de l'enregistrement
    btn_save = tk.Button(
        form_frame,
        text="Enregistrer la carte",
        command=self.sauvegarder_nouvelle_carte,
        font=("Arial", 12, "bold"),
        bg="#0f5d7b",
        fg="white",
    )
    btn_save.pack(pady=20)

  # --- GESTION DE LA NAVIGATION ---

  def go_homepage(self):
    # Masque les autres vues et affiche l'accueil
    self.subject_page.pack_forget()
    self.create_subject_page.pack_forget()
    self.homepage.pack(fill="both", expand=True)

  def go_subject_list(self):
    # Masque les autres vues, actualise et affiche la liste des sujets
    self.homepage.pack_forget()
    self.create_subject_page.pack_forget()
    self.subject_page.pack(fill="both", expand=True)
    self.charger_boutons_sujets()

  def go_create_subject_page(self):
    # Masque les autres vues, reinitialise les champs et affiche le formulaire
    self.subject_page.pack_forget()
    self.entry_sujet.delete(0, tk.END)
    self.entry_question.delete(0, tk.END)
    self.entry_reponse.delete(0, tk.END)
    self.create_subject_page.pack(fill="both", expand=True)

  # --- LOGIQUE DE DONNEES ET INTERFACE ---

  def charger_boutons_sujets(self):
    # Supprime les anciens boutons pour eviter les doublons
    for widget in self.frame_boutons_sujets.winfo_children():
      widget.destroy()

    # Recupere tous les sujets enregistres en base de donnees
    sujets = recuperer_sujets()

    if not sujets:
      lbl_vide = tk.Label(
          self.frame_boutons_sujets,
          text="Aucun sujet cree pour l'instant.",
          font=("Arial", 12),
          fg="white",
          bg="#2c2d2e",
      )
      lbl_vide.pack(pady=20)
      return

    # Genere un bouton interactif par sujet trouve
    for sujet_id, nom_sujet in sujets:
      btn = tk.Button(
          self.frame_boutons_sujets,
          text=nom_sujet,
          font=("Arial", 14, "bold"),
          bg="#0f5d7b",
          fg="white",
          command=lambda s_id=sujet_id, s_nom=nom_sujet: self.open_subjects(
              s_id, s_nom
          ),
      )
      btn.pack(fill="x", pady=5)

  def sauvegarder_nouvelle_carte(self):
    nom_sujet = self.entry_sujet.get().strip()
    question = self.entry_question.get().strip()
    reponse = self.entry_reponse.get().strip()

    # Verification des champs obligatoires
    if not nom_sujet or not question or not reponse:
      messagebox.showwarning(
          "Champs vides", "Veuillez remplir tous les champs !"
      )
      return

    # Connexion directe pour gerer la liaison automatique sujet/carte
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()

    # Verification de l'existence du sujet pour recuperer son ID
    cursor.equation = cursor.execute(
        "SELECT id FROM sujets WHERE nom = ?", (nom_sujet,)
    )
    resultat = cursor.fetchone()

    if resultat:
      sujet_id = resultat[0]
    else:
      # Creation automatique du sujet s'il n'existe pas encore
      cursor.execute("INSERT INTO sujets (nom) VALUES (?)", (nom_sujet,))
      conn.commit()
      sujet_id = cursor.lastrowid

    # Insertion de la flashcard associee au sujet
    cursor.execute(
        "INSERT INTO flashcards (sujet_id, question, reponse) VALUES (?, ?, ?)",
        (sujet_id, question, reponse),
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Succes", "Flashcard enregistree avec succes !")

    # Vidage des champs question/reponse pour une saisie en chaine
    self.entry_question.delete(0, tk.END)
    self.entry_reponse.delete(0, tk.END)

  def open_subjects(self, subject_id, subject_name):
    # Recupere les cartes associees au sujet selectionne
    cards = recuperer_flashcards_par_sujet(subject_id)
    flashcards = recuperer_flashcards_par_sujet(subject_id)
    index_aleatoire = random.randrange(len(flashcards))
    question = flashcards[index_aleatoire]
    messagebox.showinfo(
        "Question :"
    )

    question = tk.Label(
      self.subject_page,
      text = f"Question : {question}"
    )

if __name__ == "__main__":
  app = Application()
  app.mainloop()