# Project Name

This is the frontEnd of the project whose purpose is to identify norm conflicts using deep learning.
At the moment we use a two-phase approach that uses traditional machine learning together with deep learning to extract and compare norms in order to identify conflicts between them.

## Demo
http://lsa.pucrs.br/conconexp
## Dependencies
Below we list the dependencies, which we recommend to be installed within a virtual env
* [Django](https://www.djangoproject.com/download/)
* [Python] 2.7.3 ou 2.7.6 (https://www.python.org/downloads/)
* [Mysql](https://www.mysql.com/downloads/)
* [pypandoc](https://pypi.python.org/pypi/pypandoc)
* [scikit-learn](http://scikit-learn.org/stable/install.html)
* [numpy](http://www.numpy.org/)
* [scipy](https://www.scipy.org/)
* [nltk](http://www.nltk.org/install.html)
* [six](https://pypi.python.org/pypi/six)
* [keras](https://keras.io)
  * theano
  * pyyaml [have to have six, numpy and scipy, and keras will download this theano ans pyyaml for you as well]
* [upgrade tensorflow](https://www.tensorflow.org/install)
  * TensorFlow is the backend, upgrading it will download protobuf, pbr, funcsigs, mock, werkzeug and tensorflow 
  * If you get the following error ```Resource u'tokenizers/punkt/english.pickle' not found.```  Please
  use the NLTK Downloader to obtain the missing resource  ```nltk.download() ```
    * -->Do : sudo python -m nltk.downloader punkt    
    * -->pip install h5py    
    * -->sudo pip install keras --upgrade    
* pdfminer.six [will run setup.py bdist_wheel for pycrypto and built pdfminer.six and pycrypto]
* [HomeBrew](https://brew.sh/index_pt-br.html) -->If in MacOs

## Installation of dependencies 
* We reccomend to run the project with a virtual env
### OS X & Linux:

```sh$
cd ~/project_directory && virtualenv env && source env/bin/activate && pip install django && pip install mysql-python && pip install pypandoc && pip install -U scikit-learn && sudo pip install numpy && sudo pip install -U nltk  &&sudo pip install keras && pip install --upgrade tensorflow  && sudo python -m nltk.downloader punkt  &&pip install h5py && sudo pip install keras --upgrade && pip install pdfminer.six
```

### Windows:

Why would anyone use Windows?
```sh

```

## Usage
```sh$
$ cd ~/project_directory/conconexp
```
```sh$
$ python manage.py runserver  
```
* All set! Go to localhost:8000 and Django should be running locally!


## Possible issues that you will have and how to fix them
#### You will have to modify the values of 'USER' and 'PASSWORD' of 'DATABASES' dictonary 
------
 * In the archive *settings.py*, who is at _'/conconexp/conconexp'_ set the user and password to your localBase;
    * For example, you can change to:
         ```
         DATABASES = {
             'default': {
                 'ENGINE': 'django.db.backends.mysql',
                 'NAME': 'concon',
                 'USER': 'root',
                 'PASSWORD': '',
                 'HOST': 'localhost',
                 'PORT': '',
             }
         }
         ```
#### Login/logout issues
------
* Two alterations have to be done to not to have issues when redirect in login/logout due to differences between the root path of the website and the root local path of the website:
   * *Login*: go to 
 ```
 '/conconexp/conconexp/settings.py' 
 ```
 and change the variable _LOGIN_REDIRECT_URL_ to just '/', removing the 'conconexp' of it;
  
  * *Logout*: go to
  ```
 '/conconexp/conconexp/urls.py' 
 ```
 and you have to modify the definition of url to logout. It's a 'url' function(in the third argument exist a dictionary with a 'next_page' ke. You have to modify the value of _'/conconexp'_ to '/' as in the login.

#### Load dump
------
* You have to download the last dump in your local database, so, enter in mysql:
 ```
 'mysql -u root -p' 
 ```
  and, once inside mysql;
  ```
 '\. path_to/dump'
 ```
## License
Design of the page is free for personal and commercial use under the CCA 3.0 license [HTML5 UP](https://html5up.net/license)
