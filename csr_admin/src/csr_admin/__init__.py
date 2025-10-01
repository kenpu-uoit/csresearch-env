from typer import Typer, Argument, Option, Exit
from . import list
from jinja2 import Environment, FileSystemLoader
import pathlib
import os

app = Typer()

@app.command(name="list")
def List():
    list.command()

@app.command(name="create")
def Create(
    hostname: str = Argument(..., help="hostname"),
    image:str = Option(..., "--image", help="image"),
    port:int = Option(..., "--ssh", '--port', help="port"),
    cpus:int = Option(32, "--cpus", help="CPU allocation"),
    memory:str = Option("16G", "--ram", help="Memory allocation"),
    data_path: str = Option("/data", '--data', help="Global data path"),
    postgres: bool = Option(False, "--postgres", "--pg", "--postgresql", help="Postgresql database")
):
    if '/' in hostname:
        project, hostname = hostname.split('/', 1)
    else:
        print("ERROR: hostname must be in the form of: <project>/<hostname>")
        raise Exit()
    
    path = os.path.join(data_path, project, hostname)
    os.makedirs(path, exist_ok=True)
    for dir in ["home", "postgres"]:
        os.makedirs(os.path.join(path, dir), exist_ok=True)

    params = dict(
        hostname = hostname,
        project = project,
        image = image,
        port = port,
        cpus = cpus,
        memory = memory,
        data_path = data_path,
        postgres = postgres,
    )

    here = pathlib.Path(__file__).resolve().parent
    env = Environment(loader=FileSystemLoader(here / "templates"))
    template = env.get_template("docker-compose.jinja2")
    with open(os.path.join(path, 'docker-compose.yml'), 'w') as f:
        print(template.render(params), file=f)
    
    template = env.get_template('Makefile')
    with open(os.path.join(path, 'Makefile'), 'w') as f:
        print(template.render(params), file=f)

    print(f"Creating {path}/users")
    template = env.get_template("users")
    with open(os.path.join(path, 'users'), 'w') as f:
        print(template.render(params), file=f)

@app.command(name="hello")
def hello():
    print("hello")

def main():
    app()