#!/usr/bin/env python3

# Example <program> 8204 8192 4
# Sector 8204 is in cluster 5

import sys
import math
import argparse

parser = argparse.ArgumentParser(description='Convert sector to its corresponding cluster')
parser.add_argument('sector', metavar='S', type=int,
                    help='Sector that requires conversion')
parser.add_argument('sector_of_cluster_2', metavar='2',
                    type=int, help='Sector address of the second cluster')
parser.add_argument('sectors_per_cluster', metavar='N', type=int,
                    help='Number of sectors per cluster')
args = parser.parse_args()

def main():
  if args.sector < args.sector_of_cluster_2:
    print('cluster cannot be smaller than sector of cluster 2')
    sys.exit(1)

  cluster_address: int = math.floor((args.sector - args.sector_of_cluster_2) / args.sectors_per_cluster + 2)
  print(f'Sector {args.sector} is in cluster {cluster_address}')

if __name__ == "__main__":
  main()
