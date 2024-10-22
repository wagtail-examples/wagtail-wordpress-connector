import subprocess
from pathlib import Path

import click


@click.group()
def wp():
    """CLI for wordpress"""


@wp.command()
def build():
    """Wordpress initial setup"""

    # copy the .env.example file to .env if not exists
    env_file = Path("./wordpress.docker/.env")
    if not env_file.exists():
        with open("./wordpress.docker/.env.example") as f:
            env_content = f.read()
            with open("./wordpress.docker/.env", "w") as f2:
                f2.write(env_content)

    # create directory for plugins
    plugins_dir = Path("./wordpress.docker/wp-content/plugins")
    if not plugins_dir.exists():
        plugins_dir.mkdir(parents=True)

    # clone the plugins into the plugins directory, match with the plugins in init.sh
    plugins = [
        "https://github.com/valu-digital/wp-graphql-offset-pagination.git",
    ]

    for plugin in plugins:
        if not Path(plugins_dir / Path(plugin).stem).exists():
            subprocess.run(["git", "clone", plugin], cwd=plugins_dir)
        else:
            print(f"Plugin {plugin} already exists")


@wp.command()
def up():
    """Wordpress start the container"""
    subprocess.run(["docker-compose", "up", "-d"], cwd="./wordpress.docker")


@wp.command()
def down():
    """Wordpress stop the container"""
    subprocess.run(["docker-compose", "down"], cwd="./wordpress.docker")


@wp.command()
def destroy():
    """Wordpress destroy the container"""
    subprocess.run(["docker-compose", "down", "--volumes"], cwd="./wordpress.docker")

    cleanup = click.prompt("Do you want to clean up the files? (y/n)", type=str)

    if cleanup == "y":
        env_file = Path("./wordpress.docker/.env")
        if env_file.exists():
            env_file.unlink()

        wp_content = Path("./wordpress.docker/wp-content")
        if wp_content.exists():
            subprocess.run(["rm", "-rf", "./wordpress.docker/wp-content"])

        wp_xml = Path("./wordpress.docker/xml")
        if wp_xml.exists():
            subprocess.run(["rm", "-rf", "./wordpress.docker/xml"])


@wp.command()
def load():
    """Wordpress import the demo data"""
    # if docker-compose is not running, start it
    running = subprocess.run(
        ["docker-compose", "ps"], cwd="./wordpress.docker", capture_output=True
    ).stdout.decode("utf-8")
    if "wordpress" not in running:
        click.echo("Please start the container first: 'poetry run cli up'")
        return

    # import the demo data
    subprocess.run(
        ["docker-compose", "exec", "-T", "wordpress", "bin/init.sh"],
        cwd="./wordpress.docker",
    )
