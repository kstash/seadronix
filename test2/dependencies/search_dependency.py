from repositories import InfoRepository, FileRepository
from services import SearchService


def get_search_service():
    return SearchService(info_repository=InfoRepository(), file_repository=FileRepository())