[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ekD6YLNP)

Please notice that we generated all "base"-files so we have a starting point to implement our project

## Docker Login für Github Container Registry
Es muss ein Personal Access Token (PAT) mit den entsprechenden Berechtigungen für dieses Repository erstellt werden, um sich bei der Github Container Registry (ghcr.io) anzumelden.

Sobald das PAT erstellt wurde, kann man sich mit dem folgenden Befehl bei der Registry anmelden:
```bash
echo {{GITHUB_PAT}} | docker login ghcr.io -u {{GITHUB_USERNAME}} --password-stdin
```

## Docker Container starten im Hintergrund

```bash
docker run -d -p 5000:5000 ghcr.io/fia-gso/osp-code-repository-gruppe-4-1:main
```
