<h1 align="center" style="font-weight: bold">
    Getting Started
</h1>

<div class="toc">
    <h2 id="toc"><b><a href="#toc">Table of Contents</a></b></h2>
    <p>Choose the desired operating system below:</p>
    <ul>
        <li><a href="#windows">Windows</a></li>
        <li>
            <a href="#linux">Linux</a>
            <ul>
                <li><a href="#linux-debian">Debian</a></li>
                <li><a href="#linux-fedora">Fedora</a></li>
                <li><a href="#linux-arch">Arch</a></li>
            </ul>
        </li>
    </ul>
</div>

<h2 id="installing-prerequisites-windows"><a href="#windows">Windows</a></h2>

1. Follow the instructions at [this link](./installing-prerequisites.md#windows) for installing the prerequisites.

<h2 id="installing-prerequisites-linux"><a href="#linux">Linux</a></h2>

<h3 id="installing-prerequisites-linux-debian"><a href="#linux-debian">Debian</a></h3>

1. Open your preferred terminal and run the following command to install the prerequisites:

    ```sh
    sudo apt update -y
    sudo apt install -y git just python3 python3-pip
    ```

<h3 id="installing-prerequisites-linux-fedora"><a href="#linux-fedora">Fedora</a></h3>

1. Open your preferred terminal and run the following command to install the prerequisites:

    ```sh
    sudo dnf install -y git just python3.12
    ```

<h3 id="installing-prerequisites-linux-arch"><a href="#linux-arch">Arch</a></h3>

1. Open your preferred terminal and run the following command to install the prerequisites:

    ```sh
    sudo pacman -Syyu --noconfirm git just python312
    ```
