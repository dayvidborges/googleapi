# GoogleEngine

O `GoogleEngine` é uma classe Python que oferece uma interface para interagir com as APIs do Google Drive e Google Slides. Ele permite automatizar tarefas relacionadas ao Google Drive, como fazer upload de arquivos, criar pastas, atribuir permissões e muito mais. Além disso, você pode usar o `GoogleEngine` para interagir com apresentações do Google Slides, como listar elementos e atualizar texto em slides.

## Autor

- **Autor:** Dayvid Borges de Lima
- **Data de Criação:** 24/10/2023

## Instruções de Uso

1. Inicialização da Engine:
    - Antes de começar, você deve inicializar a engine com suas credenciais do Google. Para isso, execute o método `authorize(credsPath)` e forneça o caminho para o arquivo de credenciais.

2. Funções Disponíveis:
    - O `GoogleEngine` oferece várias funcionalidades para interagir com o Google Drive e Google Slides:
        - `deleteFile(IDS)`: Exclui arquivos no Google Drive com base em uma lista de IDs.
        - `uploadFile(filepath, filename)`: Faz o upload de um arquivo para o Google Drive.
        - `roleControl(IDS, emails, role)`: Atribui funções (leitor ou escritor) a usuários em arquivos no Google Drive.
        - `createFolder(folderName, parentFolderId)`: Cria pastas no Google Drive, opcionalmente dentro de uma pasta pai.
        - `moveFile(file_id, newFolderId)`: Move um arquivo para uma nova pasta.
        - `listFolders()`: Lista todas as pastas no Google Drive.
        - `listElements(presentation_id)`: Lista todos os elementos em uma apresentação do Google Slides.
        - `listTextElements(presentation_id)`: Lista todos os elementos de texto em uma apresentação do Google Slides.
        - `updateText(presentation_id, element_id, newText)`: Atualiza um elemento de texto em uma apresentação do Google Slides.
        - `copyFile(file_id, copyName)`: Copia um arquivo no mesmo local.

3. Exemplos de Uso:
    - O README fornece uma visão geral das funções disponíveis no `GoogleEngine`. Consulte a documentação dos métodos para obter detalhes sobre como usá-los.

4. Quick Start:
   ### - Se o modulo estiver no mesmo diretório do arquivo que for importado
   ```Python
    #Importe o módulo
    from googleapi import GoogleEngine
   
    #Importe os módulos do google para rodar a api
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    from googleapiclient.http import MediaFileUpload
    
    credsPath = "/caminho/para/sua/credencial.json"
    engine = GoogleEngine()
    engine.authorize(credsPath)
   ```
   ### - Se o modulo não estiver no mesmo diretório do arquivo que for importado
   ```Python
    #Import a lib sys e defina o path onde o modulo foi instalado
    import sys
    sys.path.append('caminho/') # caminho para o pasta onde o modulo foi instalado, não aponte para o modulo, sim para a pasta pai
    #Importe o módulo
    from googleapi import GoogleEngine
   
    #Importe os módulos do google para rodar a api
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    from googleapiclient.http import MediaFileUpload
    
    credsPath = "/caminho/para/sua/credencial.json"
    engine = GoogleEngine()
    engine.authorize(credsPath)
   ```

## Notas

- Lembre-se de que você precisa configurar suas credenciais do Google para usar a API do Google Drive e Google Slides.
- Certifique-se de seguir as práticas recomendadas ao manipular dados confidenciais e ao compartilhar acesso a arquivos.

---

Para obter mais informações sobre o Google APIs, consulte a documentação oficial em [Google API Python Client](https://developers.google.com/api-client-library/python/start/introduction).

Sinta-se à vontade para contribuir com melhorias e correções neste projeto. 
