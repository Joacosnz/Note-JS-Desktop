#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrypoint main.py para Note JS
"""
import argparse
from backend import run_server, PORT

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Note JS Server')
    parser.add_argument('--port', type=int, default=PORT, help='Port to bind')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind')
    args, _ = parser.parse_known_args()
    run_server(port=args.port, host=args.host)
