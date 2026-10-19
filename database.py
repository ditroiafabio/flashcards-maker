import sqlite3


def initialiser_bd():
  conn = sqlite3.connect("flashcards.db")
  cursor = conn.cursor()

  # Activer les clés étrangères (important pour SQLite)
  cursor.execute("PRAGMA foreign_keys = ON;")

  # Table des sujets
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS sujets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL
        )
    """)

  # Table des flashcards
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sujet_id INTEGER,
            question TEXT NOT NULL,
            reponse TEXT NOT NULL,
            FOREIGN KEY (sujet_id) REFERENCES sujets (id) ON DELETE CASCADE
        )
    """)

  conn.commit()
  conn.close()


def ajouter_sujet(nom_sujet):
  """Ajoute un nouveau sujet s'il n'existe pas encore."""
  conn = sqlite3.connect("flashcards.db")
  cursor = conn.cursor()
  try:
    cursor.execute("INSERT INTO sujets (nom) VALUES (?)", (nom_sujet,))
    conn.commit()
    succes = True
  except sqlite3.IntegrityError:
    succes = False  # Le sujet existe déjà
  conn.close()
  return succes


def recuperer_sujets():
  """Renvoie la liste de tous les sujets (ex: pour remplir un menu déroulant)."""
  conn = sqlite3.connect("flashcards.db")
  cursor = conn.cursor()
  cursor.execute("SELECT id, nom FROM sujets")
  sujets = cursor.fetchall()
  conn.close()
  return sujets  # Renvoie une liste de tuples : [(1, 'Maths'), (2, 'Python')]


def ajouter_flashcard(sujet_id, question, reponse):
  """Ajoute une question/réponse liée à un sujet spécifique."""
  conn = sqlite3.connect("flashcards.db")
  cursor = conn.cursor()
  cursor.execute(
      "INSERT INTO flashcards (sujet_id, question, reponse) VALUES (?, ?, ?)",
      (sujet_id, question, reponse),
  )
  conn.commit()
  conn.close()


def recuperer_flashcards_par_sujet(sujet_id):
  """Récupère toutes les questions/réponses d'un sujet donné (pour réviser)."""
  conn = sqlite3.connect("flashcards.db")
  cursor = conn.cursor()
  cursor.execute(
      "SELECT question, reponse FROM flashcards WHERE sujet_id = ?", (sujet_id,)
  )
  cartes = cursor.fetchall()
  conn.close()
  return cartes  # Renvoie [( 'Q1', 'R1' ), ( 'Q2', 'R2' )]