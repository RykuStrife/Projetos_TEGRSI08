#!/usr/bin/env python3
"""
SYMS - Detecção de Semelhanças entre Ficheiros
Data: /07/2025
Autores: [Ricardo Morgado], [Miguel Silva]
"""

import argparse
import os
import hashlib
import re
from collections import defaultdict

def parse_args():
    """Analisa os argumentos da linha de comandos"""
    parser = argparse.ArgumentParser(description='Detecta ficheiros semelhantes')
    parser.add_argument('path', nargs='?', default='.', help='Directoria a analisar')
    parser.add_argument('-c', '--contents', action='store_true', help='Comparar conteúdo')
    parser.add_argument('-n', '--name', action='store_true', help='Comparar nomes')
    parser.add_argument('-e', '--extension', action='store_true', help='Comparar extensões')
    parser.add_argument('-r', '--regex', help='Padrão regex para nomes')
    return parser.parse_args()

def get_file_hash(filepath):
    """Calcula o hash MD5 de um ficheiro"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_similar_files(path, options):
    """Encontra ficheiros semelhantes conforme as opções"""
    groups = defaultdict(list)
    
    for root, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            if options.contents:
                file_hash = get_file_hash(filepath)
                groups[f'content:{file_hash}'].append(filepath)
                
            if options.name:
                groups[f'name:{filename}'].append(filepath)
                
            if options.extension:
                ext = os.path.splitext(filename)[1]
                groups[f'ext:{ext}'].append(filepath)
                
            if options.regex:
                match = re.search(options.regex, filename)
                if match:
                    groups[f'regex:{match.group()}'].append(filepath)
    
    # Se nenhuma opção foi especificada, assume --name
    if not any([options.contents, options.name, options.extension, options.regex]):
        for root, _, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(root, filename)
                groups[f'name:{filename}'].append(filepath)
    
    return groups

def print_results(groups):
    """Imprime os grupos de ficheiros semelhantes"""
    for key, files in groups.items():
        if len(files) > 1:
            print(f"\nFicheiros com {key.split(':')[0]} igual ({key.split(':')[1]}):")
            for file in files:
                print(f"  - {file}")

def main():
    args = parse_args()
    groups = find_similar_files(args.path, args)
    print_results(groups)

if __name__ == '__main__':
    main()