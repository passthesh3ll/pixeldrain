import argparse
import os
import requests
from tqdm import tqdm
from colorama import init, Fore, Style
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from requests.auth import HTTPBasicAuth

# Initialize colorama
init()

PIXELDRAIN_UPLOAD_URL = "https://pixeldrain.com/api/file"

def upload_file(file_path, api_key, file_index=None, total_files=None):
    if not os.path.isfile(file_path):
        print(f"{Fore.RED}Error: File '{file_path}' does not exist.{Style.RESET_ALL}")
        return None

    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"{Fore.RED}Error: File is empty.{Style.RESET_ALL}")
            return None

        if file_index is not None and total_files is not None:
            print(f"{Fore.BLUE}-> [{file_index}/{total_files}] {os.path.basename(file_path)}{Style.RESET_ALL}")

        with open(file_path, 'rb') as f:
            encoder = MultipartEncoder(
                fields={'file': (os.path.basename(file_path), f, 'application/octet-stream')}
            )

            pbar = tqdm(total=file_size, unit='B', unit_scale=True, desc=f"{Fore.YELLOW}Uploading{Style.RESET_ALL}", ascii=True, leave=True)

            def progress_callback(monitor):
                pbar.update(monitor.bytes_read - pbar.n)

            monitor = MultipartEncoderMonitor(encoder, progress_callback)

            response = requests.post(
                PIXELDRAIN_UPLOAD_URL,
                auth=HTTPBasicAuth('', api_key),
                data=monitor,
                headers={'Content-Type': monitor.content_type}
            )

            pbar.close()


        # Check response status
        if response.status_code == 201:
            data = response.json()
            download_link = f"https://pixeldrain.com/u/{data['id']}"
            print(f"{Fore.GREEN}{download_link}{Style.RESET_ALL}\n")
            
            if args.log:
                output_dir = os.path.dirname(file_path) if os.path.isfile(file_path) else file_path
                filename = os.path.basename(file_path)
                log_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_links.txt")
                try:
                    with open(log_file_path, 'w', encoding='utf-8') as log_file:
                        log_file.write(f"{download_link}\n")
                except Exception as e:
                    print(f"{Fore.RED}Error saving link to file: {str(e)}{Style.RESET_ALL}")

            return {'link': download_link, 'filename': os.path.basename(file_path)}
        else:
            print(f"{Fore.RED}Upload failed with status code: {response.status_code}{Style.RESET_ALL}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"{Fore.RED}Error during upload: {str(e)}{Style.RESET_ALL}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload files or folders to Pixeldrain")
    parser.add_argument("path", help="Path to the file or folder to upload")
    parser.add_argument("--log", action="store_true", help="Save upload links to individual <filename>_links.txt files")
    parser.add_argument("--api-key", required=True, help="Pixeldrain API key")
    args = parser.parse_args()

    upload_results = []

    if os.path.isfile(args.path):
        result = upload_file(args.path, args.api_key)
        if result:
            upload_results.append(result)
    elif os.path.isdir(args.path):
        files = [os.path.join(args.path, f) for f in os.listdir(args.path) if os.path.isfile(os.path.join(args.path, f))]
        total_files = len(files)
        for index, file_path in enumerate(files, 1):
            result = upload_file(file_path, args.api_key, index, total_files)
            if result:
                upload_results.append(result)
    else:
        print(f"{Fore.RED}Error: '{args.path}' is neither a file nor a directory.{Style.RESET_ALL}")
        exit(1)

    if upload_results:
        print(f"{Fore.YELLOW}--- Uploaded files ---{Style.RESET_ALL}")
        for result in upload_results:
            print(f"{Fore.GREEN}{result['link']}{Style.RESET_ALL} {Fore.BLUE}{result['filename']}{Style.RESET_ALL}")
