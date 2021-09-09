# geradordecertificado
Gera certificados para eventos usando o Inkscape e Python

# Requisitos

- Inkscape
- Python >3.6

# Como usar

- Crie um virtual environment com sua ferramenta preferida
- Ative o ambiente e instale as dependências com

```pip install -r requirements.txt```

ou com sua ferramenta de dependência.

- Abra o arquivo certificado.svg com o Inkscape.
- Customize o texto e as images como quiser.
- Lembre-se que o `__NOME__` e `__PARTICIPACAO__` serão substituídos no certificado gerado pelo nome do participante e o tipo de participação, respectivamente.
- Edite o programa gera.py
- Modifique o SECRET para uma chave única que validará a autenticidade dos certificados gerados
- Coloque o path para chamar o inkscape em INKSCAPE
- O arquivo csv de entrada tem seu nome configurado em ENTRADA, altere se necessário
- Se você utilizou o Excel no Windows para gerar o arquivo CSV, deixe ENTRADA_ENCODING com cp1252. Modifique para utf-8 dependendo do seu sistema operacional e do programa que gerou o csv. Caso o enconding esteja errado, os acentos não serão corretamente mostrados no certificado.
- MODELO contém o nome do svg usado como modelo para geração dos certificados. Ele será aberto e terá o nome e a participação no evento substituídos pelos valores de cada linha no arquivo csv de entrada.
- Configure os parâmetros de seu servidor de email (SMTP)
- Rode o programa com:
```
python gera.py
```
- Abra os PDFs gerados. Se tudo estiver ok, modifique a variável ENVIA_EMAIL para True. Roda novamente o programa, desta vez, um email com o certificado em PDF será enviado como anexo.

# Saídas

- qr-code.png: arquivo de imagem temporário. Usado apenas para não dar erro na hora de visualizar o svg no inkscape. Você pode apagá-lo.
- hashes.txt: arquivo de assinaturas, contem o hash do nome do participante e sua participação. Para o certificado ser válido, o QRCODE tem que conter a mesma chave.
- Cada certificado será gravado em um pdf com o nome do participante.


# Créditos

- Criado por Nilo Ney Coutinho Menezes durante a primeira PyCon Amazônia em 2017.

# Notas

- Testado com o GMAIL.
- Gere os certificados sem enviar os emails primeiro.
- Teste com um CSV pequeno para não perder tempo.
- No Windows, se o PDF estiver aberto, o programa não conseguirá sobrescrevê-lo.
- Lembre-se que a `\` do Windwos precisa ser representada com `\\` ou use raw strings `r"C:\program files\inkscape\inkscape.com"`
