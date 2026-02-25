import httpx
import uuid

api_base_uri = "http://127.0.0.1:8188"

async def new_uuid():
    return str(uuid.uuid4())

async def api_get(endpoint: str, params: object | None):
    async with httpx.AsyncClient(base_url=api_base_uri) as client:
        response = await client.get(endpoint, params=params)
        return response

async def api_post(endpoint: str, data):
    async with httpx.AsyncClient(base_url=api_base_uri) as client:
        response = await client.post(endpoint, data=data)
        return response

async def api_upload(endpoint: str, files, data):
    async with httpx.AsyncClient(base_url=api_base_uri) as client:
        response = await client.post(endpoint, data=data, files=files)
        return response

async def api_download(endpoint: str, params: object | None):
    async with httpx.AsyncClient(endpoint=api_base_uri) as client:
        response = await client.get(endpoint, params=params)
        return response
