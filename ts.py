import os
import requests
import subprocess

def download_file(url, filename):
    print("getting request")
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        print("getting chunks")
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print("complete download")

def download_ts_video(manifest_url, output_filename):
    print("Stated the process")
    # Download the manifest file
    download_file(manifest_url, 'manifest.m3u8')
    print("starting mapping")
    # Parse the manifest file to get the TS segment URLs
    with open('manifest.m3u8') as f:
        lines = f.readlines()
        ts_urls = [line.strip() for line in lines if line.startswith('http')]
    
    # Download the TS segments
    for i, ts_url in enumerate(ts_urls):
        download_file(ts_url, f'segment_{i}.ts')
    print("starting the subprocess")
    # Combine the TS segments using ffmpeg
    subprocess.run(['ffmpeg', '-i', 'concat:' + '|'.join(f'segment_{i}.ts' for i in range(len(ts_urls))), '-c', 'copy', output_filename], check=True)
    print("subprocess complted")
    print("saving")
    # Clean up temporary files
    for i in range(len(ts_urls)):
        os.remove(f'segment_{i}.ts')
    os.remove('manifest.m3u8')

if __name__ == "__main__":
    manifest_url = input("Enter the URL of the manifest file: ")
    output_filename = input("Enter the desired output filename (including file extension like .mp4): ")
    download_ts_video(manifest_url, output_filename)
