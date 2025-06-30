#!/usr/bin/env python3
"""
PyCracker - Password Cracker para Linux
Data: /07/2025
Autores: [Ricardo Morgado], [Miguel Silva]
"""
import argparse
from passlib.hash import sha512_crypt, sha256_crypt
import sys
import os

def parse_shadow_line(line):
    """Analisa uma linha do ficheiro /etc/shadow"""
    if not line or line.startswith('#'):
        return None
    
    parts = line.split(':')
    if len(parts) < 2:
        return None
    
    username = parts[0]
    password_hash = parts[1]
    
    # Verifica se a conta está bloqueada ou inativa
    if password_hash.startswith(('!', '*')):
        return (username, None, "conta bloqueada/inativa")
    
    # Verifica se a conta não tem password
    if password_hash == '':
        return (username, None, "sem palavra-passe")
    
    # Extrai o algoritmo de hash e o salt
    if password_hash.startswith('$6$'):
        algorithm = 'sha512'
    elif password_hash.startswith('$5$'):
        algorithm = 'sha256'
    else:
        algorithm = 'des'  # Não suportado neste exemplo
    
    return (username, password_hash, algorithm)

def crack_password(hash_info, dictionary, verbose=False):
    """Tenta descobrir a password a partir do hash"""
    username, password_hash, algorithm = hash_info
    
    if not password_hash:
        if verbose:
            print(f"[+] A tentar utilizador '{username}' ...")
            print(f"[-] ... ignorado. {algorithm}.")
        return None
    
    if verbose:
        print(f"[+] A tentar utilizador '{username}' ...")
    
    with open(dictionary, 'r', errors='ignore') as f:
        for word in f:
            word = word.strip()
            if not word:
                continue
            
            if algorithm == 'sha512' and sha512_crypt.verify(word, password_hash):
                if verbose:
                    print(f"[-] ... PALAVRA-PASSE DESCOBERTA ===> '{word}'")
                return (username, word, 'SHA-512')
            
            elif algorithm == 'sha256' and sha256_crypt.verify(word, password_hash):
                if verbose:
                    print(f"[-] ... PALAVRA-PASSE DESCOBERTA ===> '{word}'")
                return (username, word, 'SHA-256')
    
    if verbose:
        print(f"[-] ... não foi possível determinar a palavra-passe")
    return None

def main():
    parser = argparse.ArgumentParser(description='Password Cracker para Linux')
    parser.add_argument('dictionary', help='Ficheiro do dicionário de passwords')
    parser.add_argument('passwords', nargs='?', default='/etc/shadow', 
                       help='Ficheiro de passwords (padrão: /etc/shadow)')
    parser.add_argument('-u', '--user', help='Tentar apenas este utilizador')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Modo verboso')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.dictionary):
        print(f"Erro: Ficheiro do dicionário '{args.dictionary}' não encontrado.", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(args.passwords):
        print(f"Erro: Ficheiro de passwords '{args.passwords}' não encontrado.", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(args.passwords, 'r') as f:
            shadow_lines = f.readlines()
    except PermissionError:
        print(f"Erro: Sem permissões para ler '{args.passwords}'. Execute como root.", file=sys.stderr)
        sys.exit(1)
    
    found = []
    for line in shadow_lines:
        hash_info = parse_shadow_line(line.strip())
        if not hash_info:
            continue
        
        username = hash_info[0]
        if args.user and username != args.user:
            continue
        
        result = crack_password(hash_info, args.dictionary, args.verbose)
        if result:
            found.append(result)
    
    if found:
        print("\nForam encontradas as palavras-passe dos seguintes utilizadores:")
        for user, password, algorithm in found:
            print(f"[+] {user} : '{password}'    ({algorithm})")
    else:
        print("[-] Não foram encontradas quaisquer palavras-passe")

if __name__ == '__main__':
    main()