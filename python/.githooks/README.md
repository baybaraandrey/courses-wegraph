# Git Hooks

## Installation Git >= 2.9
```sh
git config core.hooksPath .githooks
```

## Git < 2.9
```sh
mv .git/hooks .git/hooks.bak
ln -sf ../.githooks .git/hooks
```
