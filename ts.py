import requests
import os
import subprocess

def download_file(url, filename):
    response = requests.get(url, stream=True,headers={   
    'User-Agent': 'Mozilla/5.0',  # Example User-Agent header
    'Authorization': 'Bearer YOUR_TOKEN', 
    })
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def download_video(manifest_url):
    # Create a directory to store the video segments
    os.makedirs('segments', exist_ok=True)

    # Download the manifest file
    download_file(manifest_url, 'manifest.m3u8')
    
    # Parse the manifest file to get the TS segment URLs
    base_url = "https://streamcdneu.loco.gg/1540KCGYBH_193b223c-6576-4353-a5e6-28e751725863/1540KCGYBH_193b223c-6576-4353-a5e6-28e751725863_low/"
    with open('manifest.m3u8') as f:
        lines = f.readlines()
        ts_urls = [base_url +line.strip() for line in lines if line.startswith('16')]
    
    # Download the TS segments
    for i, ts_url in enumerate(ts_urls):
        download_file(ts_url, f'segments/segment_{i}.ts')
    print(f'Downloaded {len(ts_urls)} segments.')

def concatenate_segments(output_filename):
    segment_files = [f'segments/segment_{i}.ts' for i in range(len(os.listdir('segments')))]

    with open('file_list.txt', 'w') as file_list:
        for segment_file in segment_files:
            file_list.write(f"file '{segment_file}'\n")

    cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'file_list.txt', '-c', 'copy', output_filename]

    subprocess.run(cmd, check=True)




if __name__ == "__main__":
    manifest_url = "https://streamcdneu.loco.gg/1540KCGYBH_193b223c-6576-4353-a5e6-28e751725863/1540KCGYBH_193b223c-6576-4353-a5e6-28e751725863_hi/video.m3u8"
    output_filename = 'file_out.mp4'
    
    download_video(manifest_url)
    concatenate_segments(output_filename)

