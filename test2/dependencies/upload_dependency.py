from services import UploadService
from repositories import InfoRepository, FileRepository


def get_upload_service():
    return UploadService(info_repository=InfoRepository(), file_repository=FileRepository())