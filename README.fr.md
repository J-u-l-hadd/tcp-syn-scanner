*Lire dans d'autres langues : [English](README.md)*

# Scanner de Ports TCP SYN Personnalisé 🔍

Un scanner de ports TCP SYN (Furtif) léger et ultra-rapide, développé en Python avec Scapy.

Contrairement aux scanners standards qui effectuent une connexion complète, cet outil forge des paquets IP et TCP bruts pour initier une connexion semi-ouverte (scan SYN). Cela permet d'identifier rapidement les ports Ouverts, Fermés et Filtrés (bloqués par un pare-feu) sans terminer la triple poignée de main TCP (three-way handshake). Il génère automatiquement des rapports textuels horodatés pour chaque scan dans le répertoire courant.

## 🚀 Fonctionnalités
*   **Scan Furtif :** Utilise des paquets SYN bruts pour éviter les connexions TCP complètes.
*   **Catégorisation Intelligente :** Fait la différence entre les ports fermés (RST) et les ports filtrés/pare-feu (rejets ICMP/délais d'attente).
*   **Rapports Dynamiques :** Sauvegarde automatique des résultats avec des noms de fichiers horodatés (ex: `scan_127.0.0.1_all_20261025_214356.txt`).
*   **Binaires Autonomes :** Précompilé pour Windows (`.exe`) et Linux Debian/Ubuntu (aucune installation Python requise).

## ⚙️ Prérequis & Installation

Cet outil injectant des paquets bruts directement sur la carte réseau, il nécessite des privilèges d'exploitation de bas niveau.

### 🪟 Utilisateurs Windows
1. Téléchargez `port_scanner.exe` depuis la page Releases.
2. **Installer Npcap :** Vous devez installer [Npcap](https://npcap.com/). Lors de l'installation, **vous devez impérativement cocher la case "Support loopback traffic"**, sinon le scanner plantera lors des tests locaux.
3. **Exécuter en tant qu'Administrateur :** Ouvrez l'Invite de commandes ou PowerShell en tant qu'administrateur pour exécuter le scanner.

### 🐧 Utilisateurs Linux (Debian/Ubuntu)
1. Téléchargez le binaire `port_scanner` depuis la page Releases.
2. Accordez les droits d'exécution : `chmod +x port_scanner`
3. **Exécuter en tant que Root :** Vous devez utiliser `sudo` pour lancer l'outil afin que le noyau Linux autorise l'accès aux sockets bruts (raw sockets).

## 💻 Utilisation

**Syntaxe :**
```bash
port_scanner <ip_cible_ou_domaine> [-p <ports>]
