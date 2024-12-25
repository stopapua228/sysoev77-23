import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from virtual_shell import VirtualShell


@pytest.fixture
def setup_shell():
    shell = VirtualShell('virtual_fs.tar', 'log.json')
    shell.cd('/')  # Убедитесь, что тест начинается с корня
    return shell


def test_ls(setup_shell):
    shell = setup_shell
    # Ожидаем, что корневой каталог ("/") содержит три директории
    structure = shell.ls()
    expected_structure = ['dir1/', 'dir2/', 'dir3/']

    for item in expected_structure:
        assert item in structure, f"Missing {item} in ls output"


def test_cd(setup_shell):
    shell = setup_shell

    # Переход в 'dir1' и проверка содержимого
    shell.cd('dir1')
    assert shell.pwd().endswith('dir1')
    assert 'file3.txt' in shell.ls()

    # Переход в 'dir2' и проверка подпапки
    shell.cd('/')
    shell.cd('dir2/subdir1')
    assert shell.pwd().endswith('subdir1')
    assert 'file4.md' in shell.ls()

    # Переход в 'dir3' и проверка файлов
    shell.cd('/')
    shell.cd('dir3')
    assert shell.pwd().endswith('dir3')
    assert 'file1.txt' in shell.ls()
    assert 'file2.log' in shell.ls()


def test_pwd(setup_shell):
    shell = setup_shell
    assert shell.pwd() == '/'

    # Переход и проверка текущего пути
    shell.cd('dir1')
    assert shell.pwd().endswith('dir1')