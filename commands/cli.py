import subprocess
from pathlib import Path

import rich_click as click

# constants
ROOT = Path(__file__).parent.parent
WORDPRESS_ROOT = ROOT / "wordpress.docker"
WORDPRESS_URL = "http://localhost:8888"
WORDPRESS_API = "wp-json/wp/v2"
DC = "docker-compose"


@click.group()
def wp():
    """
    CLI for setting up a wordpress container that manages:

    - the wordpress installation

    - the plugins

    - the demo data

    """


@click.group()
def wt():
    """
    CLI for the wagtail site that manages:

    - migrations

    - superuser creation

    - running the server

    - fixing the tree command
    """


@click.group()
def dj():
    """
    CLI for the django admin site that manages:

    - importing data from wordpress

    - importing authors

    - importing categories

    - importing tags

    - importing pages

    - importing posts

    - importing media

    - importing comments

    - importing all data
    """


"""WORDPRESS COMMANDS"""


@wp.command()
def build():
    """Wordpress: initial setup"""

    # copy the .env.example file to .env if not exists
    env_file = WORDPRESS_ROOT / ".env"
    if not env_file.exists():
        with open(WORDPRESS_ROOT / ".env.example") as f:
            env_content = f.read()
            with open(WORDPRESS_ROOT / ".env", "w") as f2:
                f2.write(env_content)

    # create directory for plugins
    plugins_dir = WORDPRESS_ROOT / "wp-content/plugins"
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
    """Wordpress: start the container"""
    subprocess.run([DC, "up", "-d"], cwd=WORDPRESS_ROOT)


@wp.command()
def stop():
    """Wordpress: stop the container"""
    subprocess.run([DC, "down"], cwd=WORDPRESS_ROOT)


@wp.command()
def destroy():
    """Wordpress: destroy the container"""
    subprocess.run([DC, "down", "--volumes"], cwd=WORDPRESS_ROOT)

    cleanup = click.prompt("Do you want to clean up the files? (y/n)", type=str)

    if cleanup == "y":
        env_file = WORDPRESS_ROOT / ".env"
        if env_file.exists():
            env_file.unlink()

        wp_content = WORDPRESS_ROOT / "wp-content"
        if wp_content.exists():
            subprocess.run(["rm", "-rf", WORDPRESS_ROOT / "wp-content"])

        wp_xml = WORDPRESS_ROOT / "xml"
        if wp_xml.exists():
            subprocess.run(["rm", "-rf", WORDPRESS_ROOT / "xml"])


@wp.command()
def load():
    """Wordpress: import the demo data"""
    # if docker-compose is not running, start it
    running = subprocess.run(
        [DC, "ps"], cwd=WORDPRESS_ROOT, capture_output=True
    ).stdout.decode("utf-8")
    if "wordpress" not in running:
        subprocess.call(["wp", "up"])

    # import the demo data
    subprocess.run([DC, "exec", "-T", "wordpress", "bin/init.sh"], cwd=WORDPRESS_ROOT)


"""WAGTAIL COMMANDS"""


@wt.command()
def migrate():
    """Wagtail: run migrations"""
    subprocess.run(["python", "manage.py", "migrate"], cwd=ROOT)


@wt.command()
def superuser():
    """Wagtail: create superuser"""
    subprocess.run(["python", "manage.py", "createsuperuser"], cwd=ROOT)


@wt.command()
def run():
    """Wagtail: run the server"""
    subprocess.run(["python", "manage.py", "runserver"], cwd=ROOT)


@wt.command()
def fixtree():
    """Wagtail: fix the tree"""
    subprocess.run(["python", "manage.py", "fixtree"], cwd=ROOT)


"""DJANGO COMMANDS"""


@dj.command()
def authors():
    """Django: import authors from wordpress"""
    subprocess.run(
        [
            "python",
            "manage.py",
            "import",
            f"{WORDPRESS_URL}/{WORDPRESS_API}/users",
            "WPAuthor",
        ],
        cwd=ROOT,
    )


@dj.command()
def categories():
    """Django: import categories from wordpress"""
    subprocess.run(
        [
            "python",
            "manage.py",
            "import",
            f"{WORDPRESS_URL}/{WORDPRESS_API}/categories",
            "WPCategory",
        ],
        cwd=ROOT,
    )


@dj.command()
def tags():
    """Django: import tags from wordpress"""
    subprocess.run(
        [
            "python",
            "manage.py",
            "import",
            f"{WORDPRESS_URL}/{WORDPRESS_API}/tags",
            "WPTag",
        ],
        cwd=ROOT,
    )


@dj.command()
def pages():
    """Django: import pages from wordpress"""
    subprocess.run(
        [
            "python",
            "manage.py",
            "import",
            f"{WORDPRESS_URL}/{WORDPRESS_API}/pages",
            "WPPage",
        ],
        cwd=ROOT,
    )


@dj.command()
def posts():
    """Django: import posts from wordpress"""
    subprocess.run(
        [
            "python",
            "manage.py",
            "import",
            f"{WORDPRESS_URL}/{WORDPRESS_API}/posts",
            "WPPost",
        ],
        cwd=ROOT,
    )


@dj.command()
def media():
    """Django: import media from wordpress"""
    subprocess.run(
        [
            "python",
            "manage.py",
            "import",
            f"{WORDPRESS_URL}/{WORDPRESS_API}/media",
            "WPMedia",
        ],
        cwd=ROOT,
    )


@dj.command()
def comments():
    """Django: import comments from wordpress"""
    subprocess.run(
        [
            "python",
            "manage.py",
            "import",
            f"{WORDPRESS_URL}/{WORDPRESS_API}/comments",
            "WPComment",
        ],
        cwd=ROOT,
    )


@dj.command()
def all():
    """Django: import all data from wordpress"""
    subprocess.call(["dj", "authors"])
    subprocess.call(["dj", "categories"])
    subprocess.call(["dj", "tags"])
    subprocess.call(["dj", "pages"])
    subprocess.call(["dj", "posts"])
    subprocess.call(["dj", "media"])
    subprocess.call(["dj", "comments"])
