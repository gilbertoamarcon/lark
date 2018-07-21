# Lark


Lark LALR(1) usage examples.


## Dependencies

```
sudo pip install lark-parser
```


## Usage

### APL

Apl Domain Parsing:
```
python src/apl-parse.py -g grammar/apl-domain.g -i data/domain.apl -o data/apl-domain.yaml
```

Apl Problem Parsing:
```
python src/apl-parse.py -g grammar/apl-problem.g -y data/apl-domain.yaml -i data/problem.apl -o data/apl-problem.yaml
```

