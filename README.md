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

In this section we detail how to generate a Drupal instance with sample data as source system and an empty WordPress instance as target system to validate the migration functionality of the transformo framework. We first must clone the repository:
```
$ git clone https://github.com/diverso-lab/transformo
$ cd transformo
```

Now, we must deploy our Drupal and WordPress instances with Docker (one step at a time, in the order shown). First, we deploy our Drupal services:
```
$ make prepare_drupal
$ make install_drupal
```

The following commands will start our WordPress instances:
```
$ make prepare_wordpress
$ make install_wordpress
```

Thus, we have started a Drupal container populated with test data on port :8080 and a PHPMyAdmin instance on :8081, which will represent our source system. We have also started a configured and empty WordPress instance to represent our target, on port :8083 and its PHPMyAdmin on port :8084.

<div align="center">
  
|           | Web   | MySQL  | PHPMyAdmin | Credentials (Web /admin & PHPMyAdmin database access) |
|-----------|-------|--------|------------|-------------------------------------------------------|
| Drupal    | :8080 | :33061 | :8081      | user=drupal, password=drupal                          |
| WordPress | :8082 | :33062 | :8083      | user=wordpress, password=wordpress                    |
  
</div>
