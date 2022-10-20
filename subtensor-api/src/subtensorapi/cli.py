# The MIT License (MIT)
# Copyright © 2022 Opentensor Foundation

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

import subprocess
from . import FastSync
from rich.console import Console
from typing import List, Optional
import sys
import argparse

console = Console()

def run_sync_and_save(filename: str, block_hash: str, endpoint_url: str) -> None:
    # check if fast sync is available
    FastSync.verify_fast_sync_support()
    # try to fast sync
    fast_sync: FastSync = FastSync(endpoint_url)
    # get neurons
    fast_sync.sync_and_save(console, block_hash, filename)

def run_get_blockAtRegistration_for_all_and_save(filename: str, block_hash: str, endpoint_url: str) -> None:
    # check if fast sync is available
    FastSync.verify_fast_sync_support()
    # try to fast sync
    fast_sync: FastSync = FastSync(endpoint_url)
    # get neurons
    fast_sync.get_blockAtRegistration_for_all_and_save(console, block_hash, filename)

def sync_neurons(filename: str, path_to_bin: str) -> None:
    """Runs the fast sync binary to sync all neurons at a given block hash"""
    
    print("Using subtensor-node-api for neuron retrieval...")
    # will write to ~/.bittensor/metagraph.json by default
    try:
        subprocess.run([path_to_bin, "sync_and_save", '-f', filename], check=True, stdout=subprocess.PIPE)
    except subprocess.SubprocessError as e:
        raise Exception("Error running fast sync binary: {}".format(e))

def sync_and_save(args: Optional[List[str]] = sys.argv[1:] ) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, default='~/.bittensor/metagraph.json', help='Filename to save metagraph to')
    parser.add_argument('-b', '--block_hash', type=str, default='latest', help='Block hash to sync neurons at')
    parser.add_argument('-u', '--endpoint_url', type=str, default='wss://AtreusLB-2c6154f73e6429a9.elb.us-east-2.amazonaws.com:9944', help='Endpoint url to connect to')

    parsed_args = parser.parse_args(args=args)

    run_sync_and_save(parsed_args.filename, parsed_args.block_hash, parsed_args.endpoint_url)

def blockAtRegistration_for_all_and_save(args: Optional[List[str]] = sys.argv[1:] ) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, default='~/.bittensor/.json', help='Filename to save metagraph to', required=False)
    parser.add_argument('-b', '--block_hash', type=str, default='latest', help='Block hash to sync neurons at', required=False)
    parser.add_argument('-u', '--endpoint_url', type=str, default='wss://AtreusLB-2c6154f73e6429a9.elb.us-east-2.amazonaws.com:9944', help='Endpoint url to connect to', required=False)

    parsed_args = parser.parse_args(args=args)

    run_get_blockAtRegistration_for_all_and_save(parsed_args.filename, parsed_args.block_hash, parsed_args.endpoint_url)