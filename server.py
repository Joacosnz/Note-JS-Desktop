#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrypoint server.py para Note JS
Permite ejecución directa mediante python3 server.py y detección estándar por el supervisor
"""
import argparse
from backend import run_server, PORT

def main():
    parser = argparse.ArgumentParser(description='Note JS Server')
    parser.add_argument('--port', type=int, default=PORT, help='Port to bind')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Loopback host (local app only)')
    args, _ = parser.parse_known_args()
    run_server(port=args.port, host=args.host)


if __name__ == '__main__':
    main()
