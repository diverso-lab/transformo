# transformo

Activate virtual environment

```
python -m venv venv
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

# Validation Environment (Drupal MySQL -> WordPress MySQL)

We first must download the repository:
```
git clone https://github.com/diverso-lab/transformo
cd transformo
```

Then, we will move to the mysql branch
```
git checkout mysql
cd dp-to-wp
```

Now, we must deploy our Drupal and WordPress instances with Docker:
```
make prepare_drupal
make install_drupal

make prepare_wordpress
make install_wordpress
```
