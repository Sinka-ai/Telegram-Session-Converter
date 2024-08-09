import json
import os
import shutil
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, UserDeactivated, AuthKeyUnregistered
from TGConvertor.manager import SessionManager

# Настройка логирования
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Константы для папок
INPUT_DIR = 'input'
VALID_DIR = 'output/valid'
INVALID_DIR = 'output/invalid'

# Убедитесь, что нужные папки существуют
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(VALID_DIR, exist_ok=True)
os.makedirs(INVALID_DIR, exist_ok=True)


def generate_unique_name(base_name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{base_name}_{timestamp}"


def main_convert(path: str):
    with open('config.json', 'r') as file:
        config = json.load(file)
    try:
        session = SessionManager.from_tdata_folder(Path(path))
        pyrogram_string = session.to_pyrogram_string()
        app = Client(name='session', api_id=config["api_id"], api_hash=config["api_hash"],
                     session_string=pyrogram_string,system_version="4.16.30-vxCUSTOM",
    device_model="MyDevice",
    app_version="1.0")

        return app, session
    except Exception as ex:
        logging.error(f"Error converting {path}: {str(ex)}")
        return None, None


async def check_account_is_ok(client, path):
    try:
        async with client:
            user = await client.get_me()
            
            phone_number = user.phone_number
            return True
    except Exception as ex:
        logging.error(f'{path} | Account is invalid or deactivated\nError code: {str(ex)}')
        return False


async def validate_account(client, path):
    try:
        task = asyncio.create_task(check_account_is_ok(client, path))
        await asyncio.wait_for(task, timeout=15)
        return task.result()
    except asyncio.TimeoutError:
        logging.error(f'{path} | Account validation timeout')
        return False


def save_session_string(session_string, session_path):
    try:
        with open(session_path, 'w') as f:
            f.write(session_string)
    except Exception as e:
        logging.error(f"Error saving session to {session_path}: {str(e)}")


async def process_tdata_folder(tdata_path):
    client, session = main_convert(tdata_path)
    if client is None:
        unique_name = generate_unique_name(os.path.basename(tdata_path))
        shutil.move(tdata_path, os.path.join(INVALID_DIR, unique_name))
        return

    is_valid = await validate_account(client, tdata_path)
    session_name = os.path.basename(tdata_path)
    session_string = session.to_pyrogram_string()

    if is_valid:
        valid_path = os.path.join(VALID_DIR, f"{session_name}.session")
        save_session_string(session_string, valid_path)
        logging.info(f'{tdata_path} | Session is valid and saved to {valid_path}')
        shutil.move(tdata_path, os.path.join(VALID_DIR, session_name))
    else:
        invalid_path = os.path.join(INVALID_DIR, f"{session_name}.session")
        save_session_string(session_string, invalid_path)
        logging.info(f'{tdata_path} | Session is invalid and saved to {invalid_path}')
        shutil.move(tdata_path, os.path.join(INVALID_DIR, session_name))


def find_tdata_folders(root_folder):
    tdata_folders = []
    for root, dirs, files in os.walk(root_folder):
        for dir in dirs:
            if "tdata" in dir.lower():
                tdata_folders.append(os.path.join(root, dir))
    return tdata_folders


async def main():
    tdata_folders = find_tdata_folders(INPUT_DIR)
    for tdata_folder in tdata_folders:
        await process_tdata_folder(tdata_folder)


if __name__ == "__main__":
    asyncio.run(main())
