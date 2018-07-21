# APL-MAPL


Parsers for the Actions Concurrency and Time Uncertainty Planner Language (APL) and the Multiagent Actions Concurrency and Time Uncertainty Planner Language (MAPL).



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



### MAPL

Mapl Domain Parsing:
```
python src/mapl-parse.py -g grammar/mapl-domain.g -i data/domain.mapl -o data/mapl-domain.yaml
```

Mapl Problem Parsing:
```
python src/mapl-parse.py -g grammar/mapl-problem.g -y data/mapl-domain.yaml -i data/problem.mapl -o data/mapl-problem.yaml
```

