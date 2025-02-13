# Lan Audacity

## Functions

### `simple_click_on_treeview`

Lorsque je sélectionne un objet d'un treeview:

- Si le model du treeview est QFileSystemModel:
  - je garde en mémoire le chemin absolu
- Si le model du treeview est QStandardItemModel:
  - je garde en mémoire le ou les parents de l'objet
- Sinon afficher un message d'erreur

### `double_click_on_treeview`

Lorsque je double click sur un objet d'un treeview:

- Si le model du treeview est QFileSystemModel:
  - si c'est un dossier:
    - si il est ouvert je le réduit
    - sinon je l'étends
  - si c'est un fichier:
    - si il est ouvert dans un onglet:
      - si il n'est pas affiché je l'affiche
    - sinon je l'ouvre dans un onglet
  - je garde en mémoire le chemin absolu
- Si le model du treeview est QStandardItemModel:
  - je garde en mémoire le ou les parents de l'objet
- Sinon afficher un message d'erreur

### `create_file`

Lorsque je click sur le btn et j'active `create_file`

- je récupère le dernier chemin absolu enregistré
- sinon je prends le chemin racine du treeview avec QFileSystemModel
Ensuite je demande le nom du fichier puis quand je récupère la touche entrée du clavier je créer le fichier.

### `create_folder`

Lorsque je click sur le btn et j'active `create_folder`

- je récupère le dernier chemin absolu enregistré
- sinon je prends le chemin racine du treeview avec QFileSystemModel
Ensuite je demande le nom du dossier puis quand je récupère la touche entrée du clavier je créer le dossier.

### `open_tab`

Récupère le signal de `double_click_on_treeview` avec comme données

```bash
type: str
title_tab: str
data: any
option: any
```

si c'est un type `default`:

- ouvrir un onglet avec comme message `404: Error Default Page, reopen the tab object`

si c'est un type `file`:

- ouvrir un onglet avec un editeur de text en mode `Read only`

si c'est un type `lan`:

- ouvrir un onglet avec un affichage objet (au stack `Dashboard`)

si c'est un type `uc`:

- ouvrir un onglet avec un affichage objet (au stack `Dashboard`)

si c'est un type `dlc`:

- ouvrir un onglet avec un affichage objet

### `create_lan`

Lorsque je click sur le btn et j'active `create_lan`

- je récupère le dernier chemin objet enregistré
- sinon je prends le chemin racine du treeview avec QStandardItemModel
Ensuite j'ouvre un formulaire `new lan` et j'attends la validation.

### `create_uc`

Lorsque je click sur le btn et j'active `create_uc`

- je récupère le dernier chemin objet enregistré
- sinon je prends le chemin racine du treeview avec QStandardItemModel
Ensuite j'ouvre un formulaire `new uc` et j'attends la validation.
