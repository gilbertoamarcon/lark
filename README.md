# Lark


Lark LALR(1) usage examples.


## Dependencies

```
sudo pip install lark-parser
```


## Usage


Domain Parsing:
```
python src/main.py -g grammar/domain.g -i data/domain.apl -o data/domain.yaml
```

Problem Parsing:
```
python src/main.py -g grammar/problem.g -y data/domain.yaml -i data/problem.apl -o data/problem.yaml
```

