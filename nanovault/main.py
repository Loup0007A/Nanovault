import secrets
import hashlib
    
import argparse
import sys


def encode(text,password):
    salt = secrets.token_bytes(16)

    key = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode(), 
        salt, 
        100000  # Nombre d'itérations
    )

    plain_bytes = text.encode()
    encrypted_bytes = bytes([b ^ key[i % len(key)] for i, b in enumerate(plain_bytes)])
    
    # 4. On stocke le SEL + les DONNÉES CHIFFRÉES
    # Le sel n'est pas secret, il doit être lu pour recréer la clé
    return salt + b"SALT" + encrypted_bytes

def hide_data(png_path: str, secret_data: str, output_path: str,password: str):
    # Le marqueur standard de fin de fichier PNG
    PNG_END = b"\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    
    with open(png_path, 'rb') as f:
        content = f.read()

    # On vérifie si le fichier est bien un PNG
    if not content.startswith(b'\x89PNG'):
        raise ValueError("Le fichier n'est pas un PNG valide.")

    # On cherche la position du marqueur de fin
    end_pos = content.find(PNG_END)
    if end_pos == -1:
        raise ValueError("Marqueur IEND introuvable.")

    # On découpe l'image jusqu'à la fin officielle
    image_part = content[:end_pos + len(PNG_END)]
    
    # On assemble : Image officielle + Données secrètes
    # Astuce : On peut ajouter un petit "tag" pour retrouver nos données facilement
    final_content = image_part + b"START_SECRET" + encode(secret_data, password) + b"END_SECRET"

    with open(output_path, 'wb') as f:
        f.write(final_content)
    
    print(f"Données cachées avec succès dans {output_path}")

import hashlib

def decrypt_data(encrypted_payload,salt, password):
    
    # 2. On régénère la clé exactement comme à l'aller
    # On utilise le même sel et le même nombre d'itérations
    key = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode(), 
        salt, 
        100000
    )
    
    # 3. On applique le XOR inverse (XOR est réversible)
    # On itère sur les données chiffrées avec la clé régénérée
    decrypted_bytes = bytes([
        b ^ key[i % len(key)] for i, b in enumerate(encrypted_payload)
    ])
    
    return decrypted_bytes.decode('utf-8')

def extract_file(password: str, path: str) :
    with open(path, 'rb') as f:
        content = f.read()

    # On cherche les balises personnalisées
    try:
        start = content.index(b"START_SECRET") + len(b"START_SECRET")
        end = content.index(b"END_SECRET")
        salt_mark = content.index(b"SALT")
        salt = content[start:salt_mark]
        saltt = content.index(b"SALT") + len(b"SALT")
        secret_crypt = content[saltt:end]
        secret = decrypt_data(secret_crypt,salt, password)
        return secret
    except ValueError:
        return "Aucune donnée cachée trouvée ou mot de passe incorrect."

def main():
    parser = argparse.ArgumentParser(description="NanoVault - Stéganographie PNG chiffrée")
    subparsers = parser.add_subparsers(dest="command")

    # Commande hide
    hide_parser = subparsers.add_parser('hide', help='Cacher un message')
    hide_parser.add_argument('image', help='Image PNG source')
    hide_parser.add_argument('message', help='Message à cacher')
    hide_parser.add_argument('output', help='Image de sortie')
    hide_parser.add_argument('--password', '-p', required=True, help='Mot de passe')

    # Commande extract
    extract_parser = subparsers.add_parser('extract', help='Extraire un message')
    extract_parser.add_argument('image', help='Image PNG contenant le secret')
    extract_parser.add_argument('--password', '-p', required=True, help='Mot de passe')

    args = parser.parse_args()

    if args.command == 'hide':
        hide_data(args.image, args.message, args.output, args.password)
    elif args.command == 'extract':
        result = extract_file(args.password, args.image)
        print(f"Secret : {result}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()