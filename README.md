![Hoshimori-Project](http://imgur.com/download/JMpH8Ew)

# **Hoshimori-Project**

**[The Battle Girl Highschool Database and Community](http://hoshimorigakuen.pythonanywhere.com/)**

## Get Started

### Requirements

  - Debian, Ubuntu, and variants

    ```shell
    apt-get install libpython-dev libffi-dev python-virtualenv libmysqlclient-dev nodejs
    ```

  - Arch

    ```shell
    pacman -S libffi python-virtualenv libmysqlclient nodejs
    ```
    
  - OS X (install brew if you don't have it):
  
    ```shell
    brew install python node
    sudo pip install virtualenv
    npm install lessc bower
    ```
    
### Quick guide

1. Clone the repo:

    ```shell
    git clone https://github.com/kokonguyen191/Hoshimori-Project.git
    cd Hoshimori-Project
    ```

2. Create a virtualenv to isolate the package dependencies locally:

    ```shell
    virtualenv env
    source env/bin/activate
    ```

3. Install packages:

    ```shell
    pip install --upgrade setuptools
    pip install -r requirements.txt
    ```

4. Get the front-end dependencies:

    ```shell
    npm install -g bower
    bower install
    ```
  
5. Initialize the models and databse:

    ```shell
    python manage.py makemigrations hoshimori
    python manage.py migrate
    python manage.py generate_settings
    ```

6. Launch the server:

    ```shell
    python manage.py runserver
    ```

7. Open your browser to [http://localhost:8000/](http://localhost:8000/) to see the website

### Getting database

You can either get them your own way by extracting game data or crawling from wikis. Or you can use my [crawler](https://github.com/kokonguyen191/Hoshimori-Scrapy) and then process the crawled data with my [database processor](https://github.com/kokonguyen191/Hoshimori-Database-Processor). After that you can just push them onto your server.

## Developers

* **[Koko191](https://github.com/kokonguyen191)** - Main dev
* **[duyson98](https://github.com/duyson98)** - Collaborator

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
