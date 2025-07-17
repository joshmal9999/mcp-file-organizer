import os

def list_files(directory: str) -> list[str]:
    """지정된 디렉토리의 파일 및 하위 디렉토리 목록을 반환합니다."""
    try:
        return os.listdir(directory)
    except FileNotFoundError:
        return ["Error: Directory not found."]

def create_directory(directory: str) -> dict:
    """새로운 디렉토리를 생성합니다."""
    try:
        os.makedirs(directory, exist_ok=True)
        return {"message": f"Directory '{directory}' created successfully."}
    except Exception as e:
        return {"error": str(e)}
