#!/bin/bash 
#SBATCH -p csci # partition (queue) 
#SBATCH --gres=gpu:1 # number of GPUs
#SBATCH -N 1 # (leave at 1 unless using multi-node specific code) 
#SBATCH -n 1 # number of cores 
#SBATCH --mem=0 # memory per core (was 8192)
#SBATCH --job-name="georgeM" # job name 
#SBATCH -o slurm.%N.%j.stdout.txt # STDOUT 
#SBATCH -e slurm.%N.%j.stderr.txt # STDERR 
#SBATCH --mail-user=username@bucknell.edu # address to email 
#SBATCH --mail-type=ALL # mail events (NONE, BEGIN, END, FAIL, ALL) 
module load python
python $HOME/Model/server_text_gen_word_based.py
