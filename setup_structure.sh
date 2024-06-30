#!/bin/bash

# Navegar para a pasta raiz
cd medical_clinic/

# Criar diretórios principais
mkdir templates
mkdir static
mkdir static/css
mkdir static/js
mkdir instance

# Criar arquivos iniciais
touch app.py
touch config.py
touch requirements.txt
touch templates/base.html
touch templates/index.html
touch templates/patients.html
touch templates/patient_detail.html

# Mensagem de sucesso
echo "Estrutura de diretórios e arquivos criada com sucesso!"
