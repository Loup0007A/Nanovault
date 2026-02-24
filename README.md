# 🛡️ NanoVault

[![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security: Pure Python](https://img.shields.io/badge/Security-Pure%20Python-green.svg)](#)

**NanoVault** est un outil de stéganographie binaire conçu pour dissimuler des messages chiffrés à l'intérieur d'images PNG. Basé sur les dernières fonctionnalités de **Python 3.14**, il se distingue par sa philosophie **"Zero-Dependency"** : tout le code repose exclusivement sur la bibliothèque standard.



---

## ✨ Points Forts

- 🔒 **Chiffrement Robuste :** Utilise `PBKDF2-HMAC-SHA256` avec $100\,000$ itérations pour transformer votre mot de passe en clé sécurisée.
- 🧊 **Zéro Dépendance :** Aucun `pip install` requis pour le cœur du logiciel. Uniquement `hashlib`, `secrets`, et `argparse`.
- 👻 **Totalement Invisible :** Les données sont injectées après le chunk `IEND`. L'image reste parfaitement lisible par toutes les visionneuses.
- 🛡️ **Protection par Sel (Salt) :** Chaque fichier possède son propre sel de 16 octets généré de manière cryptographique via `secrets.token_bytes()`.

---

## 🚀 Installation

Pour installer NanoVault et l'utiliser comme une commande globale :

1. **Cloner le dépôt :**
   '''bash
   git clone [https://github.com/votre-pseudo/NanoVault.git](https://github.com/Loup007A/Nanovault.git)
   cd NanoVault
   '''
2. **Installer le package :**
    '''bash
    pip install .
    '''

---

## 🛠️ Utilisation (CLI)

Une fois installé, utilisez la commande nanovault directement :

**📥 Cacher un secret**
    '''bash
    nanovault hide "image.png" "Message secret" "output.png" --password "MonPass"
    '''

**📤 Extraire un secret**
    '''bash
    nanovault extract "output.png" --password "MonPass"
    '''

---

## 🧠 Fonctionnement Technique

NanoVault manipule directement les octets du fichier PNG :

1. **Dérivation de Clé**
    Nous utilisons la fonction de dérivation de clé pour ralentir les attaques par force brute :
    $$Key = PBKDF2(HMAC, Password, Salt, 100\,000, SHA256)$$

2. **Injection Binaire**
    Le script scanne le fichier pour trouver le marqueur de fin officiel du PNG : \x49\x45\x4e\x44\xae\x42\x60\x82.
    Le payload est construit comme suit :
    [IMAGE_ORIGINALE] + [START_SECRET] + [SALT] + [SALT_TAG] + [ENCRYPTED_DATA] + [END_SECRET]

---

## 📦 Intégration API

Vous pouvez importer NanoVault dans vos projets :

    '''python
    from nanovault import hide_data, extract_file

    # Cacher
    hide_data("photo.png", "Secret", "resultat.png", "password")

    # Extraire
    msg = extract_file("password", "resultat.png")
    print(msg)
    '''

---

## 📜 Licence

Distribué sous la licence MIT. Voir le fichier LICENSE pour plus de détails.

---


Développé avec passion pour la cybersécurité en Pure Python.


