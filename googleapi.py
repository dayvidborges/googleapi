import pickle
import sys
import os 
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

class GoogleEngine():
    """
    author: Dayvid Borges de Lima
    date_writed: 24/10/2023
    nota:
    ao iniciar a engine execute o methodo authorize para fazer o start dos serviços.
    """
    def __init__(self) -> None:
        self.creds = 'credsPath'
        self.scopes = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/presentations']
        self.credentials = ''
        self.slides_service = ''
        self.drive_service = ''
        self.fileTypes = {'application/vnd.google-apps.folder':'Folder','application/vnd.openxmlformats-officedocument.presentationml.presentation':'ppt'}
        
    def authorize(self,credsPath):
        self.creds = credsPath
        self.credentials = service_account.Credentials.from_service_account_file(self.creds, scopes=self.scopes)
        self.slides_service = build('slides', 'v1', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        
    def deleteFile(self,IDS):
        """
        Recebe uma lista de IDS para exclusão no gDrive,
        se não houver o ID não faz nada:

        Args:
            IDS (List): Ids dos arquivos a serem excluidos
        """
        drive_service = self.drive_service

        # Liste todos os arquivos na sua conta do Google Drive
        results = drive_service.files().list().execute()
        files = results.get('files', [])

        # Exclua cada arquivo encontrado
        for file in files:
            for fileid in IDS:
                if file['id'] == fileid:
                    drive_service.files().delete(fileId=file['id']).execute()
                    print(f"{file['name']} deletado com sucesso!")
                    
    def uploadFile(self,filepath,filename):
        """Faz upload de um arquivo para o root do gdrive
        necessário mover arquivo para destino após upload
        
        Args:
            filepath (str): Path de origem do arquivo
            filename (str): Nome do arquivo
        """
        drive_service = self.drive_service
        # Especifique o arquivo de apresentação que você deseja carregar
        file_metadata = {'name': filename}

        # Crie um objeto de mídia para fazer o upload do arquivo
        media = MediaFileUpload(filepath, mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')

        # Faça o upload do arquivo para o Google Drive
        uploaded_file = drive_service.files().create(body=file_metadata, media_body=media).execute()
        print(f'{filename} upload sucess!')
        
      
    def roleControl(self,IDS,emails,role):
        """Atribui o role aos emails listados,
        deve contre reader ou writer como role.

        Args:
            IDS (list, optional): IDS dos arquivos a serem carregados. Defaults to list.
            emails (list, optional): e-mail dos usuarios a atualizar. Defaults to list.
            role (list, optional): role (reader,writer). Defaults to str.
        """
        drive_service = self.drive_service
        for file_id in IDS:
            for user_email in emails:
                # Defina a permissão de visualização
                if role == 'reader':
                    permission = {
                        'type': 'user',
                        'role': 'reader',
                        'emailAddress': user_email
                    }
                elif role == 'writer':
                    permission = {
                        'type': 'user',
                        'role': 'writer',
                        'emailAddress': user_email
                    }
                else:
                    print('role inválido!')

                # Crie a permissão
                drive_service.permissions().create(fileId=file_id, body=permission).execute()
    
    def createFolder(self,folderName, parentFolderId=None):
        """Cria uma pasta no drive, se o parametro parentFolderId 
        nao atribuido cria no root.

        Args:
            folderName (str): Nome da pasta a ser criada.
            parentFolderId (str, optional): id da pasta a ser criada dentro. Defaults to None.
        """
        drive_service = self.drive_service
        metadata = {
            'name': folderName,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parentFolderId:
            metadata['parents'] = [parentFolderId]

        pasta = drive_service.files().create(body=metadata, fields='id').execute()
        print(f"Folder {folderName} criado com sucesso!")
        
    
    def moveFile(self,file_id, newFolderId):
        """Move o arquivo para uma nova pasta

        Args:
            file_id (str): ID do arquivo a ser movido
            newFolderId (str): ID do folder de destino
        """
        drive_service = self.drive_service
        file = drive_service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        file = drive_service.files().update(fileId=file_id, addParents=newFolderId, removeParents=previous_parents, fields='id, parents').execute()
        print(f'arquivo {file.get("name")} movido com sucesso')
        
    
    def listFolders(self):
        """Lista todas as pastas no root
        """
        drive_service = self.drive_service
        results = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'", fields="files(id, name)").execute()
        pastas = results.get('files', [])
        for folder in pastas:
            print(folder['id'],folder['name'])
            
    def listElements(self,presentation_id):
        """Lista todos os elementos na apresentação

        Args:
            presentation_id (str, optional): ID da apresentação. Defaults to str.
        """
        
        slides_service = self.slides_service
        presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])

        for slide_number, slide in enumerate(slides, start=1):
            print(f"Slide {slide_number}:")
            elements = slide.get('pageElements', [])
            for element in elements:
                print('-------------------------')
                element_id = element['objectId']
                print(f"Elemento ID: {element_id}")
                try:
                    print(f"tipo de objeto:{element['shape']['shapeType']}")
                except:
                    print('Não é um objeto')
                print('------------------------\n')     
                
    def listTextElements(self,presentation_id):
        """Lista todos os elementos de texto na apresentação

        Args:
            presentation_id (str, optional): ID da apresentação. Defaults to str.
        """
        
        slides_service = self.slides_service
        presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])

        for slide_number, slide in enumerate(slides, start=1):
            print(f"Slide {slide_number}:")
            elements = slide.get('pageElements', [])
            for element in elements:
                element_id = element['objectId']
                try:
                    text = element['shape']['text']['textElements'][1]['textRun']['content']
                    print('-------------------------')
                    print(f"tipo de objeto:{text}")
                    print(f"Elemento ID: {element_id}")
                    print('------------------------\n')
                except:
                    ...
    
    def updateText(self,presentation_id, element_id, newText):
        """Atualiza um texto em um elemento que recebe texto.

        Args:
            presentation_id (str): ID da apresentação.
            element_id (str): ID do elemento.
            newText (str): texto a ser atualizado.
        """
        slides_service = self.slides_service
        requests = []
        delete_text = {
            'objectId':element_id,
            'textRange':{
                'type':'ALL'
            }
        }
        # Define o objeto UpdateTextRequest para atualizar o texto do elemento
        update_text_request = {
            'objectId': element_id,
            'text': newText,
            'insertionIndex':0
        }
        requests.append({
            'deleteText': delete_text
        })

        requests.append({
            'insertText': update_text_request
        })

        body = {
            'requests': requests
        }

        response = slides_service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
    
    def copiar_arquivo(self,file_id, copyName):
        """copia um arquivo no msm local do arquivo a ser copiadio

        Args:
            file_id (str): ID do arquivo a ser copiado.
            copyName (str): Nome da Copia

        """
        drive_service = self.drive_service
        file_metadata = {
            'name': copyName
        }

        try:
            copied_file = drive_service.files().copy(fileId=file_id, body=file_metadata).execute()
            print(copied_file['id'])
        except Exception as e:
            print(f"Erro ao copiar o arquivo: {e}")