# CS Research Environment

## Docker

The docker image serves as a standard base image for machine learning oriented research.

### Basic operating system

- Base image is `nvidia/cuda:12.2.2-devel-ubuntu22.04`
- curl, git, less, ack, ssh (client and server), tmux, wget, ffmpeg
- openjdk-21, postgresql-client-14

### Editor and publishing
- vim
- The whole _textlive_ installation (large and time consuming)
- Quarto 1.5.40 with tinutex and chrome PDF renderer

### Python libraries

- miniconda py312-24
- data science stack including (scipy, numpy, matplotlib, pandas, etc)
- psycopg2

### Machine learning

- Pytorch 2.3.0, lightning 2.2.5
- Huggingface transformer 4.41.2, accelerate, bitsandbytes, datasets, evaluate, peft, trl, tensorboard, wandb, xformers
- flash-attn
- sentencepiece, tiktoken, rouge-score, pymupdf, colbert-ai, etc.
- faiss-gpu 1.7.4

### AI

- ollama
- openai
- llama-index
- langchain

## Customization

- `/etc/user.default` specify the user entries: three columns for 
  - `id, username, password`
  - all users have passwordless sudo priviledge
- `/bin/start.sh` starts SSH port