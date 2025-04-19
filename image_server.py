import json
import httpx
import os
import re
from mcp.server import FastMCP
from typing import Optional

app = FastMCP('image_server')

# 配置參數
API_ENDPOINT = os.getenv('IMAGE_API_URL', 'https://black-forest-labs-flux-1-schnell.hf.space/call/infer')
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512


@app.tool()
async def image_generation(image_prompt: str):
    """
    根據英文描述生成具備文章意境的圖片，並將圖片儲存至本地。

    參數:
        image_prompt (str): 
            用於生成圖片的英文描述。建議使用具體且生動的語句，並盡量體現文章的主題意境或氛圍。
            例如: 
                'A lonely lighthouse standing on a stormy coast, with dark clouds and crashing waves, evoking a sense of solitude and resilience.'
    回傳:
        str: 
            生成圖片的本地檔案路徑，例如 '/tmp/generated_image.png'。

    注意事項:
        - 請確保 image_prompt 內容為英文。
        - 描述應盡量具體，並能傳達文章的情感、氛圍或主題。
        - 回傳值僅包含圖片檔案的本地路徑。
    """
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(10.0, read=30.0),
        limits=httpx.Limits(max_connections=10)
    ) as http_client:

        try:
            data = {
                'data': [
                    image_prompt, 
                    0, 
                    True, 
                    DEFAULT_WIDTH,
                    DEFAULT_HEIGHT,
                    3
                ]
            }

            # 創建生成圖片任務
            response1 = await http_client.post(
                API_ENDPOINT,
                json=data,
                headers={"Content-Type": "application/json"}
            )

            # 解析響應獲取事件 ID
            response_data = response1.json()
            event_id = response_data.get('event_id')

            if not event_id:
                return {'error': 'Missing event_id in API response', 'code': 502}

            # 透過流式的方式取得返回數據
            url = f'{API_ENDPOINT}/{event_id}'
            chunks = []
            async with http_client.stream('GET', url) as response2:
                async for chunk in response2.aiter_text():
                    chunks.append(chunk)
            
            full_response = ''.join(chunks)
            return {'path': json.loads(full_response.split('data: ')[-1])[0]['url']}
        except Exception as e:
            return {'error': str(e), 'code': 500}



if __name__ == '__main__':
    app.run(transport='stdio')

