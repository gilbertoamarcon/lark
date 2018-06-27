# Lark


Lark LALR(1) usage examples.


## Dependencies

```
sudo pip install lark-parser
```


## Usage

```
python src/domain.py -g grammar/domain.g -i data/dom.apl -o data/domain.yaml
```


```
python src/problem.py -g grammar/problem.g -y data/domain.yaml -i data/prob.apl -o data/problem.yaml
```

