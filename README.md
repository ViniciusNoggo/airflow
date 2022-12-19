# Pre-commit

Antes de fazer algum *commit* no repositório, é necessário instalar o pacote `pre-commit` do python no ambiente virtual utilizado:

```
pip install pre-commit
```

Em seguida, deve-se instalar os *hooks* do pre-commit, através do seguinte comando:

```
pre-commit install
```

A partir desse momento, todos os pre-commits serão executados antes de um *commit* automaticamente. O *commit* não será feito, caso alguma verificação falhe; ao falhar, os *hooks* farão boa parte das modificações para fazer com que o código siga alguns `guidelines` estéticos (definidos em [.pre-commit-config.yaml](.pre-commit-config.yaml)). Em seguida, basta executar o *commit* novamente e verificar se todos os testes irão passar.

Também é possível executar os *hooks* antes do *commit* usando o seguinte comando:

```
pre-commit run --all-files
```
