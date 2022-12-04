#!/usr/bin/env python3

  # Example: <program> 5 4 8192
  # Cluster 5 includes sectors 8204-8207

import argparse

parser = argparse.ArgumentParser(description='Convert cluster to its corresponding sectors')
parser.add_argument('cluster_number', metavar='C', type=int,
                    help='Cluster that requires conversion')
parser.add_argument('sectors_per_cluster', metavar='S',
                    type=int, help='Number of sectors per cluster')
parser.add_argument('sector_address_of_sector_2', metavar='2', type=int,
                    help='Sector address of cluster 2')
args = parser.parse_args()

def main():
  start_sector: int = (args.cluster_number - 2) * args.sectors_per_cluster + args.sector_address_of_sector_2
  end_sector: int = start_sector + args.sectors_per_cluster - 1
  print(f'Cluster {args.cluster_number} includes sectors {start_sector}-{end_sector}')

if __name__ == "__main__":
  main()
