# Project Name

This project is the frontEnd of the project that have as purpose to do a Deep Learning Approach for Norm Conflict Identification.
it's a two-phase approach that uses traditional machine learning together with deep learning to extract and compare norms in order to identify conflicts between them.

## Demo

## Dependencies
* We reccomend to install the dependencies with a virtual env from here 
* Django
* Python
* Mysql
* Mysql-python
* HomeBrew [Due to mysql-python needs]
* pypandoc [https://pypi.python.org/pypi/pypandoc]
* scikit-learn [http://scikit-learn.org/stable/install.html]
* numpy [http://www.numpy.org/]
* scipy [https://www.scipy.org/]
* nltk  [http://www.nltk.org/install.html]
* six [https://pypi.python.org/pypi/six]
* keras [https://keras.io]
  * theano
  * pyyaml [have to have six, numpy and scipy, and keras will download this theano ans pyyaml for you as well]
* upgrade tensorflow [https://www.tensorflow.org/install]
  * TensorFlow is the backend, upgrading it will download protobuf, pbr, funcsigs, mock, werkzeug and tensorflow 
  * If gives you this error: Resource u'tokenizers/punkt/english.pickle' not found.  Please
  use the NLTK Downloader to obtain the resource:  >>> nltk.download() 
    -->Do : sudo python -m nltk.downloader punkt 
    -->pip install h5py
   -->sudo pip install keras --upgrade
* pdfminer.six [will run setup.py bdist_wheel for pycrypto and built pdfminer.six and pycrypto

## API Reference

## Installation of dependencies
*We reccomend to run the project with a virtual env
### OS X & Linux:

```sh$
cd ~/project_directory
$ source env/bin/activate
```
```sh$
$ virtualenv env
```
```sh$
$ source env/bin/activate
```
```sh$
$ pip install django
```
```sh$
$ pip install mysql-python
```
```sh$
pip install pypandoc
```
```sh$
pip install -U scikit-learn
```
```sh$
sudo pip install numpy
```
```sh$
sudo pip install -U nltk 
```
```sh$
sudo pip install keras
```
```sh$
pip install --upgrade tensorflow 
```
```sh$
sudo python -m nltk.downloader punkt 
```
```sh$ 
pip install h5py
```
```sh$
sudo pip install keras --upgrade
```
```sh$
pip install pdfminer.six
```

### Windows:

```sh
cd
```

## Usage
```sh$
cd ~/project_directory/conconexp
```
```sh$
python manage.py runserver  
```
* All set! Go to localhost:8000 and its running locally!


### Possible errors thet you will have and how to fix them
### You will have to modify the values of 'USER' and 'PASSWORD' of 'DATABASES' dictonary 
 * In the archieve settings.py, who is at '/conconexp/conconexp' set the user and password of your localBase;
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
### Login/logout issues
* Two alterations have to bo done to not to have issues when redirect in login/logout due to differences between the root path of the website and the root local path of the website:
  * Login: go to 
 ```
 '/conconexp/conconexp/settings.py' 
 ```
 and change the variable LOGIN_REDIRECT_URL to just '/', removing the 'conconexp' of it;
   * Logout: go to
  ```
 '/conconexp/conconexp/urls.py' 
 ```
 and you have to modify the definition of url to logout. It's a 'url' function(in the thrid argument exist a dictionary with a 'next_page' ke. You have to modify the value of '/conconexp' to '/' as in the login.

### Load dump
* You have to download the last dump in your local database, so, enter in mysql:
   ```
 'mysql -u user_name -p'
 ```
   and, once inside mysql 
   ```
    '\. caminho/para/o/dump'
   ```
## License
